from SystemFlg import SystemFlg
from MarketData import MarketData
from BTCData import BTCData
from Account import Account
from Trade import Trade
from IndexData import IndexData
import threading
import time
import copy


class Bot:
    @classmethod
    def pt_lc(cls, pt_side, pt_price, lc_price, size):
        def check_lc(side, lc_price) -> bool:
            price = BTCData.get_current_price()
            if side =='buy' and price <= lc_price:
                return True
            elif side =='sell' and price >= lc_price:
                return True
            else:
                return False

        remaining_size = copy.deepcopy(size)
        while True:
            if BTCData.get_current_price()
            Trade.order(pt_side, pt_price, remaining_size, 10)

    @classmethod
    def initialize(cls):
        Account.initialize()
        Trade.initialize()
        cls.pt_order = False
        cls.lc_order = False
        cls.entry_p = 0
        cls.order_id = ''
        cls.pt_id = ''
        cls.lc_id = ''


    @classmethod
    def kairi_trade(cls, kairi_kijun, pt, lc):
        md = MarketData('lightning_executions_','FX_BTC_JPY')
        Account.start()
        IndexData.start()

        cls.initialize()
        while SystemFlg.get_system_flg():
            kairi = 0
            if IndexData.get_ma_kairi() >= 1 + kairi_kijun:
                kairi = 1
            elif IndexData.get_ma_kairi() <= 1 - kairi_kijun:
                kairi = -1


    @classmethod
    def get_orders(cls):
        Trade.initialize()
        id = Trade.order('buy', 300000, 0.01, 1)
        id2 = Trade.order('buy', 300001, 0.01, 1)
        orders = ''
        while len(str(orders)) < 10:
            orders = Trade.get_orders()
            print(orders)
            time.sleep(0.1)
        Trade.cancel_all_orders()

    @classmethod
    def get_position(cls):
        Trade.initialize()
        print(Trade.get_positions())

    @classmethod
    def get_book(cls):
        Trade.initialize()
        print(Trade.get_order_book())

    @classmethod
    def order_and_get_open(cls):
        Trade.initialize()
        id = Trade.order('buy', 300000, 0.01, 1)
        for i in range(30):
            print('get_orders'+ str(len(Trade.get_orders())))
            #print('get all order'+Trade.get_all_orders())
            res = Trade.get_order_status(id)
            if res is not None:
                print(res['child_order_state'])
            else:
                print('none')
            print(str(0.5 * (i+1)))
            time.sleep(0.5)
        Trade.cancel_order(id)
        print('cencel')
        for i in range(30):
            print('get_orders' + str(len(Trade.get_orders())))
            # print('get all order'+Trade.get_all_orders())
            res = Trade.get_order_status(id)
            if res is not None:
                print(res['child_order_state'])
            else:
                print('none')
            print(str(0.5 * (i + 1)))
            time.sleep(0.5)



if __name__ == '__main__':
    Bot.order_and_get_open()
    #Bot.get_book()
    #Bot.get_position()
    #Bot.get_orders()
    #Bot.order_and_cancel()

