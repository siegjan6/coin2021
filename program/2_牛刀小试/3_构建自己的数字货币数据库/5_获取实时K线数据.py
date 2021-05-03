"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行

# 课程内容
通过获取实时K线数据，进一步讲解ccxt的用法
"""
import pandas as pd
import ccxt
from datetime import timedelta
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行


# =====创建ccxt交易所
exchange = ccxt.okex3()  # huobipro, binance, okex3


# =====设定参数
symbol = 'BTC/USDT'
time_interval = '5m'  # 其他可以尝试的值：'1m', '5m', '15m', '30m', '1h', '2h', '1d', '1w', '1M', '1y'，并不是每个交易所都支持
bar_num = 100  # 获取K线的数量


# =====获取最新数据
data = exchange.fetch_ohlcv(symbol=symbol, timeframe=time_interval, limit=bar_num)


# =====整理数据
df = pd.DataFrame(data, dtype=float)  # 将数据转换为dataframe
df.rename(columns={0: 'MTS', 1: 'open', 2: 'high',
                   3: 'low', 4: 'close', 5: 'volume'}, inplace=True)  # 重命名
df['candle_begin_time'] = pd.to_datetime(df['MTS'], unit='ms')  # 整理时间
df['candle_begin_time_GMT8'] = df['candle_begin_time'] + timedelta(hours=8)  # 北京时间
df = df[['candle_begin_time_GMT8', 'open', 'high', 'low', 'close', 'volume']]  # 整理列的顺序
print(df)


# =====注意点
# 这个数据之后就可以直接使用，用来计算策略信号

# bar_num不可无限大，每个交易所有自己的单次获取K线的限制，例如okex每次最多200，火币2000，币安1000，可以自己多尝试或者查看官方文档

# 当某根K线所在时间没有交易时，会保留k线数据，但是成交量为0。但不是绝对的，需要自己考察。okex MCO/USDT，火币UUU/USDT

# 当该区间段第一笔交易产生的时候，k线才会生成。


