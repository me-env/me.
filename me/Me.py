from me.plugins.banks_manager import BanksManager
from me.storage import StorageManager
from me.storage.datalist import Data
from me.logger import MeLogger, DEBUG, DEFAULT


class Me:
    def __init__(self):
        self.log = MeLogger(name=__name__, level=DEFAULT)
        self.accounts = BanksManager()
        self.db = StorageManager()
        self.plugins = list()

        self.commands_map = {
            'update': {'cmd': self.updateTxsInDb,
                       'help': 'run update on all data sources and update databases'},
            'reset': {'cmd': self.resetDbs,
                      'help': 'reset all content in dbs (make them empty/remove/recreate)'},
            'help': {'cmd': self.help,
                     'help': 'display this help section'}
        }

    def resetDbs(self):
        self.db.reset()

    def update(self):
        pass

    def updateTxsInDb(self):
        """
        Get transactions from transactions datasource, then add them in databases
        :return:
        """
        # This has to be changed because information about format have to come from datasource
        columns, check, convert = self.db.getSchema(Data.TXs)
        txs = self.accounts.getAllTransactions(columns, check, convert)

        self.log.info(f"Add {len(txs)} transactions")
        self.db.addMultipleRows(Data.TXs, txs)

    def help(self):
        """
        print the help for each command
        """
        print('\n\r'.join([f'\033[33;1m{i}\033[0m \t {self.commands_map[i]["help"]}' for i in self.commands_map]))

    def run(self, command):
        """
        Run a given command
        :param command: command as a string
        """
        if command in self.commands_map:
            self.commands_map[command]['cmd']()
        elif command != '':
            print(f'command `{command}` does not exist, please use command `help` to find out existing commands.')


