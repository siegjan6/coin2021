"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行

# 课程内容
抓取数字货币交易所的数据，构建数据库
"""
import pandas as pd
import ccxt
import time
import os
import datetime
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行


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
    # path = os.path.join(path, exchange.id)
    # if os.path.exists(path) is False:
    #     os.mkdir(path)

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
    pd.DataFrame(columns=['数据由jan整理']).to_csv(path, index=False)
    df.to_csv(path, mode='a', index=False)


start_time = '2020-05-24 00:00:00'
end_date = '2021-05-24'  # 手工设定结束时间
date_list = []
date = pd.to_datetime(start_time)
while date <= pd.to_datetime(end_date):
    date_list.append(str(date))
    date += datetime.timedelta(days=1)

path = r'C:\Users\jan\Documents\GitHub\coin2021\data'
error_list = []


# 遍历交易所
for exchange in [ccxt.binance()]:

    # 获取交易所需要的数据
    market = exchange.load_markets()
    market = pd.DataFrame(market).T

    symbol_list = list(market['symbol'])
    symbol_list = ['ETH/USDT', 'BTC/USDT', 'DOGE/USDT']  #替换上面

    # 遍历交易对
    for symbol in symbol_list:
        if symbol.endswith('/USDT') is False:
            continue

        # 遍历时间周期
        for time_interval in ['5m']:
            print(exchange.id, symbol, time_interval)

            # 抓取数据并且保存
            for t in date_list:
                try:
                    save_spot_candle_data_from_exchange(exchange, symbol, time_interval, t, path)
                except Exception as e:
                    print(e)
                    error_list.append('_'.join([exchange.id, symbol, time_interval]))


print(error_list)


"""
# 每天自动更新数据
如果需要每天更新数据，可以在北京时间8点过一点的时候，运行程序更新数据。
需要将start_time改为：
yesterday_date = datetime.date.today() - datetime.timedelta(days=1)
start_time = str(yesterday_date) + ' 00:00:00'

想要每天自动运行的话，可以参见邢不行公众号这篇文章：https://mp.weixin.qq.com/s/vrv-PniBGxEerJ44AV0jcw
"""

"""
# 批量抓取历史数据

在现有程序基础上，遍历日期即可抓取历史数据。产生日期列表的代码：

begin_date = '2020-03-01'  # 手工设定开始时间
end_date = '2020-03-16'  # 手工设定结束时间

date_list = []
date = pd.to_datetime(begin_date)
while date <= pd.to_datetime(end_date):
    date_list.append(str(date))
    date += datetime.timedelta(days=1)
"""

"""
1. 抓取数据，够用就行，别想求全。指定品种、周期。
2. 多注意数据质量，不是说抓下来的数据一定就是干净的。
3. 自己抓取binance的历史数据，火币、ok的历史数据，只能想其他办法，或者...

4. 这就是数据库，别自己额外学数据库。存、用分开。
"""
