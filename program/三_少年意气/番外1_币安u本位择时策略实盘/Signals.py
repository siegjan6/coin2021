"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行

# 课程内容
币安u本位择时策略实盘框架需要的signal
"""
import pandas as pd
import random
import numpy as np


# 将None作为信号返回
def real_signal_none(df, now_pos, avg_price, para):
    """
    发出空交易信号
    :param df:
    :param now_pos:
    :param avg_price:
    :param para:
    :return:
    """

    return None


# 随机生成交易信号
def real_signal_random(df, now_pos, avg_price, para):
    """
    随机发出交易信号
    :param df:
    :param now_pos:
    :param avg_price:
    :param para:
    :return:
    """

    r = random.random()
    if r <= 0.25:
        return 0
    elif r <= 0.5:
        return 1
    elif r <= 0.75:
        return -1
    else:
        return None


# 布林策略实盘交易信号
def real_signal_simple_bolling(df, now_pos, avg_price, para=[200, 2]):
    """
    实盘产生布林线策略信号的函数，和历史回测函数相比，计算速度更快。
    布林线中轨：n天收盘价的移动平均线
    布林线上轨：n天收盘价的移动平均线 + m * n天收盘价的标准差
    布林线上轨：n天收盘价的移动平均线 - m * n天收盘价的标准差
    当收盘价由下向上穿过上轨的时候，做多；然后由上向下穿过中轨的时候，平仓。
    当收盘价由上向下穿过下轨的时候，做空；然后由下向上穿过中轨的时候，平仓。
    :param df:  原始数据
    :param para:  参数，[n, m]
    :return:
    """

    # ===策略参数
    # n代表取平均线和标准差的参数
    # m代表标准差的倍数
    n = int(para[0])
    m = para[1]

    # ===计算指标
    # 计算均线
    df['median'] = df['close'].rolling(n).mean()  # 此处只计算最后几行的均线值，因为没有加min_period参数
    median = df.iloc[-1]['median']
    median2 = df.iloc[-2]['median']
    # 计算标准差
    df['std'] = df['close'].rolling(n).std(ddof=0)  # ddof代表标准差自由度，只计算最后几行的均线值，因为没有加min_period参数
    std = df.iloc[-1]['std']
    std2 = df.iloc[-2]['std']
    # 计算上轨、下轨道
    upper = median + m * std
    lower = median - m * std
    upper2 = median2 + m * std2
    lower2 = median2 - m * std2

    # ===寻找交易信号
    signal = None
    close = df.iloc[-1]['close']
    close2 = df.iloc[-2]['close']
    # 找出做多信号
    if (close > upper) and (close2 <= upper2):
        signal = 1
    # 找出做空信号
    elif (close < lower) and (close2 >= lower2):
        signal = -1
    # 找出做多平仓信号
    elif (close < median) and (close2 >= median2):
        signal = 0
    # 找出做空平仓信号
    elif (close > median) and (close2 <= median2):
        signal = 0

    return signal


# 【西瓜蹲】自适应布林+bias+布林强盗止盈止损_BTC: 4.64 (达标)、ETH: 9.00 (达标)、参数1
# https://bbs.quantclass.cn/thread/4378
def singal_adaptboll_bandit_bias(df, now_pos, avg_price, para=[547]):
    # ===策略参数
    n = int(para[0])

    # ===计算指标
    # 计算均线
    df['median'] = df['close'].rolling(n, min_periods=1).mean()
    # 计算上轨、下轨道
    df['std'] = df['close'].rolling(n, min_periods=1).std(ddof=0)

    df['z_score'] = abs(df['close'] - df['median']) / df['std']
    df['m'] = df['z_score'].rolling(window=n).max().shift(1)
    df['upper'] = df['median'] + df['m'] * df['std']
    df['lower'] = df['median'] - df['m'] * df['std']

    # 计算bias
    df['bias'] = df['close'] / df['median'] - 1
    df['z_score'] = abs(df['close'] / df['median'] - 1)
    df['bias_pct'] = df['z_score'].rolling(window=n).max().shift(1)

    # ===计算原始布林策略信号
    # 找出做多信号
    condition1 = df['close'] > df['upper']  # 当前K线的收盘价 > 上轨
    condition2 = df['close'].shift(1) <= df['upper'].shift(1)  # 之前K线的收盘价 <= 上轨
    df.loc[condition1 & condition2, 'signal_long'] = 1  # 将产生做多信号的那根K线的signal设置为1，1代表做多

    # 找出做多平仓信号
    condition1 = df['close'] < df['median']  # 当前K线的收盘价 < 中轨
    condition2 = df['close'].shift(1) >= df['median'].shift(1)  # 之前K线的收盘价 >= 中轨
    df.loc[condition1 & condition2, 'signal_long'] = 0  # 将产生平仓信号当天的signal设置为0，0代表平仓

    # 找出做空信号
    condition1 = df['close'] < df['lower']  # 当前K线的收盘价 < 下轨
    condition2 = df['close'].shift(1) >= df['lower'].shift(1)  # 之前K线的收盘价 >= 下轨
    df.loc[condition1 & condition2, 'signal_short'] = -1  # 将产生做空信号的那根K线的signal设置为-1，-1代表做空

    # 找出做空平仓信号
    condition1 = df['close'] > df['median']  # 当前K线的收盘价 > 中轨
    condition2 = df['close'].shift(1) <= df['median'].shift(1)  # 之前K线的收盘价 <= 中轨
    df.loc[condition1 & condition2, 'signal_short'] = 0  # 将产生平仓信号当天的signal设置为0，0代表平仓

    # ===将long和short合并为signal
    df['signal_short'].fillna(method='ffill', inplace=True)
    df['signal_long'].fillna(method='ffill', inplace=True)
    df['signal'] = df[['signal_long', 'signal_short']].sum(axis=1)
    df['signal'].fillna(value=0, inplace=True)
    df['raw_signal'] = df['signal']

    # ===根据bias，修改开仓时间
    df['temp'] = df['signal']

    # 将原始信号做多时，当bias大于阀值，设置为空
    condition1 = (df['signal'] == 1)
    condition2 = (df['bias'] > df['bias_pct'])
    df.loc[condition1 & condition2, 'temp'] = None

    # 将原始信号做空时，当bias大于阀值，设置为空
    condition1 = (df['signal'] == -1)
    condition2 = (df['bias'] < -1 * df['bias_pct'])
    df.loc[condition1 & condition2, 'temp'] = None

    # 原始信号刚开仓，并且大于阀值，将信号设置为0
    condition1 = (df['signal'] != df['signal'].shift(1))
    condition2 = (df['temp'].isnull())
    df.loc[condition1 & condition2, 'temp'] = 0

    # 使用之前的信号补全原始信号
    df['temp'].fillna(method='ffill', inplace=True)
    df['signal'] = df['temp']

    # Bandit start
    # 计算k线之间的时差，秒为单位!
    df['candle_begin_time'] = df['candle_begin_time_GMT8']
    time_diff = (df['candle_begin_time'].values[1] - df['candle_begin_time'].values[0]) / np.timedelta64(1, 's')
    # 标记开平仓时间
    df['start_time'] = np.where(df['signal'] != df['signal'].shift(1), df['candle_begin_time'], np.datetime64('NaT'))
    df['start_time'].fillna(method='ffill', inplace=True)
    # 当前k线开始时间到开平仓起始时间差，秒为单位
    df['time_diff'] = df['candle_begin_time'] - df['start_time']
    df['time_diff'] = df['time_diff'].apply(lambda x: x.total_seconds())
    # 根据时间差计算从开平仓开始到当前是第几根k线
    df['cnt'] = df['time_diff'] / time_diff
    # 计算均线周期，起始为 n ，每过一根k线减去1，直到最小值5
    df['cnt'] = df['cnt'].apply(lambda x: int(n - x) if int(n - x) > 5 else 5)

    # 按照每根k线不同的均线周期，循环计算均线值
    close_list = df['close'].values
    cnt_list = df['cnt'].values
    ma_list = []
    for i in range(0, len(close_list)):
        m = cnt_list[i]
        if i < m:
            ma_list.append(close_list[0: i + 1].mean())
        else:
            ma_list.append(close_list[i - m + 1: i + 1].mean())

    df['ma'] = ma_list

    # temp 计算新的signal
    df['temp'] = np.NaN
    condition1 = (df['signal'] == 1) & (df['close'] > df['upper'])
    condition2 = (df['signal'] == -1) & (df['close'] < df['lower'])
    condition3 = (df['signal'] == 1) & (df['close'] < df['ma']) & (df['close'] < df['upper'])
    condition4 = (df['signal'] == -1) & (df['close'] > df['ma']) & (df['close'] > df['lower'])
    # 原始signal==1（开多），并且close>upper, 标记为1
    # 原始signal==-1（开空），并且close<lower, 标记为1
    # 其他标记为空，用于平仓之后再次突破上轨后再开仓
    df['temp'] = np.where(condition1 | condition2, 1, np.NaN)
    # 原始signal==1（开多），并且close<均线同时<upper, 标记为 0
    # 原始signal==-1（开空），并且close>均线同时>lower, 标记为0
    # 其他标记为原值
    df['temp'] = np.where(condition3 | condition4, 0, df['temp'])
    # 乘以原signal，使得开空的temp变为-1
    df['temp'] = df['temp'] * df['signal']
    # 将原始不开仓的k线，在temp也标记为不开仓 0
    df['temp'] = np.where(df['signal'] == 0, 0, df['temp'])
    # 将temp用前一个值填充空值
    df['temp'].fillna(method='ffill', inplace=True)
    # 将新信号赋值到原始信号
    df['signal'] = df['temp']

    # ===将signal中的重复值删除
    temp = df[['signal']]
    temp = temp[temp['signal'] != temp['signal'].shift(1)]
    df['signal'] = temp

    df.drop(['raw_signal', 'z_score', 'm', 'std', 'z_score', 'temp', 'bias', 'bias_pct', 'signal_long', 'signal_short',
             'start_time', 'time_diff', 'cnt'], axis=1, inplace=True)

    return df.iloc[-1]['signal']
