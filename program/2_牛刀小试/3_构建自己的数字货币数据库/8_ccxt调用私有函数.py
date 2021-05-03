"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行

# 课程内容
介绍如何使用ccxt的私有函数
"""
import pandas as pd
import ccxt
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行


# ccxt私有函数介绍


# ===创建交易所
huobi = ccxt.huobipro()
binance = ccxt.binance()
okex = ccxt.okex3()


# ===使用私有函数获取K线数据
# OKEx
params = {
    'instrument_id': 'BTC-USDT',
    'granularity': '60',
    'start': '2020-03-19T02:00:00.000Z',
    'end': '2020-03-19T04:00:00.000Z'
}  # 需要对着文档，使用okex独有的参数

# data = okex.spot_get_instruments_instrument_id_candles(params=params)  # 拼接方式1
data = okex.spotGetInstrumentsInstrumentIdCandles(params=params)  # 拼接方式2
print(data)  # 返回结果是交易所原始结果，需要自己重新整理。
# okex历史数据抓取，也可以通过这样的方式来完成。


# huobi
params = {
    'symbol': 'eosusdt',
    'period': '15min',
    'size': 2000,
}
data = huobi.marketGetHistoryKline(params=params)
print(data)  # 返回结果是交易所原始结果，需要自己重新整理


# binance
params = {
    'symbol': 'BTCUSDT',
    'interval': '1m',
}  #
data = binance.publicGetKlines(params=params)
print(data)  # 返回的K线数据很有价值


# 为什么要使用ccxt的私有函数？
# 1. 获取原始数据
# 2. 交易所独有接口，只能通过私有函数获取


# ===使用私有函数获取合约K线数据
# okex
params = {
    'instrument_id': 'BTC-USD-200327',
    'granularity': '60',
    'start': '2020-03-19T00:00:00.000Z',
    'end': '2020-03-19T11:00:00.000Z'
}
data = okex.futuresGetInstrumentsInstrumentIdCandles(params=params)
print(data)


# binance
params = {
    'symbol': 'IOSTUSDT',
    'interval': '1m',
}  # 需要对着文档，使用okex独有的参数
data = binance.fapiPublicGetKlines(params=params)
print(data)  # 返回的K线数据很有价值


# huibipro
# 没有合约相关代码


# 自己多多尝试，会有搭积木的快感。
# 也很重要，之后的课程中，下单、撤单等，会大量使用私有函数。
