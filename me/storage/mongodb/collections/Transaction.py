from .Collection import Collection
from me.storage.data_config import DataType
from datetime import datetime
from me.logger import MeLogger, DEBUG


class Transaction(Collection):
    def __init__(self, db, reset=False):
        self.log = MeLogger(name=__name__)
        super().__init__(db, DataType.TXs.value, self.log, reset, "schemas/transaction_schema.json")

    def addRow(self, tx):
        tx['timestamp'] = datetime.now()  # Does it really have to be done here?
        self.log.debug("Try to insert tx", tx)
        result = self.col.insert_one(tx)
        self.log.debug("add transaction, result", result)

    def addMultipleRows(self, txs):
        time_ = datetime.now()
        txs = list(map(lambda x: dict(x, **{'timestamp': time_}), txs))
        self.log.debug('Insert', len(txs), 'transactions')
        self.col.insert_many(txs)

