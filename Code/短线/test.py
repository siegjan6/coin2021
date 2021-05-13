import os, sys
from order import *

if sys.platform != 'win32':
    sys.path.append('/root/coin2021')
import pandas as pd
import ccxt
from datetime import timedelta
import Code.base.wechat as wechat
from Code.config.configLoad import *
from program.三_少年意气.番外1_币安u本位择时策略实盘.Config import *

pd.set_option('display.max_rows', 1000)
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.unicode.ambiguous_as_wide', True)  # 设置命令行输出时的列对齐功能
pd.set_option('display.unicode.east_asian_width', True)

BINANCE_CONFIG = {
    'apiKey': apiKey171,
    'secret': secret171}
exchange = ccxt.binance(BINANCE_CONFIG)  # 交易所api

df = exchange.fetch_ohlcv('BAT/USDT')
df = pd.DataFrame(df, dtype=float)  # 将数据转换为dataframe
df.rename(columns={0: 'MTS', 1: 'open', 2: 'high',
                   3: 'low', 4: 'close', 5: 'volume'}, inplace=True)  # 重命名
df['candle_begin_time'] = pd.to_datetime(df['MTS'], unit='ms')  # 整理时间
df['candle_begin_time_GMT8'] = df['candle_begin_time'] + timedelta(hours=8)  # 北京时间
df = df[['candle_begin_time_GMT8', 'open', 'high', 'low', 'close', 'volume']]  # 整理列的顺序
curPrice = df.iat[-1, 4]
stopPrice = curPrice - curPrice * 0.05

symbol = 'BAT/USDT'
market = exchange.market(symbol)
amount = 10

price = curPrice + curPrice * 0.05
stop_price =  curPrice * 0.99
stop_limit_price = price * 1.01

response = exchange.private_post_order_oco({
    'symbol': market['id'],
    'side': 'SELL',  # SELL, BUY
    'quantity': exchange.amount_to_precision(symbol, amount),
    'price': exchange.price_to_precision(symbol, price),
    'stopPrice': exchange.price_to_precision(symbol, stop_price),
    'stopLimitPrice': exchange.price_to_precision(symbol, stop_limit_price),  # If provided, stopLimitTimeInForce is required
    'stopLimitTimeInForce': 'GTC',  # GTC, FOK, IOC
    # 'listClientOrderId': exchange.uuid(),  # A unique Id for the entire orderList
    # 'limitClientOrderId': exchange.uuid(),  # A unique Id for the limit order
    # 'limitIcebergQty': exchangea.amount_to_precision(symbol, limit_iceberg_quantity),
    # 'stopClientOrderId': exchange.uuid()  # A unique Id for the stop loss/stop loss limit leg
    # 'stopIcebergQty': exchange.amount_to_precision(symbol, stop_iceberg_quantity),
    # 'newOrderRespType': 'ACK',  # ACK, RESULT, FULL
})
print(response)