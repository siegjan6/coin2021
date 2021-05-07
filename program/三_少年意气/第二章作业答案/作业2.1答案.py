"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行

大作业2.1的答案
"""
import pandas as pd
import ccxt
import time
import os
import datetime
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行


"""
作业内容：
抓取币安交易所的历史数据
    至少抓取最近1个月的数据，建议抓取一年
    交易对自己选择，至少包括：btc/usdt、eth/usdt、eos/usdt、ltc/usdt
    时间周期至少包括：5分钟、15分钟
"""

"""
解题思路：
本作业较为简单，答案基本就是基于课程2.3.7代码的代码稍作修改。

课程2.3.7代码只能抓取指定一天的历史数据。作业要求是抓取某一段时间的全部历史数据，那只需要获取到该段时间每天的日期，然后遍历这些日期抓取每天的数据即可。
"""


# ===来自课程2.3.7的函数save_spot_candle_data_from_exchange
def save_spot_candle_data_from_exchange(exchange, symbol, time_interval, start_time, path):
    """
    将某个交易所在指定日期指定交易对的K线数据，保存到指定文件夹
    :param exchange: ccxt交易所
    :param symbol: 指定交易对，例如'BTC/USDT'
    :param time_interval: K线的时间周期
    :param start_time: 指定日期，格式为'2020-03-16 00:00:00'
    :param path: 文件保存根目录
    :return:
    """

    # ===对火币的limit做特殊处理
    limit = None
    if exchange.id == 'huobipro':
        limit = 2000

    # ===开始抓取数据
    df_list = []
    start_time_since = exchange.parse8601(start_time)
    end_time = pd.to_datetime(start_time) + datetime.timedelta(days=1)

    while True:
        # 获取数据
        df = exchange.fetch_ohlcv(symbol=symbol, timeframe=time_interval, since=start_time_since, limit=limit)
        # 整理数据
        df = pd.DataFrame(df, dtype=float)  # 将数据转换为dataframe
        # 合并数据
        df_list.append(df)
        # 新的since
        t = pd.to_datetime(df.iloc[-1][0], unit='ms')
        start_time_since = exchange.parse8601(str(t))
        # 判断是否挑出循环
        if t >= end_time or df.shape[0] <= 1:
            break
        # 抓取间隔需要暂停2s，防止抓取过于频繁
        time.sleep(1)

    # ===合并整理数据
    df = pd.concat(df_list, ignore_index=True)
    df.rename(columns={0: 'MTS', 1: 'open', 2: 'high',
                       3: 'low', 4: 'close', 5: 'volume'}, inplace=True)  # 重命名
    df['candle_begin_time'] = pd.to_datetime(df['MTS'], unit='ms')  # 整理时间
    df = df[['candle_begin_time', 'open', 'high', 'low', 'close', 'volume']]  # 整理列的顺序

    # 选取数据时间段
    df = df[df['candle_begin_time'].dt.date == pd.to_datetime(start_time).date()]
    # 去重、排序
    df.drop_duplicates(subset=['candle_begin_time'], keep='last', inplace=True)
    df.sort_values('candle_begin_time', inplace=True)
    df.reset_index(drop=True, inplace=True)

    # ===保存数据到文件
    # 创建交易所文件夹
    path = os.path.join(path, exchange.id)
    if os.path.exists(path) is False:
        # os.mkdir(path)  # 可以建一级文件夹
        os.makedirs(path)  # 可以建多级文件夹
    # 创建spot文件夹
    path = os.path.join(path, 'spot')
    if os.path.exists(path) is False:
        os.mkdir(path)
    # 创建日期文件夹
    path = os.path.join(path, str(pd.to_datetime(start_time).date()))
    if os.path.exists(path) is False:
        os.mkdir(path)
    # 拼接文件目录
    file_name = '_'.join([symbol.replace('/', '-'), time_interval]) + '.csv'
    path = os.path.join(path, file_name)
    # 保存数据
    df.to_csv(path, index=False)


# ===手工确认抓取数据的开始和结束时间
begin_date = '2019-04-21'  # 手工设定开始时间
end_date = '2020-04-21'  # 手工设定结束时间


# ===获取begin_date到end_date的每一天，放到date_list中
date_list = []
date = pd.to_datetime(begin_date)
while date <= pd.to_datetime(end_date):
    date_list.append(str(date))
    date += datetime.timedelta(days=1)

# 此处需要改为自己的本地路径
path = '/Users/xingbuxingx/Desktop/数字货币量化课程/2020版数字货币量化投资课程/xbx_coin_2020/data/history_candle_data'


# ===开始遍历每一天，抓取每一天的数据
error_list = []
for start_time in date_list:

    # 遍历交易所
    for exchange in [ccxt.binance()]:

        # 获取交易所需要的数据
        symbol_list = ['BTC/USDT', 'ETH/USDT', 'EOS/USDT', 'LTC/USDT', 'BCH/USDT']

        # 遍历交易对
        for symbol in symbol_list:

            # 遍历时间周期
            for time_interval in ['5m', '15m']:
                print(exchange.id, symbol, time_interval)

                # 抓取数据并且保存
                try:
                    save_spot_candle_data_from_exchange(exchange, symbol, time_interval, start_time, path)
                except Exception as e:
                    print(e)
                    error_list.append('_'.join([exchange.id, symbol, time_interval]))


print(error_list)


