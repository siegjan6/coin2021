'''
邢不行 | 量化小讲堂系列文章
《抱团股会一直涨？无脑执行大小盘轮动策略，轻松跑赢指数5倍【附Python代码】》
https://mp.weixin.qq.com/s/hPjVbBKomfMhowc32jUwhA
获取更多量化文章，请联系邢不行个人微信：xbx3642
'''
import pandas as pd
import numpy as np
from function import *
import matplotlib.pyplot as plt


pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数

# 读取数据
df_big = pd.read_csv('sh000300.csv', encoding='gbk', parse_dates=['candle_end_time'])
df_small = pd.read_csv('sz399006.csv', encoding='gbk', parse_dates=['candle_end_time'])

# df_big = getSymbolData('BTC-USDT_5m')
# df_small = getSymbolData('ETH-USDT_5m')
# 设置参数
trade_rate = 0.6 / 10000  # 场内基金万分之0.6，买卖手续费相同，无印花税
momentum_days = 20  # 计算多少天的动量

# 计算大小盘每天的涨跌幅amplitude
df_big['big_amp'] = df_big['close'] / df_big['close'].shift(1) - 1
df_small['small_amp'] = df_small['close'] / df_small['close'].shift(1) - 1
# 重命名行
df_big.rename(columns={'open': 'big_open', 'close': 'big_close'}, inplace=True)
df_small.rename(columns={'open': 'small_open', 'close': 'small_close'}, inplace=True)
# 合并数据
df = pd.merge(left=df_big[['candle_end_time', 'big_open', 'big_close', 'big_amp']], left_on=['candle_end_time'],
              right=df_small[['candle_end_time', 'small_open', 'small_close', 'small_amp']],
              right_on=['candle_end_time'], how='left')
# 计算N日的动量momentum
df['big_mom'] = df['big_close'].pct_change(periods=momentum_days)
df['small_mom'] = df['small_close'].pct_change(periods=momentum_days)
# 风格变换条件
df.loc[df['big_mom'] > df['small_mom'], 'style'] = 'big'
df.loc[df['big_mom'] < df['small_mom'], 'style'] = 'small'
# 相等时维持原来的仓位。
df['style'].fillna(method='ffill', inplace=True)
# 收盘才能确定风格，实际的持仓pos要晚一天。
df['pos'] = df['style'].shift(1)
# 删除持仓为nan的天数（创业板2010年才有）
df.dropna(subset=['pos'], inplace=True)
# 计算策略的整体涨跌幅strategy_amp
df.loc[df['pos'] == 'big', 'strategy_amp'] = df['big_amp']
df.loc[df['pos'] == 'small', 'strategy_amp'] = df['small_amp']

# 调仓时间
df.loc[df['pos'] != df['pos'].shift(1), 'trade_time'] = df['candle_end_time']
# 将调仓日的涨跌幅修正为开盘价买入涨跌幅（并算上交易费用，没有取整数100手，所以略有误差）
df.loc[(df['trade_time'].notnull()) & (df['pos'] == 'big'), 'strategy_amp_adjust'] = df['big_close'] / (
        df['big_open'] * (1 + trade_rate)) - 1
df.loc[(df['trade_time'].notnull()) & (df['pos'] == 'small'), 'strategy_amp_adjust'] = df['small_close'] / (
        df['small_open'] * (1 + trade_rate)) - 1
df.loc[df['trade_time'].isnull(), 'strategy_amp_adjust'] = df['strategy_amp']
# 扣除卖出手续费
df.loc[(df['trade_time'].shift(-1).notnull()), 'strategy_amp_adjust'] = (1 + df[
    'strategy_amp']) * (1 - trade_rate) - 1
del df['strategy_amp'], df['style']

df.reset_index(drop=True, inplace=True)
# 计算净值
df['big_net'] = df['big_close'] / df['big_close'][0]
df['small_net'] = df['small_close'] / df['small_close'][0]
df['strategy_net'] = (1 + df['strategy_amp_adjust']).cumprod()

# 评估策略的好坏
res = evaluate_investment(df, 'strategy_net', time='candle_end_time')
print(res)

# 绘制图形
plt.plot(df['candle_end_time'], df['strategy_net'], label='strategy')
plt.plot(df['candle_end_time'], df['big_net'], label='big_net')
plt.plot(df['candle_end_time'], df['small_net'], label='small_net')
plt.show()

# 保存文件
print(df.tail(10))
df.to_csv('大小盘风格切换.csv', encoding='gbk', index=False)
