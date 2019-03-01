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
    def kairi_contrian_trade(cls, kairi_kijun):
        def check_kairi(kairi_kijun):
            if IndexData.get_ma_kairi() -1 >= kairi_kijun:
                return 'sell'
            elif 1 - IndexData.get_ma_kairi() <= kairi_kijun:
                return 'buy'
            else:
                return 'no'

        print('bot kairi_contrian_trade has been started')
        Trade.cancel_all_orders()
        time.sleep(3)
        while SystemFlg.get_system_flg():
            #check 1m kairi and entry if higher than kairi_kijun
            judge_side = check_kairi(kairi_kijun)
            if judge_side == 'sell' or judge_side == 'buy':
                cls.order_and_pt_lc(judge_side, BTCData.get_current_price(), 0.11, 1)
            posi = Trade.get_positions()
            if len(posi) > 0:
                print('unknown position is detected!')
                Trade.price_tracing_order('buy' if posi[0]['side'] == 'BUY' else 'sell', posi[0]['size'])
            time.sleep(3)

    @classmethod
    def order_and_pt_lc(cls, side, price, size, pt, lc, ptlc_trigger_width=50):
        print('order and pt lc started for '+side+' - '+str(price)+' x '+str(size)+'pt='+str(pt)+', lc='+str(lc))
        pt_price = price + pt if side =='buy' else price - pt
        lc_price = price - lc if side =='buy' else price + lc
        opposit_side = 'buy' if side =='sell' else 'sell'
        pt_id = ''
        #entry order
        order_id = Trade.order_wait_till_boarding(side, price, size, 100)
        time.sleep(3)
        ptlc = 'no'
        while True:
            #monitor pt lc price diff from current price, and do pt or lc when diff below ptlc_trigger
            order = Trade.get_order(order_id)
            if pt_id != '':
                pt_order = Trade.get_order(pt_id)
            if order[0]['info']['child_order_state'] != 'COMPLETED':
                ptlc = cls.__check_pt_lc(side, price, size, pt, lc, ptlc_trigger_width)
            else:
                ptlc = 'no'
            if ptlc =='pt' and order[0]['filled'] > 0:
                pt_id = Trade.order(opposit_side, pt_price, order[0]['filled'], 100)
                if order[0]['info']['child_order_state'] != 'COMPLETED':
                    Trade.cancel_and_wait_completion(order_id)
                print('lc started')
                Trade.price_tracing_order(opposit_side, order[0]['filled'])
                break
            elif pt_order[0]['info']['child_order_state'] == 'COMPLETED':
                print('pt completed at ' +str(pt_order[0]['info']['average_price']) + ' x '+str(pt_order['size']))
                break
            time.sleep(1)
        Trade.cancel_all_orders()

    @classmethod
    def __check_pt_lc(cls,side, entry_price, pt, lc, ptlc_trigger_width=50):
        pt_price = entry_price + pt if side == 'buy' else entry_price - pt
        lc_price = entry_price - lc if side == 'buy' else entry_price + lc
        if abs(BTCData.get_current_price() - pt_price) <= ptlc_trigger_width:
            return 'pt'
        elif abs(BTCData.get_current_price() - lc_price) <= ptlc_trigger_width:
            return 'lc'
        else:
            return 'no'


    @classmethod
    def pt_lc_till_execution(cls, pt_side, pt_price, lc_price, size):
        def check_lc(side, lc_price) -> bool:
            price = BTCData.get_current_price()
            if side =='buy' and price <= lc_price:
                return True
            elif side =='sell' and price >= lc_price:
                return True
            else:
                return False

        remaining_size = copy.deepcopy(size)
        side = 'buy' if pt_side == 'sell' else 'sell'
        oid = None
        while True:
            if check_lc(side, lc_price): #lc
                print('lc has been started, ' + pt_side + ':' + str(lc_price) + ' x ' + str(remaining_size))
                lc_price = Trade.price_tracing_order(side, remaining_size)
                print('lc has been completed')
                Trade.cancel_all_orders()
            else:
                if oid is None: #pt order
                    oid = Trade.order(pt_side, pt_price, remaining_size, 100)
                    print('placed pt order, ' + pt_side + ':' + str(pt_price) + ' x ' + str(remaining_size))
            time.sleep(1)

    @classmethod
    def test_check_data(cls):
        cls.initialize()
        i = 0
        while True:
            p = BTCData.get_current_price()
            ma = IndexData.get_ma()
            kairi = IndexData.get_ma_kairi()
            print('i={}, price={}, ma={}, kairi={}'.format(i,p,ma,kairi))
            i += 1
            time.sleep(0.1)


    @classmethod
    def initialize(cls):
        SystemFlg.initialize()
        #Account.initialize()
        Trade.initialize()
        md = MarketData('lightning_executions_', 'FX_BTC_JPY')
        #Account.start()
        cls.pt_order = False
        cls.lc_order = False
        cls.entry_p = 0
        cls.order_id = ''
        cls.pt_id = ''
        cls.lc_id = ''
        print('bot initialized')
        time.sleep(5)


    @classmethod
    def kairi_trade(cls, kairi_kijun, pt, lc):
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
    Bot.test_check_data()
    #Bot.get_book()
    #Bot.get_position()
    #Bot.get_orders()
    #Bot.order_and_cancel()

