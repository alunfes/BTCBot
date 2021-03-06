import websocket
import threading
import time
import json
from BTCData import BTCData
import pandas as pd
import asyncio

class MarketData:
    def __init__(self, channel, symbol):
        self.symbol = symbol
        self.ticker = None
        self.channel = channel
        self.connect()
        self.df = pd.DataFrame()
        BTCData.initialize()

    def connect(self):
        self.ws = websocket.WebSocketApp(
            'wss://ws.lightstream.bitflyer.com/json-rpc', header=None,
            on_open = self.on_open, on_message = self.on_message,
            on_error = self.on_error, on_close = self.on_close)
        self.ws.keep_running = True 
        websocket.enableTrace(True)
        self.thread = threading.Thread(target=lambda: self.ws.run_forever())
        self.thread.daemon = True
        self.thread.start()

    def is_connected(self):
        return self.ws.sock and self.ws.sock.connected

    def disconnect(self):
        print('disconnected')
        self.ws.keep_running = False
        self.ws.close()

    def get(self):
        return self.ticker

    def on_message(self, ws, message):
        message = json.loads(message)['params']
        self.ticker = message['message']
        if self.ticker is not None:
            BTCData.add_execution_data(self.ticker) #[{'id': 821682156, 'side': 'SELL', 'price': 395067.0, 'size': 0.015, 'exec_date': '2019-02-16T13:47:51.0022592Z', 'buy_child_order_acceptance_id': 'JRF20190216-134750-185055', 'sell_child_order_acceptance_id': 'JRF20190216-134748-681261'}

    def on_error(self, ws, error):
        print('error')
        self.disconnect()
        time.sleep(3)
        self.connect()

    def on_close(self, ws):
        print('Websocket disconnected')

    def on_open(self, ws):
        ws.send(json.dumps( {'method':'subscribe',
            'params':{'channel':self.channel + self.symbol}} ))
        time.sleep(1)
        print('Websocket connected')

    async def loop(self):
        while True:
            await asyncio.sleep(1)


if __name__ == '__main__':

    md = MarketData('lightning_executions_','FX_BTC_JPY')
    num_failed = 0
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(md.loop())
    loop.run_forever()

    #md.disconnect()