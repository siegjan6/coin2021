"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行/西蒙斯

# 课程内容
- 数据筛选
"""
import pandas as pd  # 将pandas作为第三方库导入，我们一般为pandas取一个别名叫做pd

pd.set_option('expand_frame_repr', False)  # 当列太多时清楚展示

# =====导入数据
df = pd.read_csv(
    # 该参数为数据在电脑中的路径，
    # 要注意字符串转义符号 \ ，可以使用加r变为raw string或者每一个进行\\转义
    filepath_or_buffer=r'C:\Users\Simons\Desktop\xbx_coin_2020\data\OKEX_20200302_5T.csv',
    # 编码格式，不同的文件有不同的编码方式，一般文件中有中文的，编码是gbk，默认是utf8
    # ** 大家不用去特意记住很多编码，我们常用的就是gbk和utf8，切换一下看一下程序不报错就好了
    skiprows=1,
    encoding='gbk',
)

# =====数据筛选，根据指定的条件，筛选出相关的数据。
# print(df['symbol'] == 'BTC/USDT')  # 判断交易交易对是否等于BTC/USDT
# print(df[df['symbol'] == 'BTC/USDT'])  # 将判断为True的输出：选取交易对等于BTC/USDT的行
# print(df[df['symbol'] == 'BTC/USDT'].index)  # 输出判断为True的行的index
# print(df[df['symbol'].isin(
#     ['BTC/USDT', 'ETH/USDT', 'EOS/BTC']
# )])  # 选取交易对等于'BTC/USDT'或'ETH/USDT'或'EOS/BTC'的都行
# print(df[df['close'] < 8500])  # 选取收盘价小于8500的行
# print(df[(df['close'] < 8888) & (df['candle_begin_time'] > '2020-03-02 23:30:00+00:00')])  # 两个条件，或者的话就是|
