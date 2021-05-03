import time

import ccxt
import pandas as pd
import Code.wechat as wechat
#  ======参数=======

ex = ccxt.binance()
wx = wechat.WeChat()

def filterUSDT(markets):
    lst = []
    for marketObj in markets:
        if '/USDT' in marketObj['symbol']:
            lst.append(marketObj['symbol'])
    return lst



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
            'symbol':symbol,
            'max': max,
            'last': last,
            'changeTime': '2021-1-1'
        }
        time.sleep(ex.rateLimit/1000)
    return symbols


# symbolList = filterUSDT(ex.fetch_markets())  # 所有的交易對
# symbols = updateMaxData(symbolList)

# df = pd.DataFrame(symbols).T
# df.to_csv('temp.csv',encoding='gbk',index=False)
df = pd.read_csv('temp.csv',encoding='gbk',index_col='symbol')

while True:
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
                info  = '歷史新高:' + k + ' ' + str(max) + ' ' + str(bid)
                wx.send_data(info)
                print(info)
    time.sleep(ex.rateLimit/1000)
    df.to_csv('temp.csv',encoding='gbk')


