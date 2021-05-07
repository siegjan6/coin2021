"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行

# 课程内容
介绍如何将策略实际持仓pos，转换成资金曲线
"""
import pandas as pd
import numpy as np
from datetime import timedelta
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数


# =====导入数据
df = pd.read_hdf('/Users/xingbuxingx/Desktop/数字货币量化课程/2020版数字货币量化投资课程/xbx_coin_2020/data/pos.h5', key='df')
# 选取数据：币种上线10天之后的日期
t = df.iloc[0]['candle_begin_time'] + timedelta(days=10)
df = df[df['candle_begin_time'] > t]
df.drop(['volume', 'quote_volume'], axis=1, inplace=True)

# =====找出下根K线的开盘价
df['next_open'] = df['open'].shift(-1)  # 下根K线的开盘价
df['next_open'].fillna(value=df['close'], inplace=True)


# =====找出开仓、平仓的k线
condition1 = df['pos'] != 0  # 当前周期不为空仓
condition2 = df['pos'] != df['pos'].shift(1)  # 当前周期和上个周期持仓方向不一样。
open_pos_condition = condition1 & condition2

condition1 = df['pos'] != 0  # 当前周期不为空仓
condition2 = df['pos'] != df['pos'].shift(-1)  # 当前周期和下个周期持仓方向不一样。
close_pos_condition = condition1 & condition2


# =====对每次交易进行分组
df.loc[open_pos_condition, 'start_time'] = df['candle_begin_time']
df['start_time'].fillna(method='ffill', inplace=True)
df.loc[df['pos'] == 0, 'start_time'] = pd.NaT


# =====开始计算资金曲线
# ===基本参数
initial_cash = 1000000  # 初始资金，默认为10000元
face_value = 0.01  # btc是0.01，不同的币种要进行不同的替换
c_rate = 5 / 10000  # 手续费，commission fees，默认为万分之5。不同市场手续费的收取方法不同，对结果有影响。比如和股票就不一样。
slippage = 1 / 1000  # 滑点 ，可以用百分比，也可以用固定值。建议币圈用百分比，股票用固定值
leverage_rate = 3
min_margin_ratio = 1 / 100  # 最低保证金率，低于就会爆仓


# ===在开仓时
# 在open_pos_condition的K线，以开盘价计算买入合约的数量。（当资金量大的时候，可以用本根K线的前5分钟均价）
df.loc[open_pos_condition, 'contract_num'] = initial_cash * leverage_rate / (face_value * df['open'])
df['contract_num'] = np.floor(df['contract_num'])  # 对合约张数向下取整
# 开仓价格：理论开盘价加上相应滑点
df.loc[open_pos_condition, 'open_pos_price'] = df['open'] * (1 + slippage * df['pos'])
# 开仓之后，要扣除手续费。在初始保证金中扣除
df['cash'] = initial_cash - df['open_pos_price'] * face_value * df['contract_num'] * c_rate  # 即保证金

# ===持仓：开仓之后每根K线结束时
# 买入之后cash，contract_num，open_pos_price不再发生变动
for _ in ['contract_num', 'open_pos_price', 'cash']:
    df[_].fillna(method='ffill', inplace=True)
df.loc[df['pos'] == 0, ['contract_num', 'open_pos_price', 'cash']] = None

# ===在平仓时
# 平仓价格
df.loc[close_pos_condition, 'close_pos_price'] = df['next_open'] * (1 - slippage * df['pos'])  # 使用到next_open
# 平仓手续费
df.loc[close_pos_condition, 'close_pos_fee'] = df['close_pos_price'] * face_value * df['contract_num'] * c_rate

# ===计算利润
# 开仓至今持仓盈亏
df['profit'] = face_value * df['contract_num'] * (df['close'] - df['open_pos_price']) * df['pos']
df.loc[close_pos_condition, 'profit'] = face_value * df['contract_num'] * (df['close_pos_price'] - df['open_pos_price']) * df['pos']
# 账户净值
df['net_value'] = df['cash'] + df['profit']


# ===计算爆仓
# 至今持仓盈亏最小值
df.loc[df['pos'] == 1, 'price_min'] = df['low']
df.loc[df['pos'] == -1, 'price_min'] = df['high']
df['profit_min'] = face_value * df['contract_num'] * (df['price_min'] - df['open_pos_price']) * df['pos']
# 账户净值最小值
df['net_value_min'] = df['cash'] + df['profit_min']
# 计算最低保证金率
df['margin_ratio'] = df['net_value_min'] / (face_value * df['contract_num'] * df['price_min'])
# 计算是否爆仓
df.loc[df['margin_ratio'] <= (min_margin_ratio + c_rate), '是否爆仓'] = 1
# 此处爆仓计算使用价格的极值，这里比现实更加严格。因为现实中使用标记价格来计算爆仓的。

# ===平仓时扣除手续费
df.loc[close_pos_condition, 'net_value'] -= df['close_pos_fee']
# 当下一根K线价格突变，在平仓的时候爆仓，要做相应处理。此处处理有省略，不精确。
df.loc[close_pos_condition & (df['net_value'] < 0), '是否爆仓'] = 1

# ===对爆仓进行处理
df['是否爆仓'] = df.groupby('start_time')['是否爆仓'].fillna(method='ffill')
df.loc[df['是否爆仓'] == 1, 'net_value'] = 0


# =====计算资金曲线
df['equity_change'] = df['net_value'].pct_change()
df.loc[open_pos_condition, 'equity_change'] = df.loc[open_pos_condition, 'net_value'] / initial_cash - 1  # 开仓日的收益率
df['equity_change'].fillna(value=0, inplace=True)
df['equity_curve'] = (1 + df['equity_change']).cumprod()


# =====删除不必要的数据，并存储
df.drop(['next_open', 'contract_num', 'open_pos_price', 'cash', 'close_pos_price', 'close_pos_fee',
         'profit', 'net_value', 'price_min', 'profit_min', 'net_value_min', 'margin_ratio', '是否爆仓'],
        axis=1, inplace=True)

df.to_hdf('/Users/xingbuxingx/Desktop/数字货币量化课程/2020版数字货币量化投资课程/xbx_coin_2020/data/equity_curve.h5', key='df', mode='w')

