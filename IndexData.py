import threading
import time
import BTCData
from SystemFlg import SystemFlg


class IndexData:
    @classmethod
    def __initialize(cls, term): #term is secconds
        cls.lock = threading.Lock()
        cls.num = 0
        cls.ma = 0
        cls.ma_kairi = 0
        cls.term = term

    @classmethod
    def set_ma(cls,ma):
        with cls.lock:
            cls.ma = ma

    @classmethod
    def get_ma(cls):
        return cls.ma

    @classmethod
    def set_ma_kairi(cls, kairi):
        with cls.lock:
            cls.ma_kairi = kairi

    @classmethod
    def get_ma_kairi(cls):
        return cls.ma_kairi

    @classmethod
    def start(cls, term):
        cls.__initialize(term)
        th = threading.Thread(target = cls.main_loop)
        th.start()

    @classmethod
    def main_loop(cls):
        flg = True

        while flg: #loop for waiting enough num of tick data
            data = BTCData.BTCData.get_exes_for_db()
            if len(data) >= cls.term:
                flg = False
            else:
                time.sleep(1)

        while SystemFlg.get_system_flg(): #loop for calc of ma and kairi
            data = BTCData.BTCData.get_exes_for_db()['price']
            sum = data.loc[len(data) - cls.term : len(data)].sum()
            ma = float(sum) / float(cls.term)
            cls.set_ma(ma)
            cls.set_ma_kairi(data[len(data)-1] / ma)
