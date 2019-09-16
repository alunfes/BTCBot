import Bot
import WebsocketMaster
import SystemFlg
import time



class MasterThread:

    @classmethod
    def start_bot_trade(cls):
        SystemFlg.SystemFlg.initialize()
        Bot.Bot.initialize()
        Bot.Bot.kairi_contrian_trade(0.01)

    @classmethod
    def start_market_data(cls):
        SystemFlg.SystemFlg.initialize()
        md = WebsocketMaster.MarketData('lightning_executions_', 'FX_BTC_JPY')
        while True:
            time.sleep(1)



if __name__ == '__main__':
    MasterThread.start_market_data()