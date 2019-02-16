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
    def order(cls, side, price, size, expire_m):
        order_id = cls.bf.create_order(
            symbol='BTC/JPY',
            type='limit',
            side=side,
            price=price,
            amount=size,
            params={'product_code': 'FX_BTC_JPY'}
            #params={'product_code': 'FX_BTC_JPY', 'minute_to_expire': expire_m}  # 期限切れまでの時間（分）（省略した場合は30日）
        )
        print('ok order'+str(order_id))
        return order_id

    @classmethod
    def get_order_status(cls, id):
        # orders = cls.bf.fetch_open_orders(symbol='BTC/JPY')
        res = ''
        try:
            res = cls.bf.private_get_getchildorders(params={'product_code': 'FX_BTC_JPY', 'child_order_acceptance_id': id})[0]
        except Exception as e:
            print(e)
        finally:
            print(res)
            return res

    @classmethod
    def get_orders(cls):
        orders = cls.bf.fetch_open_orders(symbol='BTC/JPY', params={"product_code": "FX_BTC_JPY"})
        for o in orders:
            print(o['id'])
        return orders

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


if __name__ == '__main__':
    Trade.initialize()
    id = Trade.order('buy',300000,0.01,1)
    Trade.get_order_status(id['id'])
    Trade.get_orders()
    Trade.cancel_order(id['id'])