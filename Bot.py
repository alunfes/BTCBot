from SystemFlg import SystemFlg
from MarketData import MarketData
from Account import Account
from Trade import Trade
import threading
import time


class Bot:
    @classmethod
    def kairi_trade(cls):
        md = MarketData('lightning_executions_','FX_BTC_JPY')



    @classmethod
    def order_and_cancel(cls):
        Trade.initialize()
        id = Trade.order('buy', 300000, 0.01, 1)
        print(id)
        for i in range(10):
            status = Trade.get_order_status(id)
            if len(str(status)) > 10:
                break
            time.sleep(0.3)
        Trade.cancel_order(id)

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


if __name__ == '__main__':
    #Bot.get_book()
    #Bot.get_position()
    #Bot.get_orders()
    Bot.order_and_cancel()

