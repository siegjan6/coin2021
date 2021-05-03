"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行/西蒙斯

# 课程内容：查看Pandas读入的数据
- 看数据
- 行列操作
"""
import pandas as pd  # 将pandas作为第三方库导入，我们一般为pandas取一个别名叫做pd
pd.set_option('expand_frame_repr', False)  # 当列太多时显示不清楚

# =====导入数据
df = pd.read_csv(
    # 该参数为数据在电脑中的路径，
    # 要注意字符串转义符号 \ ，可以使用加r变为raw string或者每一个进行\\转义
    filepath_or_buffer=r'C:\Users\Simons\Desktop\xbx_coin_2020\data\OKEX_BTC-USDT_20200302_1T.csv',
    # 编码格式，不同的文件有不同的编码方式，一般文件中有中文的，编码是gbk，默认是utf8
    # ** 大家不用去特意记住很多编码，我们常用的就是gbk和utf8，切换一下看一下程序不报错就好了
    encoding='gbk',
    # 该参数代表跳过数据文件的的第1行不读入
    skiprows=1,
    # nrows=15,
    # parse_dates=['candle_begin_time'],
    # 将指定列设置为index。若不指定，index默认为0, 1, 2, 3, 4...
    index_col=['candle_begin_time'],
)

# =====看数据
# print(df.shape)  # 输出dataframe有多少行、多少列。
# print(df.shape[0])  # 取行数量，相应的列数量就是df.shape[1]
# print(df.columns)  # 顺序输出每一列的名字，演示如何for语句遍历。
# print(df.index)  # 顺序输出每一行的名字，可以for语句遍历。
# print(df.dtypes)  # 数据每一列的类型不一样，比如数字、字符串、日期等。该方法输出每一列变量类型
# print(df.head(3))  # 看前3行的数据，默认是5。与自然语言很接近
# print(df.tail(3))  # 看最后3行的数据，默认是5。
# print(df.sample(n=3))  # 随机抽取3行，想要去固定比例的话，可以用frac参数
# print(df.describe())  # 非常方便的函数，对每一列数据有直观感受；只会对数字类型的列有效
# print(df.info())  # 输出一个dataframe的基本信息

# 对print出的数据格式进行修正
# pd.set_option('expand_frame_repr', False)  # 当列太多时显示不清楚
# pd.set_option("display.max_rows", 1000)  # 设定显示最大的行数
# pd.set_option('precision', 1)  # 浮点数的精度
# print(df.head())

# 更多设置请见http://pandas.pydata.org/pandas-docs/stable/options.html


# =====如何选取指定的行、列
# print(df['open'])  # 根据列名称来选取，读取的数据是Series类型
# print(df[['candle_begin_time', 'close']])  # 同时选取多列，需要两个括号，读取的数据是DataFrame类型
# print(df[['open']])

# print(df)

# loc操作：通过label的名字来读取数据
# print(df.loc['2020-03-02 00:06:00+00:00'])  # 选取指定的某一行，读取的数据是Series类型
# print(df.loc['2020-03-02 00:06:00+00:00', 'close'])  # loc操作：通过label（columns和index的名字）来读取数据
# print(df.loc[['2020-03-02 00:06:00+00:00', '2020-03-02 00:10:00+00:00']])  # 选取指定的两行
# print(df.loc['2020-03-02 00:06:00+00:00': '2020-03-02 00:10:00+00:00'])  # 选取在此范围内的多行，和在list中slice操作类似，读取的数据是DataFrame类型
# print(df.loc[:, 'open':'low'])  # 选取在此范围内的多列，读取的数据是DataFrame类型
# print(df.loc['2020-03-02 00:06:00+00:00': '2020-03-02 00:10:00+00:00', 'open':'close'])  # 读取指定的多行、多列。逗号之前是行的范围，逗号之后是列的范围。读取的数据是DataFrame类型
# print(df.loc[:, :])  # 读取所有行、所有列，读取的数据是DataFrame类型
# print(df.at['2020-03-02 00:06:00+00:00', 'open'])  # 使用at读取指定的某个元素。loc也行，但是at更高效。
# print(df.loc['2020-03-02 00:06:00+00:00', 'open'])

# iloc操作：通过position来读取数据
# print(df.iloc[0])  # 以index选取某一行，读取的数据是Series类型
# print(df.iloc[1:3])  # 选取在此范围内的多行，读取的数据是DataFrame类型
# print(df.iloc[:, 1:3])  # 选取在此范围内的多列，读取的数据是DataFrame类型
# print(df.iloc[1:3, 1:3])  # 读取指定的多行、多列，读取的数据是DataFrame类型
# print(df.iloc[:, :])  # 读取所有行、所有列，读取的数据是DataFrame类型
# print(df.iat[1, 3])  # 使用iat读取指定的某个元素。使用iloc也行，但是iat更高效。

# =====文档
# 以上是我认为最常用的函数
# 哪里可以看到全部的函数？http://pandas.pydata.org/pandas-docs/stable/api.html
