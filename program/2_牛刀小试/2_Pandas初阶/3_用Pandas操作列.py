"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行/西蒙斯

# 课程内容
- 列操作
- 针对列的统计函数
"""
import pandas as pd  # 将pandas作为第三方库导入，我们一般为pandas取一个别名叫做pd

pd.set_option('expand_frame_repr', False)  # 当列太多时显示完整

# =====导入数据
df = pd.read_csv(
    # 该参数为数据在电脑中的路径，
    # 要注意字符串转义符号 \ ，可以使用加r变为raw string或者每一个进行\\转义
    filepath_or_buffer=r'C:\Users\Simons\Desktop\xbx_coin_2020\data\OKEX_BTC-USDT_20200302_1T.csv',
    # 编码格式，不同的文件有不同的编码方式，一般文件中有中文的，编码是gbk，默认是utf8
    # ** 大家不用去特意记住很多编码，我们常用的就是gbk和utf8，切换一下看一下程序不报错就好了
    encoding='gbk',
    nrows=15,
    # 该参数代表跳过数据文件的的第1行不读入
    skiprows=1,
    # 将指定列设置为index。若不指定，index默认为0, 1, 2, 3, 4...
    # index_col=['candle_begin_time'],
)

# =====列操作
# 行列加减乘除
# print(df['candle_begin_time'] + ' UTC时间')  # 字符串列可以直接加上字符串，对整列进行操作
# print(df['close'] * 100)  # 数字列直接加上或者乘以数字，对整列进行操作。
# print(df[['close', 'volume']])
# print(df['close'] * df['volume'])  # 两列之间可以直接操作。收盘价*成交量计算出的是什么？
# 新增一列
# df['candle_begin_time2'] = df['candle_begin_time'] + ' UTC'
# df['交易所'] = 'OKEX'

# =====统计函数
# print(df['close'].mean())  # 求一整列的均值，返回一个数。会自动排除空值。
# print(df[['close', 'volume']].mean())  # 求两列的均值，返回两个数，Series
# print(df[['close', 'volume']])
# print(df[['close', 'volume']].mean(axis=1))  # 求两列的均值，返回DataFrame。axis=0或者1要搞清楚。
# axis=1，代表对整几列进行操作。axis=0（默认）代表对几行进行操作。实际中弄混很正常，到时候试一下就知道了。

# print(df['high'].max())  # 最大值
# print(df['low'].min())  # 最小值
# print(df['close'].std())  # 标准差
# print(df['close'].count())  # 非空的数据的数量
# print(df['close'].median())  # 中位数
# print(df['close'].quantile(0.25))  # 25%分位数
# 还有其他的函数计算其他的指标，在实际使用中遇到可以自己搜索


# =====shift类函数、删除列的方式
# df['下周期收盘价'] = df['close'].shift(-1)  # 读取上一行的数据，若参数设定为3，就是读取上三行的数据；若参数设定为-1，就是读取下一行的数据；
# del df['下周期收盘价']  # 删除某一列的方法

# df['涨跌'] = df['close'].diff(1)  # 求本行数据和上一行数据相减得到的值
# df.drop(['涨跌'], axis=1, inplace=True)  # 删除某一列的另外一种方式，inplace参数指是否替代原来的df
# df['涨跌幅'] = df['close'].pct_change(1)  # 类似于diff，但是求的是两个数直接的比例，相当于求涨跌幅

# =====cum(cumulative)类函数
# df['累计成交量'] = df['volume'].cumsum()  # 该列的累加值
# print(df[['candle_begin_time', 'volume', '累计成交量','涨跌幅']])
# print((df['涨跌幅'] + 1.0).cumprod())  # 该列的累乘值，此处计算的就是资金曲线，假设初始1元钱。


# =====其他列函数
# df['收盘价_排名'] = df['close'].rank(ascending=True, pct=False)  # 输出排名。ascending参数代表是顺序还是逆序。pct参数代表输出的是排名还是排名比例
# print(df[['close', '收盘价_排名']])
# del df['收盘价_排名']
# print(df['close'].value_counts())  # 计数。统计该列中每个元素出现的次数。返回的数据是Series

# =====文档
# 以上是我认为最常用的函数
# 哪里可以看到全部的函数？http://pandas.pydata.org/pandas-docs/stable/api.html
