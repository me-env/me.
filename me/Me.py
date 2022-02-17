from me.plugins.plugins.me_banking import MeBankingDataSource, MeBankingService
from me.storage import StorageManager, StorageManagerCapsule
from me.storage.data_config import DataType
from me.logger import MeLogger, DEFAULT
from me.plugins import IDataSource, IService


class Me:
    def __init__(self):
        """
        Me class is the "main" class. It is used to load plugins, setup storage manager and run commands.
        It connects the different components together such as the shell, the plugin and the storage (later: map reduce tools).
        """
        self.log = MeLogger(name=__name__, level=DEFAULT)
        self.storage = StorageManager()
        self.plugins = {  # TODO plugins should be detected automatically
            'datasource': [MeBankingDataSource()],
            'plugins': [MeBankingService()]
        }

        self.commands_map = {
            'update': {'cmd': self.updateAllDatasource,
                       'help': 'run update on all data source plugins and update databases'},
            'run': {'cmd': self.runAllServices,
                    'help': 'run all available service plugins'},
            'reset': {'cmd': self.resetDbs,
                      'help': 'reset all content in dbs (make them empty/remove/recreate)'},
            'help': {'cmd': self.help,
                     'help': 'display this help section'}
        }

    def resetDbs(self) -> None:
        """
        Remove all content in all dbs
        """
        self.storage.reset()

    def runAllServices(self) -> None:
        """
        Run all currently connected plugins implementing a service
        """
        for srv in self.plugins['plugins']:
            self.__runService(srv)

    def __runService(self, srv: IService) -> None:
        """
        Run a specific service by first asking what data access it needs and then giving it through the 'run' function.
        The user has to agree the data access request.
        """
        neededData = srv.neededDataDetails()
        data = StorageManagerCapsule(self.storage, neededData)
        srv.run(data)

    def updateAllDatasource(self) -> None:
        """
        Update all data sources by fetching data sources and sending data to the storage
        """
        for ds in self.plugins['datasource']:
            self.__updateDatasource(ds)

    def __updateDatasource(self, datasource: IDataSource) -> None:
        """
        Update one specific data source by fetching it and sending data to the storage
        """
        data_type = datasource.getStorageDetails()['type']
        columns, check, convert = self.storage.getSchema(data_type)

        data = datasource.getData(columns, check, convert)

        self.log.info(f"Fetched data: {len(data)}")
        self.storage.addMultipleRows(data_type, data)

    def help(self):
        """
        print the help for each command
        """
        print('\n\r'.join([f'\033[33;1m{i}\033[0m \t {self.commands_map[i]["help"]}' for i in self.commands_map]))

    def execute(self, command):
        """
        Run a given command
        :param command: command as a string
        """
        if command in self.commands_map:
            self.commands_map[command]['cmd']()
        elif command != '':
            print(f'command `{command}` does not exist, please use command `help` to find out existing commands.')
