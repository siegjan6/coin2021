"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行/西蒙斯

# 课程内容
- 排序
- 合并
- 去重
- 其他
"""
import pandas as pd  # 将pandas作为第三方库导入，我们一般为pandas取一个别名叫做pd

pd.set_option('expand_frame_repr', False)  # 当列太多时清楚展示

# =====导入数据
df = pd.read_csv(
    filepath_or_buffer=r'C:\Users\Simons\Desktop\xbx_coin_2020\data\OKEX_20200302_5T.csv',
    skiprows=1,
    encoding='gbk'
)

# =====排序函数
# print(df.sort_values(by=['candle_begin_time'], ascending=True))  # by参数指定按照什么进行排序，ascending参数指定是顺序还是逆序
# print(df.sort_values(by=['symbol', 'candle_begin_time'], ascending=[1, 0]))  # 按照多列进行排序


# =====两个df上下合并操作，append操作
# df1 = df.iloc[0:10][['candle_begin_time', 'symbol', 'close', 'volume']]
# print(df1)
# df2 = df.iloc[5:15][['candle_begin_time', 'symbol', 'close', 'volume']]
# print(df2)
# print(df1.append(df2))  # append操作，将df1和df2上下拼接起来。注意观察拼接之后的index。index可以重复
# df3 = df1.append(df2, ignore_index=True)  # ignore_index参数，用户重新确定index
# print(df3)


# =====两个df左右合并操作，merge操作
# df1 = df.iloc[0:10][['candle_begin_time', 'symbol', 'close', 'volume']]
# print(df1)
# df2 = df.iloc[5:15][['candle_begin_time', 'symbol', 'close', 'volume']]
# print(df2)
#
# df_merged = pd.merge(left=df1, right=df2, left_on='candle_begin_time', right_on='candle_begin_time',
#                      suffixes=['_left', '_right'])
# print(df_merged)


# =====对数据进行去重
# df3中有重复的行数，我们如何将重复的行数去除？
# print(df3)
# df3.drop_duplicates(
#     subset=['candle_begin_time', 'symbol'],  # subset参数用来指定根据哪类类数据来判断是否重复。若不指定，则用全部列的数据来判断是否重复
#     keep='first',  # 在去除重复值的时候，我们是保留上面一行还是下面一行？first保留上面一行，last保留下面一行，False就是一行都不保留
#     inplace=True
# )
# print(df3)


# =====其他常用重要函数
# df.reset_index(inplace=True, drop=True)  # 重置index
# df.rename(columns={
#     'close': '收盘价',
#     'open': '开盘价',
#     'symbol': '交易对',
#     'candle_begin_time': '交易时间',
#     'high': '最高价',
#     'low': '最低价',
#     'volume': '成交量'
# }, inplace=True)  # rename函数给变量修改名字。使用dict将要修改的名字传给columns参数
# print(df.empty)  # 判断一个df是不是为空，此处输出不为空
# print(pd.DataFrame().empty)  # pd.DataFrame()创建一个空的DataFrame，此处输出为空
# print(df.T)  # 将数据转置，行变成列，很有用
