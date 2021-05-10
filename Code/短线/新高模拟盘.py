import pandas as pd
import ccxt
import time
import datetime


import os,sys
if sys.platform != 'win32':
    sys.path.append('/root/coin2021')
import Code.base.Tool as tool
import Code.base.wechat as wechat

#  ======参数=======

wx = wechat.WeChat()


class CoinNewHighMgr:
    def __init__(self):
        self.ex = ccxt.binance()
        self.bias_pct = 0.01  # 低于这个阈值挂单
        self.df = self.onInitHighPrice()

    def onInitHighPrice(self):
        lst = []
        symbolList = self.getSymbols()
        for symbol in symbolList:
            obj = self.ex.fetch_ohlcv(symbol, timeframe='1M')
            df = pd.DataFrame(obj, dtype=float)
            df[0] = pd.to_datetime(df[0], unit='ms')  # 整理时间
            max = df[2].max()
            last = df.iat[-1, 4]
            lst.append([symbol, max, last])
            time.sleep(.3)
        df = pd.DataFrame(lst, columns=['symbol', 'max', 'last'])
        df.set_index('symbol', inplace=True)
        return df

    def getSymbols(self):
        tickers = self.ex.fetch_tickers()
        lst = []
        for k in tickers:
            if 'DOWN/' in k:
                continue
            if 'UP/' in k:
                continue
            if not k.endswith('/USDT'):
                continue
            lst.append(k)
        return lst

    def fetch_tickers(self):
        try:
            tickers = self.ex.fetch_tickers()
            lst = []
            for k in tickers:
                if 'DOWN/' in k:
                    continue
                if 'UP/' in k:
                    continue
                if not k.endswith('/USDT'):
                    continue
                lst.append(tickers[k])
            return lst
        except:
            return []


    """
        'symbol': 'BTC/USDT',
        'timestamp': 1620101863798,
        'datetime': '2021-05-04T04:17:43.798Z',
        'high': 58981.44,
        'low': 54580.0,
        'bid': 55625.97,
        'bidVolume': 0.468416,
        'ask': 55625.98,
        'askVolume': 4.742734,
        'vwap': 57333.33426434,
        'open': 57972.04,
        'close': 55625.98,
        'last': 55625.98,
        'previousClose': 57972.05,
        'change': -2346.06,
        'percentage': -4.047,
        'average': None,
        'baseVolume': 65863.538062,
        'quoteVolume': 3776176243.540664,"""

    def updateData(self):
        tickers = self.fetch_tickers()
        for obj in tickers:
            symbol = obj['symbol']
            bid = obj['bid']
            dfMax = self.df.at[symbol, 'max']
            if symbol in self.df.index.values:
                if bid > dfMax:
                    self.df.loc[symbol, 'max'] = bid
                    self.df.loc[symbol, 'changeTime'] = pd.to_datetime(obj['timestamp'], unit='ms')
                    self.onHighPrice(obj)
            else:  # 新币 暂不处理
                pass

    def onHighPrice(self, obj):
        path = 'highPrice.csv'
        dd = pd.DataFrame(columns=['symbol', 'bidPrice', 'dateTime'])
        dd.set_index('symbol', inplace=True)
        if os.path.isfile(path):
            dd = pd.read_csv(path, encoding='gbk', index_col='symbol')
        # if obj['symbol'] in dd.index.values: #新高触发过就  忽略
        #     pass
        # else:
        dd.loc[obj['symbol']] = [obj['bid'], pd.to_datetime(obj['timestamp'], unit='ms')]
        dd.to_csv(path, encoding='gbk')
        wx.send_data(dd.to_string())

    # 挂单
    def onOrder(self, symbol, price):
        print(symbol, price, datetime.datetime.now())
        

    def run(self):
        # 撤单
        # 扫描 - 挂单
        # 查询订单成交情况
        pass


engine = CoinNewHighMgr()
while True:
    engine.updateData()
    time.sleep(10)

