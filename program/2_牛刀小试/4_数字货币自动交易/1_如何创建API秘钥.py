"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行

# 课程内容
介绍如何在交易所创建API
"""
import pandas as pd
import ccxt
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行


# 创建ccxt的okex交易所
exchange = ccxt.okex3()

# 设置API
exchange.apiKey = ''
exchange.secret = ''
exchange.password = ''  # okex在创建第三代api的时候，需要填写一个Passphrase。这个填写到这里即可

# 获取账户信息
balance = exchange.fetch_balance()  # 现货
print(balance)

