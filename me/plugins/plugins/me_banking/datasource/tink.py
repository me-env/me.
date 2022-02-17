from me.logger import MeLogger, DEFAULT
from me.plugins.plugins.me_banking.datasource.parser import TinkParser
import requests
import json
import os

usages_cpd = {
    'rtxs': 'transactions:read',
    'racc': 'accounts:read',
    'report': 'account-verification-reports:read',
    'ridt': 'identity:read',
    'usrc': 'user:create'
}

bank_id_to_name = {
    'de0074746603468b9259d368e13e6fa3': 'cic',
    'a7f4775b2e2b4103b885f6214beeff30': 'boursorama'
}

bank_name_to_id = {bank_id_to_name[i]: i for i in bank_id_to_name}


class BankAccountTink:
    """
    BankAccount manager for banks implemented by Tink (tink.com)
    """
    def __init__(self, bank_name):
        self.log = MeLogger(name=__name__, level=DEFAULT)

        self.bank_id = None
        self.bank_name = bank_name
        if bank_name not in bank_name_to_id:
            self.log.warn('Bank', bank_name, 'is not registered')
        else:
            self.bank_id = bank_name_to_id[bank_name]

        self.log.info('Setup bank:', bank_name)

        self._client_id = os.environ['CLIENT_ID']
        self._client_secret = os.environ['CLIENT_SECRET']
        self._external_user_id = os.environ['EXTERNAL_USER_ID']

        self._authorization_token = self.__getAuthorizationToken()
        self._code = self.__getCode()
        self._token = self.__getToken()

        self.parser = TinkParser()

    def __getAuthorizationToken(self):
        url = 'https://api.tink.com/api/v1/oauth/token'

        payload = dict(
            client_id=self._client_id,
            client_secret=self._client_secret,
            grant_type='client_credentials',
            scope='user:create,authorization:grant'
        )
        res = requests.post(url, data=payload)

        token = json.loads(res.text)['access_token']
        return token

    def __getCode(self):
        url = 'https://api.tink.com/api/v1/oauth/authorization-grant'

        payload = dict(
            external_user_id=self._external_user_id,
            scope='accounts:read,balances:read,transactions:read,provider-consents:read,authorization:grant,balances:read,credentials:read,credentials:refresh,credentials:write,identity:read,link-session:read,link-session:write,payment:read,payment:write,provider-consents:read,providers:read,transactions:read,transfer:execute,transfer:read,user:create,user:delete,user:read,user:web_hooks,webhook-endpoints'
        )
        res = requests.post(url, headers={'Authorization': f'Bearer {self._authorization_token}'}, data=payload)
        code = json.loads(res.text)['code']
        return code

    def __getToken(self):
        url = 'https://api.tink.com/api/v1/oauth/token'

        payload = dict(
            client_id=self._client_id,
            client_secret=self._client_secret,
            grant_type='authorization_code',
            code=self._code
        )
        res = requests.post(url, data=payload)

        token = json.loads(res.text)['access_token']
        return token

    def listAccounts(self):
        url = 'https://api.tink.com/api/v1/accounts/list'

        res = requests.get(url, headers={'Authorization': f'Bearer {self._token}'})
        print(f'[account list] {self.bank_name} code: [{res.status_code}] reason: \'{res.reason}\'')
        print('Accounts', res.text)

    def listTransactions(self):
        url = 'https://api.tink.com/api/v1/search'
        res = requests.get(url, headers={'Authorization': f'Bearer {self._token}'})
        print(res.__dict__)
        print(res.status_code, res.reason)
        print('txs', res.text)
        print(res.content)
        with open('txs.json', 'w') as f:
            f.write(res.text)

    def listTransactionsV2(self):
        url = 'https://api.tink.com/data/v2/transactions'
        res = requests.get(url, headers={'Authorization': f'Bearer {self._token}'})
        print(res.__dict__)
        print(res.status_code, res.reason)
        print('txs', res.text)
        print(res.content)
        with open('txs.json', 'w') as f:
            f.write(res.text)

    def exportReport(self):
        url = 'https://api.tink.com/api/v1/account-verification-reports/6ea86c639a97493f9808485279a4b0cd/pdf?template=standard-1.0'
        res = requests.get(url, headers={'Authorization': f'Bearer {self._token}'})

        with open('data/report.pdf', 'wb') as f:
            f.write(res.content)

    def listIdentityData(self):
        url = 'https://api.tink.com/api/v1/identities'
        res = requests.get(url, headers={'Authorization': f'Bearer {self._token}'})
        print(f'[Identity list] {self.bank_name} code: [{res.status_code}] reason: \'{res.reason}\'')
        print(f'[Identity list] {res.text}')

    def __fetchTransactions(self, page_token=None):
        url = 'https://api.tink.com/data/v2/transactions?pageSize=100'

        if page_token:
            url += f'&pageToken={page_token}'
            self.log.debug('add page token', page_token)
        self.log.debug('request txs', url, self._token)
        res = requests.get(url, headers={'Authorization': f'Bearer {self._token}'})
        res = json.loads(res.text)

        # self.log.debug('txs %s', res)
        self.log.debug('LEN_ %d', len(res['transactions']))

        next_page_token = res['nextPageToken']
        txs = res['transactions']

        return txs, next_page_token

    def getTransactions(self, min_timestamp=None):
        """
        ((unused))
        :param min_timestamp: TODO
        :return: transactions
        """
        txs, next_page_token = self.__fetchTransactions()
        return txs

    def getAllTransactions(self, columns, check, convert):
        """
        get all transactions from a the account. Make the transaction format match columns
        TODO fix this function which is a little messy
        :param columns: columns to match
        :param check: tool to check the type of the data matches what is needed
        :param convert: tool to convert the data to the correct type if possible
        :return:
        """
        all_txs, next_page_token = self.__fetchTransactions()
        first_page_next_token = next_page_token
        first = True
        while len(all_txs) == 100 and next_page_token and (next_page_token != first_page_next_token or first is True):
            txs, next_page_token = self.__fetchTransactions(page_token=next_page_token)
            all_txs += txs
            first = False

        txs = TinkParser.remove_neq(data=all_txs, key='accountId', value=self.bank_id)
        txs = self.parser.addBankName(txs, bank_name=self.bank_name)
        txs = self.parser.parse(txs, columns)
        self.log.debug(self.bank_name, self.bank_id, txs)
        return txs





