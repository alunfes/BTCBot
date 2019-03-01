import pandas as pd
import threading
from datetime import datetime, timedelta
import IndexData
import copy
import time
import SystemFlg


#[{'id': 821682156, 'side': 'SELL', 'price': 395067.0, 'size': 0.015, 'exec_date': '2019-02-16T13:47:51.0022592Z', 'buy_child_order_acceptance_id': 'JRF20190216-134750-185055', 'sell_child_order_acceptance_id': 'JRF20190216-134748-681261'}
class BTCData:
    @classmethod
    def initialize(cls):
        cls.exes_list = []
        cls.exes_list_lock = threading.Lock()
        cls.high = 0
        cls.low = 99999999
        cls.size = 0
        cls.minutes_data = pd.DataFrame()

        cls.lock_ac = threading.Lock()
        cls.exes_for_account = pd.DataFrame()
        cls.lock_db = threading.Lock()
        cls.exes_for_db = pd.DataFrame()
        cls.minutes_data = pd.DataFrame()
        cls.lock_minutes_data = threading.Lock()
        cls.next_dt = None
        cls.minutes_tick = pd.DataFrame()
        cls.__start()
        IndexData.IndexData.start(3)

    @classmethod
    def __start(cls):
        th = threading.Thread(target=cls.minutes_data_converter)
        th.start()

    @classmethod
    def add_execution_data2(cls, data):
        with cls.exes_list_lock:
            for d in data:
                cls.exes_list.append(d)
                cls.high = max(cls.high, d['price'])
                cls.low = min(cls.low, d['price'])
                cls.size += d['size']

    @classmethod
    def minutes_data_converter(cls):
        while SystemFlg.SystemFlg.get_system_flg():
            if datetime.now().second == 0 and len(cls.exes_list) > 0:
                with cls.exes_list_lock:
                    sef = pd.DataFrame(pd.Series([datetime.now(),cls.exes_list[0]['price'], cls.high,cls.low, cls.exes_list[len(cls.exes_list)-1]['price'],
                                                  cls.size])).T
                    cls.exes_list = []
                    sef.columns = ['dt','open','high','low','close','size']
                    cls.minutes_data = pd.concat([cls.minutes_data, sef], ignore_index=True, axis=0)
                    cls.minutes_data.columns = ['dt','open','high','low','close','size']
                    print(cls.minutes_data)
                    cls.high = 0
                    cls.low = 99999999
                    cls.size = 0
                time.sleep(58)
            time.sleep(0.1)


    @classmethod
    def get_all_minutes_data(cls):
        with cls.exes_list_lock:
            res = copy.deepcopy(cls.minutes_data)
        return res

    @classmethod
    def get_latest_minutes_data(cls):
        with cls.exes_list_lock:
            res = copy.deepcopy(cls.minutes_data)
        return res[len(res)-1:len(res)]

    @classmethod
    def add_execution_data(cls, data): #1分間約定ない場合の対応検討
        df = pd.DataFrame.from_dict(data)
        df['exec_date'] = df['exec_date'].map(cls.dt_converter)
        '''
        with cls.lock_minutes_data:
            if cls.next_dt == None:
                for i,d in enumerate(df['exec_date']):
                    if d.second == 0:
                        cls.next_dt = d + timedelta(minutes=1)
                        cls.minutes_tick = df.iloc[i:i+1]
                        print('current_dt has been defined, '+str(cls.next_dt))
            else:
                for i, d in enumerate(df['exec_date']):
                    if d >= cls.next_dt:
                        cls.next_dt = cls.next_dt + timedelta(minutes=1)
                        se = pd.Series([d, cls.minutes_tick['price'][0], cls.minutes_tick['price'].max(), cls.minutes_tick['price'].min(),
                                        cls.minutes_tick['price'][len(cls.minutes_tick['price'])], cls.minutes_tick['size'].sum()])
                        cls.minutes_tick = pd.DataFrame()
                        cls.minutes_data.columns = ['dt','open','high','low','close']
                        d = cls.minutes_data.iloc[len(cls.minutes_data)-1:len(cls.minutes_data)]
                        #print('dt={}, open={}, high={}, low={}, close={}, size={}'.format(d, ))
                        print(cls.minutes_data[len(cls.minutes_data)-1:len(cls.minutes_data)])
                    else:
                        cls.minutes_tick = pd.concat([cls.minutes_tick, df.iloc[i:i+1]], axis=1, ignore_index=True)
        '''
        with cls.lock_ac:
            cls.exes_for_account = pd.concat([cls.exes_for_account, df], axis=0, ignore_index=True)
            print(cls.exes_for_account[len(cls.exes_for_account)-1:len(cls.exes_for_account)])
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
        with cls.exes_list_lock:
            if len(cls.exes_list) > 0:
                p = cls.exes_list[len(cls.exes_list)-1]['price']
                return p
            else:
                return None

    @classmethod
    def dt_converter(cls, dt):
        utc_split = datetime(
            year = int(dt[0:4]), month = int(dt[5:7]), day = int(dt[8:10]),
            hour = int(dt[11:13]), minute = int(dt[14:16]), second = int(dt[17:19])
        )
        return utc_split + timedelta(hours=+9)





