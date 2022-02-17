from me.logger import MeLogger, DEFAULT

from .tink import BankAccountTink


class BanksManager:
    def __init__(self):
        self.log = MeLogger(name=__name__, level=DEFAULT)
        self.log.info('Setup Bank Accounts')
        self.accounts = {
            'cic': BankAccountTink('cic'),
            'boursorama': BankAccountTink('boursorama'),
            # Can add from other sources than tink
        }

    def getTransactions(self, min_timestamp=None):
        """
        ((unused))
        Get transactions from all accounts
        :param min_timestamp: ((unused))
        :return: all fetched transactions
        """
        txs = []
        for account in self.accounts:
            txs_account = self.accounts[account].getTransactions(min_timestamp)
            self.log.debug('txs_account', txs_account)
            txs += txs_account
        return txs

    def getAllTransactions(self, columns, check, convert):
        """
        Get all transactions from all accounts
        :return: all fetched transactions
        """
        txs = []
        for account in self.accounts:
            self.log.debug("get transactions")
            txs_account = self.accounts[account].getAllTransactions(columns, check, convert)
            self.log.info('add', len(txs_account), 'transactions for account', account)
            self.log.debug('append', txs_account)
            txs += txs_account

        return txs


