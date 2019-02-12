class OrderData:
    def __init__(self):
        self.orders = {}

    def add_order(self, id, status, dt, side, price, size):
        val = OrderDictVal(status, dt, side, price, size)
        self.orders[id] = val

    def remove_order(self, id):
        del self.orders[id]

    def get_all_ids(self):
        return self.orders.keys()

class OrderDictVal:
    def __init__(self, status, dt, side, price, size):
        self.order_status = ''
        self.order_dt = ''
        self.order_side = ''
        self.order_price = 0
        self.order_size = 0