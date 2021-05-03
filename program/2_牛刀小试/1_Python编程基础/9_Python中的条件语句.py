"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行/西蒙斯

# 课程内容
- 条件语句介绍
- 条件语句示例

功能：本程序主要介绍python的条件语句。希望以后大家只要看这个程序，就能回想起相关的基础知识。
"""

# =====先来个段子
"""
# 原题
程序员老婆："出去买6个苹果，如果看到西瓜，买一个回来";
结果程序员买了一个苹果回家。

# 解析
程序员理解方式如下：（伪代码）
---
product = '苹果'
amount = 6
other_product = '西瓜'

if other_product.exists():
    amount = 1

buy(product, amount)
---
Result: '西瓜' * 1
"""

# =====条件语句介绍
# 条件语句语法如下：
"""
if 条件A（结果为布尔值，True或者False）:
    执行相关操作1（需要使用tab缩进）
    ......

elif 条件B（结果为布尔值，True或者False）:
    执行相关操作2
    ......
else:
    执行相关操作3
"""

# 条件语句解释说明如下：
"""
1. 若条件A为True，那么执行相关操作1，程序结束
2. 若条件A为False，那么判断条件B，若条件B为True，那么执行相关操作2，程序结束
3. 若条件A为False，那么判断条件B，若条件B为False，那么执行相关操作3，程序结束
"""

# 条件语句示例：根据symbol代码，判断币的计价单位
# symbol = 'xrpbtc'  # 尝试将symbol改成'xrpbtc'，'xrpeth', 'xrpbnb'看相关结果。
# if symbol.endswith('usdt'):
#     print(symbol, '以USDT计价')
# elif symbol.endswith('btc'):
#     pass
# elif symbol.endswith('eth'):
#     print(symbol, '以以太坊计价')
# else:
#     print(symbol, '不知道以什么计价')


# 条件语句示例：高级写法
"""
# 口语化的条件表达
变量名 = 满足条件时候要显示的内容 if 条件 else 不满足条件的时候要显示的内容
"""
# change = 0.1
# if change > 0:
# #     status = '上涨'
# # else:
# #     status = '没涨'

# status = '上涨' if change > 0 else '没涨'
# print(change, status)
