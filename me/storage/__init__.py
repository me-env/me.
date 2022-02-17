from typing import List

from me.storage.mongodb import Mongodb
from me.storage.data_config import DataType, DataAccess, DataAction
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
            f'{DataType.TXs.value}': 'psql'
        }

    def getSchema(self, data_type):
        check, convert = self.dbs[self.link_data_db[data_type.value]].getScheme(data_type)
        return [i for i in check], check, convert

    def addRow(self, data_type, data):
        self.log.debug("add row", data_type, ':', data)
        self.dbs[self.link_data_db[data_type.value]].addRow(data_type, data)

    def addMultipleRows(self, data_type, data):
        self.log.debug(f"add multiple rows {len(data)}", data_type, data)
        self.dbs[self.link_data_db[data_type.value]].addMultipleRows(data_type, data)

    def updateRow(self, data_type, data):
        self.log.debug("update row", data_type, ':', data)
        self.dbs[self.link_data_db[data_type.value]].updateRow(data_type, data)

    def updateMultipleRow(self, data_type, data):
        self.log.debug("add multiple rows", data_type, ':', data)
        self.dbs[self.link_data_db[data_type.value]].updateMultipleRow(data_type, data)

    def reset(self):
        self.__applyOnDbManagers(lambda x: x.reset())

    def getAllRows(self, data_type):
        self.log.debug("retrieve all rows", data_type)
        return self.dbs[self.link_data_db[data_type.value]].getAllRows(data_type)

    def __applyOnDbManagers(self, fct):
        list(map(fct, self.dbs.values()))


class StorageManagerCapsule:  # TODO I feel like this is not an optimal way of doing it.
    def __init__(self, storage_manager, access: List[DataAccess]):
        """
        StorageManagerCapsule let you get instances of StorageManager on which you can only perform limited operations depending on the parameters.
        in theory, it is at the creation of this class by a given plugin that the user is asked if he authorizes the plugins to access data and performing x operations on it.
        """
        self.log = MeLogger(name=__name__)
        self._storage_manager = storage_manager
        self._access = access

    def addRow(self, data_type, data):
        minimum_needed_rights = DataAccess(data_type, [DataAction.CREATE])
        if any([minimum_needed_rights <= a for a in self._access]):
            self._storage_manager.addRow(data_type, data)
        else:
            self.log.warn(f'app tried to access {__name__} with not enough rights.\nCurrent rights:', self._access, '\nNeeded rights:', minimum_needed_rights)

    def addMultipleRows(self, data_type, data):
        minimum_needed_rights = DataAccess(data_type, [DataAction.CREATE])
        if any([minimum_needed_rights <= a for a in self._access]):
            self._storage_manager.addMultipleRows(data_type, data)
        else:
            self.log.warn(f'app tried to access {__name__} with not enough rights.\nCurrent rights:', self._access, '\nNeeded rights:', minimum_needed_rights)

    def updateRow(self, data_type, data):
        minimum_needed_rights = DataAccess(data_type, [DataAction.UPDATE])
        if any([minimum_needed_rights <= a for a in self._access]):
            self._storage_manager.updateRow(data_type, data)
        else:
            self.log.warn(f'app tried to access {__name__} with not enough rights.\nCurrent rights:', self._access, '\nNeeded rights:', minimum_needed_rights)

    def updateMultipleRow(self, data_type, data):
        minimum_needed_rights = DataAccess(data_type, [DataAction.UPDATE])
        if any([minimum_needed_rights <= a for a in self._access]):
            self._storage_manager.updateMultipleRow(data_type, data)
        else:
            self.log.warn(f'app tried to access {__name__} with not enough rights.\nCurrent rights:', self._access, '\nNeeded rights:', minimum_needed_rights)
            
    def getAllRows(self, data_type):
        minimum_needed_rights = DataAccess(data_type, [DataAction.READ])
        if any([minimum_needed_rights <= a for a in self._access]):
            return self._storage_manager.getAllRows(data_type)
        else:
            self.log.warn(f'app tried to access {__name__} with not enough rights.\nCurrent rights:', self._access, '\nNeeded rights:', minimum_needed_rights)
        return None

    def reset(self):
        # TODO check if it has correct accesses
        self._storage_manager.reset()
