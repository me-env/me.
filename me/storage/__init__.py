from me.storage.mongodb import Mongodb
from me.storage.datalist import Data
from me.logger import MeLogger, DEBUG
from me.storage.postgresql import PostgreSQL


class StorageManager:
    def __init__(self):
        self.log = MeLogger(name=__name__)
        self.dbs = dict(
            mongodb=Mongodb(),
            psql=PostgreSQL()
        )
        self.link_data_db = {
            f'{Data.TXs.value}': 'psql'
        }

    def getSchema(self, data_type):
        check, convert = self.dbs[self.link_data_db[data_type.value]].getScheme(data_type)
        return [i for i in check], check, convert

    def addRow(self, data_type, data):
        self.log.debug("add row", data_type, ':', data)
        self.dbs[self.link_data_db[data_type.value]].addRow(data_type, data)

    def addMultipleRows(self, data_type, data):
        self.log.debug(f"add {len(data)} rows", data_type)
        self.dbs[self.link_data_db[data_type.value]].addMultipleRows(data_type, data)

    def reset(self):
        self.__applyOnDbManagers(lambda x: x.reset())

    def __applyOnDbManagers(self, fct):
        list(map(fct, self.dbs.values()))
