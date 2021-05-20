# https://stockbuzzai.wordpress.com/2019/07/08/python%E5%9B%9E%E6%B8%AC%E6%A1%86%E6%9E%B6%EF%BC%88%E4%B8%80%EF%BC%89backtrader-%E4%BB%8B%E7%B4%B9/

# https://stockbuzzai.wordpress.com/category/%e4%b8%8d%e8%b2%a0%e8%b2%ac%e7%be%8e%e8%82%a1%e5%af%a6%e9%a9%97%e5%ae%a4/%e7%94%a8%e7%a8%8b%e5%bc%8f%e5%9b%9e%e6%b8%ac%e6%95%b8%e6%93%9a/
from datetime import datetime
import backtrader as bt
from dateutil.relativedelta import relativedelta


class TestStrategy(bt.Strategy):
    def __init__(self):
        self._next_buy_date = datetime(2010, 1, 5)

    def next(self):
        # print("self.data.datetime.date()"+str(self.data.datetime.date()))
        # print("self.data.datetime.date()1"+str(self._next_buy_date.date()))
        if self.data.datetime.date() >= self._next_buy_date.date():
            self._next_buy_date += relativedelta(months=1)
            self.buy(size=1)


data = bt.feeds.YahooFinanceData(dataname='MSFT',
                                 fromdate=datetime(2010, 1, 1),
                                 todate=datetime(2018, 12, 31))

cerebro = bt.Cerebro()
cerebro.adddata(data)
cerebro.addstrategy(TestStrategy)
cerebro.broker.set_cash(cash=10000)
cerebro.run()
cerebro.plot()
