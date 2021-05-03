import pandas as pd
import ccxt
import time
import datetime
from dateutil.relativedelta import relativedelta


# df['candle_begin_time_GMT8'] = pd.to_datetime(df['candle_begin_time'], unit='ms') + timedelta(hours=8)  # 北京时间
# df.drop(columns=['candle_begin_time'], inplace=True)
# df = df[['candle_begin_time_GMT8', 'open', 'high', 'low', 'close', 'volume']]

# print(df)


def updateSymbolData(ex, symbol, timeframe, startTime, endTime):
    dfList = []
    while startTime < endTime:
        data = ex.fetch_ohlcv(symbol, timeframe=timeframe, limit=2000, since=ex.parse8601(str(startTime)))
        df = pd.DataFrame(data, dtype=float)
        df['candle_begin_time'] = pd.to_datetime(df.iloc[:, 0], unit='ms')
        dfList.append(df)
        startTime = pd.to_datetime(df.iat[-1, 0], unit='ms')
        time.sleep(ex.rateLimit / 1000)
        print(startTime)
    df = pd.concat(dfList, ignore_index=True)
    df.rename(columns={0: 'MTS', 1: 'open', 2: 'high', 3: 'low', 4: 'close', 5: 'volume', 6: 'candle_begin_time'}, inplace=True)
    df = df[['candle_begin_time', 'open', 'high', 'low', 'close', 'volume']]
    df = df[df['candle_begin_time'] < endTime]
    df.sort_values('candle_begin_time', inplace=True)
    df.reset_index(drop=True,inplace=True)
    df.to_csv(symbol[:3] + timeframe + '.csv', index=False)


if __name__ == '__main__':
    pd.set_option('expand_frame_repr', False)
    pd.set_option('display.max_rows', 5000)
    exchange = ccxt.okex()

    # 计算 上一个整月时间
    now = datetime.datetime.now().date()
    startTime = datetime.datetime(now.year, now.month - 1, 1)
    endTime = datetime.datetime(now.year, now.month, 1)  # 小于结束时间

    for symbol in ['BTC/USDT']:
        updateSymbolData(exchange, symbol, '5m', startTime, endTime)
