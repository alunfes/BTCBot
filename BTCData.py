import pandas as pd
import threading
import copy

class BTCData:
    @classmethod
    def initialize(cls):
        cls.lock_ac = threading.Lock()
        cls.exes_for_account = pd.DataFrame()

        cls.lock_db = threading.Lock()
        cls.exes_for_db = pd.DataFrame()

    @classmethod
    def add_execution_data(cls, data):
        df = pd.DataFrame.from_dict(data)
        with cls.lock_ac:
            cls.exes_for_account = pd.concat([cls.exes_for_account, df], axis=0, ignore_index=True)
        with cls.lock_db:
            cls.exes_for_db = pd.concat([cls.exes_for_account, df], axis=0, ignore_index=True)

    @classmethod
    def get_exes_for_account(cls):
        with cls.lock_ac:
            res = copy.deepcopy(cls.exes_for_account)
            cls.exes_for_account =pd.DataFrame()
            return res


    @classmethod
    def get_exes_for_db(cls):
        with cls.lock_db:
            res = copy.deepcopy(cls.exes_for_db)
            if len(res) >= 100000:
                cls.exes_for_db.drop(range(0, 10000), inplace=True)
        return cls.exes_for_db





