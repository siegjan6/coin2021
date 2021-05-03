"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行/西蒙斯

# 课程内容
- Rolling操作
- Expanding操作
- 输出到本地文件
"""
import pandas as pd  # 将pandas作为第三方库导入，我们一般为pandas取一个别名叫做pd

pd.set_option('expand_frame_repr', False)  # 当列太多时清楚展示

# =====导入数据
df = pd.read_csv(
    r'C:\Users\Simons\Desktop\xbx_coin_2020\data\OKEX_BTC-USDT_20200302_1T.csv',
    encoding='gbk',
    skiprows=1
)

# =====rolling
# 计算'close'这一列的均值
# print(df['close'])
# 如何得到每个周期的最近3个周期收盘价的均值呢？即如何计算常用的移动平均线？
# 使用rolling函数
# df['收盘价_移动平均线'] = df['close'].rolling(3).mean()
# print(df[['close', '收盘价_移动平均线']])
# rolling(n)即为取最近n行数据的意思，只计算这n行数据。后面可以接各类计算函数，例如max、min、std等
# print(df['close'].rolling(3).max())
# print(df['close'].rolling(3).min())
# print(df['close'].rolling(3).std())


# =====expanding操作
# rolling可以计算每个周期的最近3个周期收盘价的均值，如果想计算每个周期的从一开始至今的均值，应该如何计算？
# 使用expanding操作
# df['收盘价_至今均值'] = df['close'].expanding().mean()
# print(df[['close', '收盘价_至今均值']])

# expanding即为取从头至今的数据。后面可以接各类计算函数
# print(df['close'].expanding().max())
# print(df['close'].expanding().min())
# print(df['close'].expanding().std())

# rolling和expanding简直是为量化领域量身定制的方法，经常会用到。


# =====输出到本地文件
# print(df)
# df.to_csv('output.csv', encoding='gbk', index=False)
