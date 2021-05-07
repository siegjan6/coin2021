"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行

# 课程内容
遍历参数，查看每个参数的结果
"""
import pandas as pd
from datetime import timedelta
from Signals import *
from Position import *
from Evaluate import *
import talib
import matplotlib.pyplot as plt
import numpy as np

pd.set_option('display.max_rows', 1000)
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
# 设置命令行输出时的列对齐功能
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)

# =====参数设定
# 手工设定策略参数
symbol = 'BTC-USDT_5m'

face_value = 0.01  # btc是0.01，不同的币种要进行不同的替换
c_rate = 5 / 10000  # 手续费，commission fees，默认为万分之5。不同市场手续费的收取方法不同，对结果有影响。比如和股票就不一样。
slippage = 1 / 1000  # 滑点 ，可以用百分比，也可以用固定值。建议币圈用百分比，股票用固定值
leverage_rate = 3
min_margin_ratio = 1 / 100  # 最低保证金率，低于就会爆仓
rule_type = '15T'
drop_days = 10  # 币种刚刚上线10天内不交易

# =====读入数据
df = pd.read_hdf(r'C:\Users\jan\Documents\xingbuxing\coin2020\data\%s.h5' % symbol, key='df')
# 任何原始数据读入都进行一下排序、去重，以防万一
df.sort_values(by=['candle_begin_time'], inplace=True)
df.drop_duplicates(subset=['candle_begin_time'], inplace=True)
df.reset_index(inplace=True, drop=True)

# =====转换为其他分钟数据
rule_type = '12H'
period_df = df.resample(rule=rule_type, on='candle_begin_time', label='left', closed='left').agg(
    {'open': 'first',
     'high': 'max',
     'low': 'min',
     'close': 'last',
     'volume': 'sum',
     'quote_volume': 'sum',
     })
period_df.dropna(subset=['open'], inplace=True)  # 去除一天都没有交易的周期
period_df = period_df[period_df['volume'] > 0]  # 去除成交量为0的交易周期
period_df.reset_index(inplace=True)
df = period_df[['candle_begin_time', 'open', 'high', 'low', 'close', 'volume', 'quote_volume']]
dff = df[df['candle_begin_time'] >= pd.to_datetime('2021-01-10')]
dff.reset_index(inplace=True, drop=True)

para_list = []
for m in range(0, 30, 2):
    for n in range(0, 30, 2):
        for p in range(0, 21, 3):
            para = [m, n, p]
            para_list.append(para)
df_list = []
for para in para_list:
    df = dff.copy()
    if para[0] == para[1]: continue
    try:
        macd, signal, hist = talib.MACD(df['close'].values, fastperiod=para[0], slowperiod=para[1], signalperiod=para[2])
    except:
        continue
    print(para)
    df['signal'] = (macd - signal) > 0
    df['signal'] = df['signal'].astype('int')
    df['signal'].fillna(value='0', inplace=True)
    df = df[df['signal'] != df['signal'].shift()]

    df['pos'] = df['signal'].shift()
    df.dropna(how='any', inplace=True)

    df['start_time'] = df[df['pos'] == 1]['candle_begin_time']
    df['start_time'].fillna(method='ffill', inplace=True)
    df.dropna(how='any', inplace=True)
    df.drop(['signal'], inplace=True, axis=1)

    trade = pd.DataFrame()  # 计算结果放在trade变量中

    for _index, group in df.groupby('start_time'):
        if group.shape[0] <= 1:
            print(group)
            continue

        trade.loc[_index, 'start_time'] = group['start_time'].iloc[0]
        # trade.loc[_index, 'signal'] = group['pos'].iloc[0]

        g = group
        # 本次交易结束那根K线的开始时间
        trade.loc[_index, 'end_bar'] = group['candle_begin_time'].iloc[-1]  # g.iloc[-1]['candle_begin_time']
        # 开仓价格
        trade.loc[_index, 'start_price'] = g.iloc[0]['open']
        # 平仓信号的价格
        trade.loc[_index, 'end_price'] = g.iloc[-1]['close']

        group['equity_change'] = (g.iloc[-1]['close'] - g.iloc[0]['open']) / g.iloc[0]['open']
        group['equity_curve'] = (1 + group['equity_change']).cumprod()

        # 本次交易收益
        trade.loc[_index, 'change'] = (g.iloc[-1]['close'] - g.iloc[0]['open']) / g.iloc[0]['open']
        # 本次交易结束时资金曲线
        # trade.loc[_index, 'end_equity_curve'] = g.iloc[-1]['equity_curve']
        # # 本次交易中资金曲线最低值
        # trade.loc[_index, 'min_equity_curve'] = g['equity_curve'].min()

        trade['change'] = (1 + trade['change']).cumprod()
        trade['para'] = str(para)
        # trade.sort_values('change', inplace=True)
    df_list.append(trade.head(1))

df = pd.concat(df_list, ignore_index=True)
# df['candle_begin_time'] = pd.to_datetime(df['time'], unit='ms')  # 整理时间
# 去重、排序
# df.drop_duplicates(subset=['time'], keep='last', inplace=True)
df.sort_values('change', inplace=True)
df.reset_index(drop=True, inplace=True)
df.to_csv('test.csv', index=False)

# 画图
# fig = plt.figure(figsize=[18, 5])
# plt.plot(df.index, macd, label='macd dif')
# plt.plot(trade['start_time'], trade['end_equity_curve'], label='signal dea')
# plt.plot(trade['candle_begin_time'], hist, label='hist bar')
# plt.plot(df.index, mydif, label='my dif')
# plt.plot(df.index, mydea, label='my dea')
# plt.plot(df.index, mybar, label='my bar')
# plt.legend(loc='best')
# plt.show()
