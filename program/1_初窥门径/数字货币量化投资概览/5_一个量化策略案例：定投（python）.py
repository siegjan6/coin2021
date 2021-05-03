"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行/西蒙斯

介绍数字货币定投的简单策略
"""
import pandas as pd  # 第三方库，专门用于数据分析，处理表格数据
pd.set_option('expand_frame_repr', False)  # 照抄即可，不求甚解


# ===读取数据
df = pd.read_csv('EOSUSD_1D.csv',  # 此处为数据文件地址，请自行修改为本电脑的地址
                 skiprows=1,  # 跳过第一行数据
                 )
# print(df)  # 将数据打印出来查看，head，sample，
df = df[['candle_begin_time', 'close']]  # 选取特定的几列

# ===选取时间段
# df = df[df['candle_begin_time'] >= '2013-12-04']  # 定投开始时间
# df = df[df['candle_begin_time'] <= '2015-12-31']  # 定投结束时间

# ===计算累计投入资金
df['每次投入资金'] = 100  # 每个周期投入100元买币
df['累计投入资金'] = df['每次投入资金'].cumsum()  # 至今累计投入的资金，cumulative_sum

# ===计算累计买币数量
c_rate = 0.002  # 手续费，回测一定要精确
df['每次买币数量'] = df['每次投入资金'] / df['close'] * (1 - c_rate)  # 每个周期买入币的数量，扣除了手续费（此处手续费计算有近似）
df['累计买币数量'] = df['每次买币数量'].cumsum()  # 累计买入币的数量

# ===计算币的市值
df['平均持有成本'] = df['累计投入资金'] / df['累计买币数量']
df['币市值'] = df['累计买币数量'] * df['close']

# ===输出数据
print(df[['candle_begin_time', 'close', '累计投入资金', '币市值', '平均持有成本']])
df.to_csv('计算输出数据结果.csv', index=False)
