from me.storage.i_database import IDatabase
from me.storage.mongodb.collections.Transaction import Transaction
from me.storage.mongodb.config import s00, db_name
from me.storage.data_config import DataType
from me.logger import *

import pymongo


class Mongodb(IDatabase):
    """
    At this point mongodb architecture is created to work using only one shard.
    """
    def __init__(self):
        self.log = MeLogger(name=__name__)
        self.clients, self.shs, self.dbs = self.connect()
        if not self.isConnectionValid():
            return

        self.log.i('dbs loaded:', self.dbs)
        self.collections = {
            DataType.TXs: Transaction(self.dbs['s00'])
        }

    def addRow(self, data_type, tx):
        self.collections[data_type].addRow(tx)

    def addMultipleRows(self, data_type, txs):
        self.collections[data_type].addMultipleRows(txs)

    def reset(self):
        self.__applyToCollections(lambda x: x.resetCollection())

    def getScheme(self, data):
        return self.collections[data].schema_types

    def getAllRows(self, data_type):
        pass  # TODO

    def connect(self):
        self.log.info("Connect to", s00)
        clients = dict(
            s00=pymongo.MongoClient(s00, connect=True, socketTimeoutMS=12000, serverSelectionTimeoutMS=1000),
        )
        shs = dict(
            s00=clients['s00'],
        )
        dbs = dict(
            s00=shs['s00'][db_name],
        )
        return clients, shs, dbs

    def isConnectionValid(self):
        self.log.i('Check connection to mongodb')
        try:
            self.log.d(self.dbs['s00'].list_collection_names())
            self.log.i('Connection OK to s00 mongodb')
            return True
        except pymongo.errors.OperationFailure as e:
            self.log.error("Connection to mongodb failed", e)
        return False

    def __applyToCollections(self, fct):
        if self.isConnectionValid():
            list(map(fct, self.collections.values()))

