from datetime import datetime
from dateutil.relativedelta import relativedelta
import backtrader
import math


class TestStrategy(backtrader.Strategy):
    def __init__(self):
        # 設定入金日期 記錄用
        self._last_deposit_date = datetime(2010, 1, 5)
        # 設定入金後實際購買日期
        self._last_buy_date = datetime(2010, 1, 7)

    def next(self):
        # 今日日期
        current_date = self.data.datetime.date()
        # 如果今日日期 大於等於 上次紀錄的入金日期
        if current_date >= self._last_deposit_date.date():
            self._last_deposit_date += relativedelta(months=1)
            self._last_buy_date = datetime.combine(
                date=current_date, time=datetime.min.time()) + relativedelta(days=3)
            self.broker.add_cash(cash=300)
        # 如果今日日期 大於等於 上次購買日期
        if current_date >= self._last_buy_date.date():
            print("hight:" + str(self.data.high))
            print("low:" + str(self.data.low))

            # 我們使用當日最高價（self.data.high）和最低價（self.data.low）的平均來計算要買的價
            price = (self.data.high + self.data.low) / 2.0
            print("price:"+str(price))
            # 要算出要買的量 用要投資的現金(1)除均價就是要買的量
            volume = math.floor((self.broker.cash) / price)
            self.buy(size=volume)
            self._last_buy_date += relativedelta(months=1)


# 查詢資料源
cerebro = backtrader.Cerebro()
data = backtrader.feeds.YahooFinanceData(dataname='MSFT',
                                         fromdate=datetime(2010, 1, 1),
                                         todate=datetime(2018, 12, 31))


cerebro.adddata(data)
cerebro.addstrategy(TestStrategy)
cerebro.broker.set_cash(cash=1)
cerebro.run()
cerebro.plot()
