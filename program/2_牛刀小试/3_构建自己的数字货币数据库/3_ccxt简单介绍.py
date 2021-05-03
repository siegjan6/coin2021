"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行

# 课程内容
通过案例介绍初步介绍ccxt的概念
"""
import pandas as pd
import ccxt
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行


# =====ccxt
# python第三方库，专门用于对接各类数字货币交易所的接口


# =====创建ccxt交易所
exchange = ccxt.okex3()  # huobipro，binance


# =====获取ticker数据
data = exchange.fetch_ticker('BTC/USDT')
# 输出结果案例分析：原始数据放在info中；会整理数据，统一输出
print(data['symbol'])
print(data['high'])
# 更换交易所；输入symbol格式统一
# 修改为免翻墙网址


# =====获取其他数据，所有交易所都是同一行代码
data = exchange.fetch_ohlcv('BTC/USDT', limit=5)  # K线数据
print(data)
data = exchange.fetch_trades('BTC/USDT', limit=5)  # trades数据
print(data)
data = exchange.fetch_order_book('BTC/USDT')  # order_book数据
print(data)


# =====ccxt介绍
# 首页：https://github.com/ccxt/ccxt，可以尝试阅读相关文档

# 支持众多交易所，一般ccxt不支持的交易所...

# ccxt会不断更新

# 详细的安装、使用之后会讲。之后获取数据、下单等有大量的使用场景。

# 番外篇：西蒙斯带读ccxt源代码，选修，推荐学习。读源码受益匪浅

# 捐赠

# 小技巧：exchange = ccxt.okex3({'verbose': True})


