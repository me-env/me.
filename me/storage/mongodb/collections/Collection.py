from me.storage.mongodb.config import BULK_LIMIT, BULK_MIN
from me.storage.mongodb.config import mongo_to_python
from me.tools import fread_json


class Collection:
    def __init__(self, db, name, logger, reset=False, schema_file=None):
        self.db = db
        self.name = name
        self.bulk_buffer = []
        self.schema = fread_json(schema_file)
        self.col = self.getCollection()
        self.log = logger

        if reset is True and self.col is not None:
            self.resetCollection()
        elif self.col is None:
            self.createCollection(self.schema)

    def collectionExists(self):
        return self.name in self.db.list_collection_names()

    def getCollection(self):
        if not self.collectionExists():
            return None
        return self.db[self.name]

    def createCollection(self, val_expr=None):
        self.db.create_collection(self.name)
        if val_expr:
            self.log.debug("val_expr", val_expr)
            self.db.command('collMod', self.name, validator=val_expr, validationLevel='moderate')
        self.col = self.getCollection()
        self.log.info(f"Collection {self.name} created.")

    def dropCollection(self):
        self.col.drop()
        self.log.info(f"Collection {self.name} dropped.")

    def resetCollection(self):
        """
        Drop the collection and recreate it
        """
        self.dropCollection()
        self.createCollection(self.schema)
        self.log.info(f"Collection {self.name} reset.")

    def deleteAll(self):
        self.col.delete_many({})

    def bulkWrite(self, content, force=False):
        self.bulk_buffer.append(content)
        if len(self.bulk_buffer) >= BULK_LIMIT or force:
            self.flushBulk()

    def flushBulk(self):
        if len(self.bulk_buffer) >= BULK_MIN:
            self.log.debug('Write Flush', self.name, "len", len(self.bulk_buffer))
            results = self.col.bulk_write(self.bulk_buffer)
            self.bulk_buffer = []
            self.log.debug("bulk write result", results.bulk_api_result)

    def flush(self):
        self.flushBulk()

    def update(self, query, update):
        self.col.update_many(query, update)

    def insert(self, document):
        self.log.debug('insert', document)
        self.col.insert_one(document)

    def delete(self, query):
        self.col.delete_one(query)

    @property
    def schema_types(self):
        __required = {i: object for i in self.schema['$jsonSchema']['required']}
        self.log.debug(self.schema['$jsonSchema']['properties'])
        __properties = {i: self.schema['$jsonSchema']['properties'][i]['bsonType'] for i in self.schema['$jsonSchema']['properties']}
        res = {**__required, **__properties}
        check = {i: mongo_to_python(res[i], 'check') for i in res}
        convert = {i: mongo_to_python(res[i], 'convert') for i in res}
        return check, convert

    def __getitem__(self, arg):
        """
        :description: Perform a query over a collection (within a specific shard)
        :arg arg: filters to perform the query
        """
        return self.col.find(arg)

    def __str__(self):
        return ''.join([u.__str__() for u in self.col.find({})])
