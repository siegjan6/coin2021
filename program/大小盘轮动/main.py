import pandas as pd
import datetime
import ccxt
import time

# import talib
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', None)


def get_sma_diff(symbol, limit, timeframe):
    df = ex.fetch_ohlcv(symbol=symbol, timeframe=timeframe, limit=20)
    df = pd.DataFrame(df, dtype=float)
    df.rename(columns={0: 'candle_begin_time', 1: 'open', 2: 'high', 3: 'low', 4: 'close', 5: 'volume'}, inplace=True)
    # sma = signal_sma(df, limit)[-1]
    # sma = talib.SMA(df['close'].values, limit)[-1]
    sma = df['close'].mean()

    df['diff'] = df['close'].pct_change(19)
    # ret = (df.iat[-1, 4] - sma) / sma
    return df['diff'].values[-1]


def get_sma_diff_max(ex, symbols, timeframe, limit):
    """
    获取20日涨幅最大的币种
    """
    data = []
    for symbol in symbols:
        diff = get_sma_diff(symbol, limit, timeframe)
        data.append([symbol, diff])
    df = pd.DataFrame(data, dtype=float, columns=['symbol', 'diff'])
    df.sort_values(by='diff', inplace=True, ascending=False)
    df.reset_index(drop=True,inplace=True)
    print(df)
    if df.at[1, 'diff'] > 0:
        return df.head(1).values[0]
    print('所有币种均线低于20')
    return ''


def set_sell_all(df):
    for index, row in df.iterrows():
        symbol = row['asset'] + '/USDT'
        amout = row['free']
        p = ex.amount_to_precision(symbol=symbol, amount=amout)
        if float(p) <= 5:
            continue
        v = ex.create_market_order(symbol, 'SELL', amout)
        print(v)


def getUserInfo(ex):
    future_info = ex.fetch_balance()
    df = future_info['info']['balances']
    df = pd.DataFrame(df, dtype=float)
    df = df[df['free'] > 0.001]
    df = df[df['asset'] != 'USDT']
    df['asset'] = df['asset'] + '/USDT'
    df.reset_index(drop=True, inplace=True)
    return df


def getUserUSDT(ex):
    balance = ex.fetch_balance()
    hasUSDT = balance['USDT']['free']  # 目前剩余多少美金
    return hasUSDT


def main(ex, symbols, timeframe, limit):
    asset, free = get_sma_diff_max(ex, symbols, timeframe, limit)
    # 更新账户信息symbol_info
    df = getUserInfo(ex)  # 币
    if asset not in df['asset'].values:
        print(asset)
        print(df)
        exit()
        set_sell_all(df)
        time.sleep(3)
        usdt = getUserUSDT(ex)
        print(usdt)
        amount = usdt * 0.01 / free
        v = ex.create_market_order(asset, 'BUY', amount)
        print('下单买入' + asset)
        print(v)
    else:
        print('维持不动')


if __name__ == '__main__':
    ex = ccxt.binance()
    ex.apiKey = ''

    symbols = ['BTC/USDT', 'EOS/USDT', 'ETH/USDT', 'LINK/USDT']
    timeframe = '12h'
    limit = 20
    main(ex, symbols, timeframe, limit)
