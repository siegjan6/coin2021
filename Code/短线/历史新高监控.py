import time
import os,sys
import ccxt
import pandas as pd
sys.path.append('/root/coin2021')

import Code.wechat as wechat
import Code.base.Tool as Tool


#  ======参数=======

ex = ccxt.binance()
wx = wechat.WeChat()


def updateMaxData(symbolList):
    symbols = {}
    for symbol in symbolList:
        obj = ex.fetch_ohlcv(symbol, timeframe='1M')
        df = pd.DataFrame(obj, dtype=float)
        df[0] = pd.to_datetime(df[0], unit='ms')  # 整理时间
        max = df[2].max()
        print(symbol)
        last = df.iat[-1, 4]
        symbols[symbol] = {
            'symbol': symbol,
            'max': max,
            'last': last,
            'changeTime': '2021-1-1'
        }
        time.sleep(ex.rateLimit / 1000)
    return symbols


def read_csv(path="temp.csv"):
    if os.path.isfile(path):
        return pd.read_csv(path, encoding='gbk', index_col='symbol')
    symbols = updateMaxData(Tool.filterUSDT(ex))
    df = pd.DataFrame(symbols).T
    df.to_csv(path, encoding='gbk')
    return df


df = read_csv()
tickers = ex.fetch_tickers()
for k in tickers:
    if 'DOWN/' in k:
        continue
    if 'UP/' in k:
        continue
    if k in df.index.values:
        max = df.at[k, 'max']
        bid = tickers[k]['bid']
        df.loc[k, 'last'] = bid
        if bid > max:
            df.loc[k, 'max'] = bid
            df.loc[k, 'changeTime'] = pd.to_datetime(tickers[k]['timestamp'], unit='ms')
            info = '歷史新高:' + k + ' ' + str(max) + ' ' + str(bid)
            wx.send_data(info)
time.sleep(ex.rateLimit / 1000)
df.to_csv('temp.csv', encoding='gbk')
