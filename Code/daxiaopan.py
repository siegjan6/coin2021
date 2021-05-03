import ccxt
from datetime import timedelta
import pandas as pd
import time
from base.Tool import *
import wechat

# print(ccxt.__version__)  # 检查ccxt版本，需要最新版本，1.44.21以上
wx = wechat.WeChat()
rule_type = '4h'
num = 20
bigSymbol = 'BTC/USDT'
smallSymbol = 'ETH/USDT'

ex = ccxt.binance()


def getMom(symbol):
    obj = ex.fetch_ohlcv(symbol, timeframe=rule_type, limit=num * 2)
    df = pd.DataFrame(obj, dtype=float)
    df['mom'] = df[4].pct_change(periods=num - 1)
    df[0] = pd.to_datetime(df[0], unit='ms') + timedelta(hours=8)  # 整理时间
    df = df.tail(2)
    df = df.head(1)
    return df

symbolList = [bigSymbol,smallSymbol]
dList = []
for symbol in symbolList:
    d = getMom(symbol)
    time.sleep(ex.rateLimit / 1000)
    dList.append([symbol, str(round(d['mom'].values[0], 5))])

df = pd.DataFrame(dList, columns=['symbol', 'mom'])
df.sort_values(by=['mom'], inplace=True)
df = df.tail(50)
dd = df.to_string()

wx.send_data(dd)



symbolList = filterUSDT(ex)
dList = []
for symbol in symbolList:
    d = getMom(symbol)
    time.sleep(0.5)
    dList.append([symbol, str(round(d['mom'].values[0], 5))])

df = pd.DataFrame(dList, columns=['symbol', 'mom'])
df.sort_values(by=['mom'], inplace=True)
df = df.tail(10)
dd = df.to_string()

wx.send_data(dd)
