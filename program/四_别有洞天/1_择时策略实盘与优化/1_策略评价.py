"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行/西蒙斯

# 本节课程内容
评价策略好坏的主流指标
"""
import pandas as pd
from Statistics import *
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数


# 读取资金曲线数据
equity_curve = pd.read_pickle('/Users/xingbuxingx/Desktop/数字货币量化课程/2020版数字货币量化投资课程/xbx_coin_2020/data/cls-4.1.1/equity_curve.pkl')
# print(equity_curve)


# 计算每笔交易
trade = transfer_equity_curve_to_trade(equity_curve)
print(trade)


# 计算各类统计指标
r, monthly_return = strategy_evaluate(equity_curve, trade)

print(r)
print(monthly_return)
