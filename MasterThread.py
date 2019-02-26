import Bot
import MarketData
import SystemFlg



class MasterThread:

    @classmethod
    def start_bot_trade(cls):
        SystemFlg.SystemFlg.initialize()
        md = MarketData.MarketData('lightning_executions_','FX_BTC_JPY')

