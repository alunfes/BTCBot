import pandas as pd
import threading
import copy

class BTCData:
    @classmethod
    def initialize(cls):
        cls.lock = threading.Lock()
        cls.exes_for_account = pd.DataFrame()

    @classmethod
    def add_exes_for_account(cls, data):
        with cls.lock:
            cls.exes_for_account = pd.concat([cls.exes_for_account, pd.DataFrame.from_dict(data)], axis=0, ignore_index=True)

    @classmethod
    def get_exes_for_account(cls):
        with cls.lock:
            res = copy.deepcopy(cls.exes_for_account)
            cls.exes_for_account =pd.DataFrame()
            return res





