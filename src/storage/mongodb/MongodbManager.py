from src.storage.mongodb.collections.Transaction import Transaction
from src.storage.mongodb.config import s00, db_name
from src.storage.datalist import Data
from src.logger import *

import pymongo


class MongodbManager:
    """
    At this point mongodb architecture is created to work using only one shard.
    """
    def __init__(self):
        self.log = MeLogger(name=__name__)
        self.clients, self.shs, self.dbs = self.connect()
        self.checkConnection()
        self.log.i('dbs loaded:', self.dbs)

        self.collections = {
            Data.TXs: Transaction(self.dbs['s00'])
        }

    def addRow(self, data_type, tx):
        self.collections[data_type].addRow(tx)

    def addMultipleRows(self, data_type, txs):
        self.collections[data_type].addMultipleRows(txs)

    def reset(self):
        self.__applyToCollections(lambda x: x.resetCollection())

    def getSchema(self, data):
        return self.collections[data].schema_types

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

    def checkConnection(self):
        self.log.i('Check connection to mongodb')
        self.log.d(self.dbs['s00'].list_collection_names())
        self.log.i('Connection OK to s00 mongodb')

    def __applyToCollections(self, fct):
        list(map(fct, self.collections.values()))

