"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行/西蒙斯

# 本节课程内容
- groupby操作
- 计算大小
- 获取指定group
- 常见函数
- group内部计算
- 遍历group
"""

import pandas as pd

pd.set_option('expand_frame_repr', False)  # 当列太多时显示完整

# =====导入数据
df = pd.read_csv(r'C:\Users\Simons\Desktop\xbx_coin_2020\data\cls-3.2BITFINEX-1H-data-20180124.csv', skiprows=1)


# =====groupby常用操作汇总
# 根据'candle_begin_time'进行group，将相同'交易日期'的行放入一个group，
# print(df.groupby('candle_begin_time'))  # 生成一个group对象。不会做实质性操作，只是会判断是否可以根据该变量进行groupby

# group后可以使用相关函数，size()计算每个group的行数
# print(df.groupby('candle_begin_time').size())  # 每小时交易的币的个数
# 根据'symbol'进行group，将相同'symbol'的行放入一个group，
# print(df.groupby('symbol').size())  # 每个币交易的小时数


# 获取其中某一个group
# print(df.groupby('candle_begin_time').get_group('2018-01-24 00:00:00'))
# print(df.groupby('symbol').get_group('BTCUSD'))


# 其他常见函数
# print(df.groupby('symbol').describe())  # 只会对数值变量进行describe
# print(df.groupby('symbol').head(3))
# print(df.groupby('symbol').tail(3))  # 每个group里面的行顺序，会保留。
# print(df.groupby('symbol').first())
# print(df.groupby('symbol').last())
# print(df.groupby('symbol').nth(2))
# 将group变量不设置为index
# print(df.groupby('symbol', as_index=False).nth(2))


# 在group之后，取一部分变量进行计算
# 计算每个group的均值
# print(df.groupby('symbol')['close', 'volume'].mean())
# 计算每个group的最大值
# print(df.groupby('symbol')['close', 'volume'].max())

# 计算每个group的加总
# print(df.groupby('symbol')['volume'].sum())

# 计算该数据在每个group中的排名
# print(df.groupby('candle_begin_time')['volume'].rank())
# print(df.groupby('candle_begin_time')['volume'].rank(pct=True))


# 也可以同时用多个变量来进行group，将这些变量的值都相同的行
# df['candle_begin_time'] = pd.to_datetime(df['candle_begin_time'])
# df.loc[df['candle_begin_time'].dt.hour < 12, '时间'] = '上午'
# df['时间'].fillna(value='下午', inplace=True)
# print(df.groupby(['symbol', '时间']).size())


# 我们之前讲过的resample、fillna、apply等常见操作，在group里面都可以进行。
# 这些操作需要大家有一定的积累，若直接在group上进行这些操作不熟练，可以使用已下的方式。


# 遍历group，对每个group进行单独操作，然后将这些group合并起来。
# 语法：for key, group in df.groupby('列名'):

# for symbol, group in df.groupby('symbol'):
#     print(symbol)
#     print(group)
#
#     # 以下可以对各个group进行任意操作。
#     # group.fillna()
#     # group.apply()
#
#     # 操作完之后，将这些group再append起来

# 在一开始不熟练的时候，可以多用遍历每个group的方式
