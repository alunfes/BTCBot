import pandas as pd
import threading
from datetime import datetime, timedelta
import IndexData
import copy
import time

#[{'id': 821682156, 'side': 'SELL', 'price': 395067.0, 'size': 0.015, 'exec_date': '2019-02-16T13:47:51.0022592Z', 'buy_child_order_acceptance_id': 'JRF20190216-134750-185055', 'sell_child_order_acceptance_id': 'JRF20190216-134748-681261'}
class BTCData:
    @classmethod
    def initialize(cls):
        cls.lock_ac = threading.Lock()
        cls.exes_for_account = pd.DataFrame()
        cls.lock_db = threading.Lock()
        cls.exes_for_db = pd.DataFrame()
        IndexData.IndexData.start(500)

    @classmethod
    def add_execution_data(cls, data):
        df = pd.DataFrame.from_dict(data)
        df['exec_date'] = df['exec_date'].map(cls.dt_converter)
        with cls.lock_ac:
            cls.exes_for_account = pd.concat([cls.exes_for_account, df], axis=0, ignore_index=True)
            #print(cls.exes_for_account)
            #print(len(cls.exes_for_account))
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

    @classmethod
    def get_latest_exes_for_db(cls):
        with cls.lock_db:
            if len(cls.exes_for_db) > 0:
                return cls.exes_for_db[len(cls.exes_for_db)-1:len(cls.exes_for_db)]
            else:
                return None

    @classmethod
    def get_current_price(cls):
        with cls.lock_db:
            if len(cls.exes_for_db) > 0:
                p = cls.exes_for_db['price']
                return p[len(p)-1]
            else:
                return None

    @classmethod
    def dt_converter(cls, dt):
        utc_split = datetime(
            year = int(dt[0:4]), month = int(dt[5:7]), day = int(dt[8:10]),
            hour = int(dt[11:13]), minute = int(dt[14:16]), second = int(dt[17:19])
        )
        return utc_split + timedelta(hours=+9)





