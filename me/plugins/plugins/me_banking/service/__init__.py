from me.logger import MeLogger, DEBUG
from me.storage import StorageManagerCapsule, DataType
from flask import Flask, jsonify

from multiprocessing import Process
from threading import Thread


class BankingAPI:
    def __init__(self, data: StorageManagerCapsule):
        self.log = MeLogger(name=__name__, level=DEBUG)
        self.data_manager = data
        self.app = Flask(__name__)
        self._subproc = None
        self.app.add_url_rule(rule='/', endpoint='root', view_func=self.hello)
        self.app.add_url_rule(rule='/data', endpoint='data', view_func=self.data)

    def run(self):
        self._subproc = Thread(target=lambda: self.app.run(port=5001, debug=True, use_reloader=False))  # FIXME should be a proc not a thread
        self._subproc.start()

    def hello(self):
        return 'Hello, World! (banking service)', 200

    def data(self):
        self.log.info('/data called in', __name__)
        data = self.data_manager.getAllRows(DataType.TXs)
        self.log.debug('retrieved data', data)
        return jsonify(data), 200
