import ccxt
from Account import Account


class Trade:
    @classmethod
    def initialize(cls):
        cls.secret_key=''
        cls.api_key = ''
        cls.__read_keys()
        cls.bf = ccxt.bitflyer({
            'apiKey': cls.api_key,
            'secret': cls.secret_key,
        })
        #print(cls.bf.fetch_trades(symbol='BTC/JPY', limit=2))
        #print(cls.bf.fetch_balance())
        #print(cls.bf.has)
        cls.order_id = {}

    @classmethod
    def __read_keys(cls):
        file = open('ex.txt', 'r')  # 読み込みモードでオープン
        cls.secret_key = file.readline().split(':')[1]
        cls.secret_key = cls.secret_key[:len(cls.secret_key)-1]
        cls.api_key = file.readline().split(':')[1]
        cls.api_key = cls.api_key[:len(cls.api_key)-1]
        file.close()


    @classmethod
    def order(cls, side, price, size, expire_m): #min size is 0.01
        order_id = cls.bf.create_order(
            symbol='BTC/JPY',
            type='limit',
            side=side,
            price=price,
            amount=size,
            params={'product_code': 'FX_BTC_JPY'}
            #params={'product_code': 'FX_BTC_JPY', 'minute_to_expire': expire_m}  # 期限切れまでの時間（分）（省略した場合は30日）
        )['info']['child_order_acceptance_id']
        print('ok order'+str(order_id))
        return order_id

    @classmethod
    def get_order_status(cls, id): #{'id': 0, 'child_order_id': 'JFX20190216-151959-489658F', 'product_code': 'FX_BTC_JPY', 'side': 'BUY', 'child_order_type': 'LIMIT', 'price': 300000.0, 'average_price': 0.0, 'size': 0.01, 'child_order_state': 'ACTIVE', 'expire_date': '2019-03-18T15:19:59', 'child_order_date': '2019-02-16T15:19:59', 'child_order_acceptance_id': 'JRF20190216-151959-561199', 'outstanding_size': 0.01, 'cancel_size': 0.0, 'executed_size': 0.0, 'total_commission': 0.0}
        res = None
        try:
            res = cls.bf.private_get_getchildorders(params={'product_code': 'FX_BTC_JPY', 'child_order_acceptance_id': id})[0]
        except Exception as e:
            print('error in get_order_status ' + e)
        finally:
            return res

    @classmethod
    def get_orders(cls): #[{'id': 'JRF20190216-152736-108492', 'info': {'id': 0, 'child_order_id': 'JFX20190216-152736-105655F', 'product_code': 'FX_BTC_JPY', 'side': 'BUY', 'child_order_type': 'LIMIT', 'price': 300001.0, 'average_price': 0.0, 'size': 0.01, 'child_order_state': 'ACTIVE', 'expire_date': '2019-03-18T15:27:36', 'child_order_date': '2019-02-16T15:27:36', 'child_order_acceptance_id': 'JRF20190216-152736-108492', 'outstanding_size': 0.01, 'cancel_size': 0.0, 'executed_size': 0.0, 'total_commission': 0.0}, 'timestamp': 1550330856000, 'datetime': '2019-02-16T15:27:36.000Z', 'lastTradeTimestamp': None, 'status': 'open', 'symbol': 'BTC/JPY', 'type': 'limit', 'side': 'buy', 'price': 300001.0, 'cost': 0.0, 'amount': 0.01, 'filled': 0.0, 'remaining': 0.01, 'fee': {'cost': 0.0, 'currency': None, 'rate': None}}, {'id': 'JRF20190216-152736-643929', 'info': {'id': 0, 'child_order_id': 'JFX20190216-152736-105514F', 'product_code': 'FX_BTC_JPY', 'side': 'BUY', 'child_order_type': 'LIMIT', 'price': 300000.0, 'average_price': 0.0, 'size': 0.01, 'child_order_state': 'ACTIVE', 'expire_date': '2019-03-18T15:27:36', 'child_order_date': '2019-02-16T15:27:36', 'child_order_acceptance_id': 'JRF20190216-152736-643929', 'outstanding_size': 0.01, 'cancel_size': 0.0, 'executed_size': 0.0, 'total_commission': 0.0}, 'timestamp': 1550330856000, 'datetime': '2019-02-16T15:27:36.000Z', 'lastTradeTimestamp': None, 'status': 'open', 'symbol': 'BTC/JPY', 'type': 'limit', 'side': 'buy', 'price': 300000.0, 'cost': 0.0, 'amount': 0.01, 'filled': 0.0, 'remaining': 0.01, 'fee': {'cost': 0.0, 'currency': None, 'rate': None}}]
        orders = cls.bf.fetch_open_orders(symbol='BTC/JPY', params={"product_code": "FX_BTC_JPY"})
        #for o in orders:
        #    print(o['id'])
        return orders

    @classmethod
    def get_all_orders(cls):
        return cls.bf.fetch_open_order(symbol='BTC/JPY', params={"product_code": "FX_BTC_JPY"})

    @classmethod
    def get_positions(cls): #None
        positions = cls.bf.private_get_getpositions( params = { "product_code" : "FX_BTC_JPY" })

    @classmethod
    def cancel_order(cls, order_id):
        try:
            res = cls.bf.cancel_order(id=order_id, symbol='BTC/JPY', params={"product_code": "FX_BTC_JPY"})
        except Exception as e:
            print(e)

    @classmethod
    def cancel_all_orders(cls):
        orders = cls.get_orders()
        for o in orders:
            cls.cancel_order(o['id'])

    @classmethod
    def price_tracing_order(cls, side, size):
        order_p = 0
        while size > 0:
            print('')
            book = cls.get_order_book()
            order_id = ''
            if side == 'buy':
                best_p = book['bids'][0]
                if order_p <= best_p:
                    cls.cancel_order(order_id)
                    order_p = best_p + 1
            elif side == 'sell':
                book['bids'][0]


            #get best price
            #update order price
            #check execution

    @classmethod
    def get_order_book(cls): #{'bids': [[394027.0, 0.15], [394022.0, 0.01], [394020.0, 3.22357434], [394018.0, 0.02050665], [394016.0, 0.085], [394015.0, 0.02], [394014.0, 0.025], [394013.0, 0.21195378], [394012.0, 1.67], [394011.0, 1.36], [394010.0, 0.395], [394009.0, 0.01], [394008.0, 0.021], [394007.0, 0.09018275], [394006.0, 1.4862514], [394005.0, 6.42], [394004.0, 0.79593158], [394003.0, 5.0], [394002.0, 0.34592307], [394001.0, 4.14846844], [394000.0, 173.92494563], [393999.0, 0.01], [393998.0, 0.55], [393997.0, 0.484], [393996.0,
        return cls.bf.fetch_order_book(symbol='BTC/JPY', params={"product_code": "FX_BTC_JPY"})



if __name__ == '__main__':
    Trade.initialize()
    id = Trade.order('buy',300000,0.01,1)
    Trade.get_order_status(id)
    Trade.get_orders()
    Trade.cancel_order(id)
