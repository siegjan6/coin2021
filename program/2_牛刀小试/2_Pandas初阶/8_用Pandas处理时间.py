"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行/西蒙斯

# 课程内容
- pandas中的时间处理
"""
import pandas as pd  # 将pandas作为第三方库导入，我们一般为pandas取一个别名叫做pd

pd.set_option('expand_frame_repr', False)  # 当列太多时清楚展示

# =====导入数据
df = pd.read_csv(
    r'C:\Users\Simons\Desktop\xbx_coin_2020\data\OKEX_BTC-USDT_20200302_1T.csv',
    encoding='gbk',
    skiprows=1
)

# ===== 时间处理
# print(df['candle_begin_time'])
# print(df.at[0, 'candle_begin_time'])
# print(type(df.at[0, 'candle_begin_time']))
# df['candle_begin_time'] = pd.to_datetime(df['candle_begin_time'])  # 将交易日期由字符串改为时间变量
# print(df.at[0, 'candle_begin_time'])
# print(type(df.at[0, 'candle_begin_time']))

# print(pd.to_datetime('1999年1月11日'))  # pd.to_datetime函数：将字符串转变为时间变量

# print(df['candle_begin_time'])
# print(df['candle_begin_time'].dt.year)  # 输出这个日期的年份。相应的month是月份，day是天数，还有hour, minute, second
# print(df['candle_begin_time'].dt.week)  # 这一天是一年当中的第几周
# print(df['candle_begin_time'].dt.dayofyear)  # 这一天是一年当中的第几天
# print(df['candle_begin_time'].dt.dayofweek)  # 这一天是这一周当中的第几天，0代表星期一
# print(df['candle_begin_time'].dt.weekday)  # 和上面函数相同，更加常用
# print(df['candle_begin_time'].dt.weekday_name)  # 和上面函数相同，返回的是星期几的英文，用于报表的制作。
# print(df['candle_begin_time'].dt.days_in_month)  # 这一天所在月份有多少天
# print(df['candle_begin_time'].dt.is_month_end)  # 这一天是否是该月的开头，是否存在is_month_end？
# print(df['candle_begin_time'] + pd.Timedelta(days=1))  # 增加一天，Timedelta用于表示时间差数据，[weeks, days, hours, minutes, seconds, milliseconds, microseconds, nanoseconds]
# print((df['candle_begin_time'] + pd.Timedelta(days=1)) - df['candle_begin_time'])  # 增加一天然后再减去今天的日期
