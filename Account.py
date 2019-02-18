from BTCData import BTCData
from SystemFlg import SystemFlg
import threading
import pandas as pd


class Account:
    @classmethod
    def initialize(cls):
        cls.lock = threading.Lock()f

        cls.order_side = []
        cls.order_id = []
        cls.order_price = []
        cls.order_size = []
        cls.order_dt = []
        cls.order_expire_dt = []
        cls.order_status = [] #ordering, cancelling
        cls.order_memo = [] #memo for info used in Bot, pt, lc, entry
        cls.order_log = {} #id, status

        '''
        cls.position_price = []
        cls.position_size = []
        cls.position_dt = []
        cls.position_id = []
        '''

        cls.ave_position_side = 'None' #buy, sell
        cls.ave_position_price = 0
        cls.ave_position_size = 0

        #cls.money = 0
        cls.total_asset = 0

        cls.num_trade = 0
        cls.total_pl = 0
        cls.total_pl_log = []
        cls.win_ratio = 0
        cls.num_win = 0
        cls.unrealized_pl = 0

    @classmethod
    def get_orders(cls):
        with cls.lock:
            return {'order_side':cls.order_side, 'order_id':cls.order_id, 'order_price':cls.order_price, 'order_size':cls.order_size,
                    'order_dt':cls.order_dt, 'order_expire_dt':cls.order_expire_dt, 'order_status':cls.order_status}
    @classmethod
    def add_order(cls, oid, side, price, size, dt, expire_dt, memo):
        with cls.lock:
            cls.order_side.append(side)
            cls.order_price.append(price)
            cls.order_size.append(round(size,2))
            cls.order_dt.append(dt)
            cls.order_expire_dt.append(expire_dt)
            cls.order_status.append('ordering')
            cls.order_memo.append(memo)
            cls.order_log[oid] = 'ordering'

    @classmethod
    def __remove_order(cls, ind):
        with cls.lock:
            cls.order_id.pop(ind)
            cls.order_side.pop(ind)
            cls.order_status.pop(ind)
            cls.order_expire_dt.pop(ind)
            cls.order_dt.pop(ind)
            cls.order_price.pop(ind)
            cls.order_size.pop(ind)
            cls.order_memo.pop(ind)

    @classmethod
    def cancel_order(cls, ind, dt):
        with cls.lock:
            cls.order_status[ind] = 'cancelling'
            cls.order_dt[ind] = dt

    @classmethod
    def get_positions(cls):
        return {'ave_position_side':cls.ave_position_side, 'ave_position_price':cls.ave_position_price, 'ave_position_size':cls.ave_position_size}

    '''
    @classmethod
    def __check_order_expiration(cls):


    @classmethod
    def add_position(cls, side, price, size, dt, id):
        with cls.lock:
    '''

    @classmethod
    def start(cls, ccxt_bf):
        cls.initialize(ccxt_bf)
        th = threading.Thread(target = cls.main_loop)
        th.start()

    @classmethod
    def main_loop(cls):
        while SystemFlg.get_system_flg():
            cls.__check_execution()
            cls.__check_order_cancellation()
            cls.__calc_pl_unrealized()

    @classmethod
    def __check_execution(cls):
        exes = BTCData.get_exes_for_account()
        orders = cls.get_orders()
        oids = orders['order_id']
        osides = orders['order_side']
        for i, oid in enumerate(oids):
            df_extract = pd.DataFrame()
            if osides[i] == 'buy':
                df_extract  = exes[exes['buy_child_order_acceptance_id']==oid].reset_index()
            elif osides[i] == 'sell':
                df_extract = exes[exes['sell_child_order_acceptance_id'] == oid].reset_index()
            if len(df_extract) > 0:
                cls.__execution(orders['order_size'][i], orders['order_price'][i], osides[i], oid, i, df_extract)

    @classmethod
    def __execution(cls, order_size, order_price, order_side, order_id, order_ind, exe_df):
        sum_size = exe_df['size'].sum()
        ndf = exe_df['price'] * exe_df['size']
        ave_p = ndf.sum() / float(len(ndf))
        print('executed ' + order_side + ' ' + str(ave_p) + ' x ' + str(sum_size))
        cls.__remove_order(order_ind)
        if cls.ave_position_side == 'None':
            cls.__update_position(order_side, ave_p, sum_size, order_id)

    @classmethod
    def __calc_pl_exec(cls, side, price, size):
        pre = cls.total_pl
        pl = 0
        if cls.ave_position_side == 'buy' and side == 'sell':
            pl = (price - cls.ave_position_price) * size
        elif cls.ave_position_side == 'sell' and side == 'buy':
            pl =(cls.ave_position_price - price) * size
        cls.total_pl_log.append(pl - pre)
        cls.total_pl +=pl
        cls.num_win += 1 if pl >0 else 0
        cls.win_ratio = float(cls.num_win) / float(cls.num_trade)


    @classmethod
    def __calc_pl_unrealized(cls):
        price = BTCData.get_latest_exes_for_db()['price']
        if cls.ave_position_side == 'buy':
            cls.unrealized_pl = (price - cls.ave_position_price) * cls.ave_position_size
        elif cls.ave_position_side == 'sell':
            cls.unrealized_pl = (cls.ave_position_price - price) * cls.ave_position_size
        else:
            cls.unrealized_pl = 0

    @classmethod
    def get_executions(cls):
        print('')

    @classmethod
    def __update_position(cls,side,price,size,dt,id):
        if cls.ave_position_side == 'None':
            cls.add_position(side, price, size, dt, id)
        elif cls.ave_position_side == side:
            cls.ave_position_price = (cls.ave_position_price * cls.ave_position_size + price * size) / (cls.ave_position_size + size)
            cls.ave_position_size += size
        elif cls.ave_position_side != side:
            cls.__calc_pl_exec(side, price, size)
            if cls.ave_position_size > size:
                cls.ave_position_size -= size
            elif cls.ave_position_size == size:
                cls.ave_position_side = 'None'
                cls.ave_position_size = 0
                cls.ave_position_price = 0
            elif cls.ave_position_size < size:
                cls.ave_position_side = side
                cls.ave_position_size = size - cls.ave_position_size
                cls.ave_position_price = price
        print('current position = ' + cls.ave_position_side + ' '+str(cls.ave_position_price) + ' x '+str(cls.ave_position_size))

    @classmethod
    def __check_order_cancellation(cls):
        with cls.lock:
            for i,status in enumerate(cls.order_status):
                if status == 'cancelling':
                    print('')

