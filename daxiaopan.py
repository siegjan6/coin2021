import ccxt                                                                                                
from datetime import timedelta
import pandas as pd
import wechat
print(ccxt.__version__)  # 检查ccxt版本，需要最新版本，1.44.21以上
wx = wechat.WeChat()
rule_type = '4h'
num = 20
bigSymbol = 'BTC/USDT'
smallSymbol = 'ETH/USDT'

ex = ccxt.binance()

def getMom(symbol):
    obj = ex.fetch_ohlcv(symbol,timeframe=rule_type,limit=num*2)
    df = pd.DataFrame(obj, dtype=float)
    df['mom'] = df[4].pct_change(periods=num -1) 
    df[0] = pd.to_datetime(df[0], unit='ms') + timedelta(hours=8) # 整理时间
    df = df.tail(2)
    df = df.head(1)
    return df

d1 = getMom(bigSymbol)
d2 = getMom(smallSymbol)
data = bigSymbol + ' ' + str(round(d1['mom'].values[0],5)) + '\n' + smallSymbol + ' ' + str(round(d2['mom'].values[0],5)) + '\n'  
print(data)
wx.send_data(data)
print('end')
