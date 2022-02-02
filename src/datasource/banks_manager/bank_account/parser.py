from abc import ABCMeta, abstractmethod
from datetime import datetime

import pandas as pd


class IParser(metaclass=ABCMeta):
    @abstractmethod
    def parse(self, data, columns):
        """ Parse the given data """


class TinkParser(IParser):
    def __init__(self):
        self.parser = {
            "transaction_id": lambda x: x['id'],
            "transaction_name": lambda x: x['descriptions']['original'],
            "account_id": lambda x: x['accountId'],
            "account_name": lambda x: x['accountName'],
            "amount": TinkParser.get_amount,
            "type": TinkParser.get_type,
            "tx_date": lambda x: datetime.strptime(x['dates']['booked'], '%Y-%m-%d'),
            "refunded": lambda x: False,
            "refunded_double_checked": lambda x: False,
            "timestamp": lambda x: None,
            "payment": lambda x: True if x['amount']['value']['unscaledValue'][0] == '-' else False
        }

    def __getitem__(self, item):
        return self.parser[item]

    def parse(self, data, columns):  # TODO, not happy with the way this works.
        data = {c: list(map(lambda x: self[c](x), data)) for c in columns}
        data = pd.DataFrame(data, columns=columns).to_dict('records')
        return data

    @staticmethod
    def remove_neq(data, key, value):  # TODO make this work with multiple levels (ex: ["amount"]["value"]..)
        return [i for i in data if i[key] == value]

    @staticmethod
    def get_amount(tx):
        raw = tx['amount']['value']['unscaledValue']
        sep = len(raw) - int(tx['amount']['value']['scale'])
        return float(f"{raw[:sep]}.{raw[sep:]}")

    @staticmethod
    def get_type(tx):
        return []

    def addBankName(self, txs, bank_name):
        txs = list(map(lambda x: dict(x, **{'accountName': bank_name}), txs))
        return txs




