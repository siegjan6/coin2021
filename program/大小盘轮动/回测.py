"""
在此之前需要行情数据，备份
回测大小盘（BTC、ETH）
"""
import pandas as pd
from Tool import *
pd.set_option('display.max_rows', 1000)
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
# 设置命令行输出时的列对齐功能
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)


# ==========整理出历史数据、转换4小时数据============
btcDf = getSymbolData('BTC-USDT_5m')
ethDf = getSymbolData('ETH-USDT_5m')
print(btcDf)
# btcDf['mean120'] = btcDf['close'].rolling(120, min_periods=1).mean()
btcDf['mean120'] = btcDf['close'].pct_change(periods=120)
btcDf['next_open'] = btcDf['open'].shift(-1)  # 下根K线的开盘价
btcDf['next_open'].fillna(value=btcDf['close'], inplace=True)
btcDf = btcDf.loc[120:]
# ethDf['mean120'] = ethDf['close'].rolling(120, min_periods=1).mean()
ethDf['mean120'] = ethDf['close'].pct_change(periods=120)
ethDf['next_open'] = ethDf['open'].shift(-1)  # 下根K线的开盘价
ethDf['next_open'].fillna(value=ethDf['close'], inplace=True)
ethDf = ethDf.loc[120:]
# =====两个df左右合并操作，merge操作
df_merged = pd.merge(left=btcDf, right=ethDf, left_on='candle_begin_time', right_on='candle_begin_time',
                     suffixes=['_btc', '_eth'])
# 计算信号
df_merged.loc[df_merged['mean120_btc'] > df_merged['mean120_eth'], 'signal'] = 1
df_merged.loc[df_merged['mean120_btc'] > df_merged['mean120_eth'], 'open'] = df_merged['open_btc']
df_merged.loc[df_merged['mean120_btc'] > df_merged['mean120_eth'], 'close'] = df_merged['close_btc']
df_merged.loc[df_merged['mean120_eth'] > df_merged['mean120_btc'], 'signal'] = 2
df_merged.loc[df_merged['mean120_eth'] > df_merged['mean120_btc'], 'open'] = df_merged['open_eth']
df_merged.loc[df_merged['mean120_eth'] > df_merged['mean120_btc'], 'close'] = df_merged['close_eth']
df_merged['pctChange'] = (df_merged['close'] - df_merged['open']) / df_merged['open']
df_merged['next_open'] = df_merged['open'].shift(-1)  # 下根K线的开盘价
df_merged['next_open'].fillna(value=df_merged['close'], inplace=True)

condition1 = df_merged['mean120_btc'] < 0
condition2 = df_merged['mean120_eth'] < 0
df_merged.loc[condition1 & condition2, 'signal'] = 0
# 计算POS
df_merged['pos'] = df_merged['signal'].shift()
df_merged['pos'].fillna(value=0, inplace=True)  # 将初始行数的pos补全为0
df_merged.drop(['signal'], axis=1, inplace=True)

# =====找出开仓、平仓的k线
condition1 = df_merged['pos'] != 0  # 当前周期不为空仓
condition2 = df_merged['pos'] != df_merged['pos'].shift(1)  # 当前周期和上个周期持仓方向不一样。
open_pos_condition = condition1 & condition2

condition1 = df_merged['pos'] != 0  # 当前周期不为空仓
condition2 = df_merged['pos'] != df_merged['pos'].shift(-1)  # 当前周期和下个周期持仓方向不一样。
close_pos_condition = condition1 & condition2

# =====对每次交易进行分组
df_merged.loc[open_pos_condition, 'start_time'] = df_merged['candle_begin_time']
df_merged['start_time'].fillna(method='ffill', inplace=True)
df_merged.loc[df_merged['pos'] == 0, 'start_time'] = pd.NaT

df = df_merged.loc[close_pos_condition]
df['equity_curve'] = (1 + df['pctChange']).cumprod()

df.to_csv('temp.csv',encoding='gbk',index=False)