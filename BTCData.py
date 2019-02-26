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
        cls.minutes_data = pd.DataFrame()
        cls.minutes_data.columns = ['dt', 'open', 'high', 'low', 'close', 'size']
        cls.lock_minutes_data = threading.Lock()
        cls.current_dt = None
        cls.next_dt = None
        cls.open = 0
        cls.high = 0
        cls.low = 0
        cls.close = 0
        cls.size = 0
        IndexData.IndexData.start(500)

    @classmethod
    def add_execution_data(cls, data):
        df = pd.DataFrame.from_dict(data)
        df['exec_date'] = df['exec_date'].map(cls.dt_converter)
        with cls.lock_minutes_data:
            if cls.current_dt == None:
                for i,d in enumerate(df['exec_date']):
                    if d.second == 0:
                        cls.current_dt = d
                        cls.next_dt =cls.current_dt + datetime.timedelta(minutes=1)
                        cls.open = df['price'][i]
                        print('current_dt has been defined, '+cls.current_dt)
            else:
                for i, d in enumerate(df['exec_date']):
                    if d >= cls.next_dt:
                        cls.close = df['price'][i]
                        cls.high = max(cls.high, df['price'][i])
                        cls.low = min(cls.low, df['price'][i])
                        cls.next_dt = cls.next_dt + datetime.timedelta(minutes=1)
                        cls.size += df['size'][i]
                        pd.DataFrame()
                        cls.minutes_data = pd.concat(cls.minutes_data, )
                    else:
                        cls.size += df['size'][i]
                        cls.high = max(cls.high, df['price'][i])
                        cls.low = min(cls.low, df['price'][i])


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





