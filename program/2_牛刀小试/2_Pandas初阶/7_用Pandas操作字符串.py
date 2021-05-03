"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行/西蒙斯

# 课程内容
- pandas中的字符串的常见操作
"""
import pandas as pd  # 将pandas作为第三方库导入，我们一般为pandas取一个别名叫做pd

pd.set_option('expand_frame_repr', False)  # 当列太多时清楚展示

# =====导入数据
df = pd.read_csv(
    filepath_or_buffer=r'C:\Users\Simons\Desktop\xbx_coin_2020\data\OKEX_20200302_5T.csv',
    skiprows=1,
    encoding='gbk'
)

# =====字符串处理
# print(df['symbol'])
# print('BTC/USDT'[:3])
# print(df['symbol'].str[:3])
# print(df['symbol'].str.upper())  # 加上str之后可以使用常见的字符串函数对整列进行操作
# print(df['symbol'].str.lower())
# print(df['symbol'].str.len())  # 计算字符串的长度,length
# df['symbol'].str.strip()  # strip操作，把字符串两边的空格去掉
# print(df['symbol'])
# print(df['symbol'].str.contains('BTC'))  # 判断字符串中是否包含某些特定字符
# print(df['symbol'].str.replace('/', '-'))  # 进行替换，'/'号变成'-'
# 更多字符串函数请见：http://pandas.pydata.org/pandas-docs/stable/text.html#method-summary
