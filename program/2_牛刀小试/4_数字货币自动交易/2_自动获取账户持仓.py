"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行

# 课程内容
获取各个交易所的账户持仓数据
"""
import pandas as pd
import ccxt
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行


# =====okex交易所
# ===创建交易所
exchange = ccxt.okex3()  # 此处是okex第三代api接口，所以是okex3
exchange.apiKey = ''
exchange.secret = ''
exchange.password = ''  # okex在创建第三代api的时候，需要填写一个Passphrase。这个填写到这里即可

# ===通过fetch_balance获取账户信息
balance = exchange.fetch_balance()  # 现货
balance = exchange.fetch_balance(params={'type': 'margin'})  # 杠杆账户
balance = exchange.fetch_balance(params={'type': 'swap'})  # 永续账户
balance = exchange.fetch_balance(params={'type': 'futures'})  # 交割合约账户

# ===通过ccxt私有函数获取现货账户
balance = exchange.spotGetAccounts()  # 所有账户
params = {'currency': 'eos'}
balance = exchange.spotGetAccountsCurrency(params=params)  # 指定币种

# ===通过ccxt私有函数获取永续账户
balance = exchange.swapGetAccounts()  # 所有账户
position = exchange.swapGetPosition()  # 所有持仓
params = {'instrument_id': 'BTC-USD-SWAP'}
balance = exchange.swapGetInstrumentIdAccounts(params=params)  # 指定账户
position = exchange.swapGetInstrumentIdPosition(params=params)  # 指定持仓

# ===通过ccxt私有函数获取杠杆账户、交割合约账户
# 自己尝试获取


# =====binance交易所
# ===创建交易所
exchange = ccxt.binance()
exchange.apiKey = ''
exchange.secret = ''

# ===通过fetch_balance获取账户信息
balance = exchange.fetch_balance()  # 现货账户
balance = exchange.fetch_balance(params={'type': 'margin'})

# ===通过ccxt私有函数获现货账户数据
balance = exchange.privateGetAccount()
# ===通过ccxt私有函数获取杠杆账户数据
balance = exchange.sapiGetMarginAccount()
# ===通过ccxt私有函数获取合约账户数据
balance = exchange.fapiPrivateGetAccount()


# =====火币交易所
# 自己尝试获取

