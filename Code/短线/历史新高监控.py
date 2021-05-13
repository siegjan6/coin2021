import pandas as pd
import os, sys
import ccxt
import time
import datetime

if sys.platform != 'win32':
    sys.path.append('/root/coin2021')
import Code.base.Tool as tool
import Code.base.wechat as wechat
from Code.Function import *
from Code.config.configLoad import *
#  ======参数=======

wx = wechat.WeChat()


class CoinNewHighMgr:
    def __init__(self):
        self.ex = ccxt.binance()
        self.ex.apiKey = apiKey3266
        self.ex.secret = secret3266
        self.bias_pct = 0.01  # 低于这个阈值挂单
        if os.path.isfile('highPrice.csv'):
            self.df = pd.read_csv('highPrice.csv', encoding='gbk', index_col='symbol')
        else:
            self.df = self.onInitHighPrice(self.getSymbols())
            self.df.to_csv('highPrice.csv', encoding='gbk')

    def onInitHighPrice(self, symbolList):
        lst = []
        for symbol in symbolList:
            obj = self.ex.fetch_ohlcv(symbol, timeframe='3d', limit=1440)
            df = pd.DataFrame(obj, dtype=float)
            df[0] = pd.to_datetime(df[0], unit='ms')  # 整理时间
            max = df[2].max()
            last = df.iat[-1, 4]
            df.sort_values(by=[2], inplace=True)
            maxTime = df.iat[-1, 0]
            lst.append([symbol, max, maxTime])
            time.sleep(.3)
        df = pd.DataFrame(lst, columns=['symbol', 'max', 'maxTime'])
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
            if symbol in self.df.index.values:
                dfMax = self.df.at[symbol, 'max']
                dfMaxTime = self.df.at[symbol, 'maxTime']
                dfMaxTime = pd.to_datetime(dfMaxTime)
                dff = pd.to_datetime(obj['timestamp'], unit='ms') - dfMaxTime
                # dff = dff.days()  # 天差
                if bid > dfMax:
                    self.df.loc[symbol, 'max'] = bid
                    self.df.loc[symbol, 'maxTime'] = pd.to_datetime(obj['timestamp'], unit='ms')
                    self.df.to_csv('highPrice.csv', encoding='gbk')
                    if dff.days > 2:
                        self.onHighPrice(obj, dff.days)
            else:  # 新币 暂不处理
                print(symbol)
                self.df.loc[symbol, 'max'] = bid
                self.df.loc[symbol, 'maxTime'] = pd.to_datetime(obj['timestamp'], unit='ms')
                self.df.to_csv('highPrice.csv', encoding='gbk')

    def onHighPrice(self, obj, dff):
        symbol = obj['symbol']
        bid = obj['bid']
        price = obj['ask'] * 1.02
        spot_amount = 1000 / obj['ask']
        # spot_order_info = binance_spot_place_order(exchange=self.ex, symbol=symbol, long_or_short='买入',price=price , amount=spot_amount)
        data = symbol + ' ' + dff + '天后突破新高' + '\n' + bid
        wx.send_data(data)

    # 挂单
    def onOrder(self, symbol, price):
        print(symbol, price, datetime.datetime.now())

    def run(self):
        # 撤单
        # 扫描 - 挂单
        # 查询订单成交情况
        pass


engine = CoinNewHighMgr()
engine.updateData()
