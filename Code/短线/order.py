import ccxt
import time
import pandas as pd
from Code.config import *
#  ======参数=======
from Code.config.configLoad import *

coin = 'CHZ'.upper()
symbol = coin + 'USDT'

side = 'BUY'
# price = 99999  # 卖1价

executePrice = 20  # USDT 总投入
profit = 0.01
stop = 0.01
future_fee_rate = 4 / 10000  # 根据自己的手续费进行修改。如果是bnb支付，可以修改为0。
coin_precision = 5


ex = ccxt.binance()
ex.apiKey = apiKey
ex.secret = secret

askPrice = ex.fapiPublicGetTickerBookTicker(params={'symbol': symbol})['askPrice']
askPrice = float(askPrice)
price = askPrice
future_coin_num = executePrice / float(askPrice)  # 合约对应币数量
future_coin_num = round(future_coin_num, 0)
fee = future_fee_rate * future_coin_num  # 手续费


# 确定下单参数
# 开多

def adjustPrice(price, precision, rate = 0.98):
    price = float(price) * rate
    return round(price, precision)


params = {'side': side, 'positionSide': 'LONG', 'symbol': symbol, 'type': 'LIMIT', 'price': adjustPrice(askPrice, coin_precision, 1.02),
          'quantity': future_coin_num, 'timeInForce': 'GTC', 'timestamp': int(time.time() * 1000)}

# print(params)
# order_info = ex.fapiPrivatePostOrder(params)
# print('币安合约交易下单成功：', symbol, '开多', askPrice, future_coin_num)
# print('下单信息：', order_info, '\n')


time.sleep(2)
df = ex.fetch_balance(params={'type': 'future'})  # delivery 币本位 ，future U本位
df = pd.DataFrame(df['info']['positions'],dtype=float)
df = df[df['symbol'] == 'CHZUSDT']
df = df[df['positionSide'] == 'LONG']
df.reset_index(inplace=True)
num = int(df.at[0, 'positionAmt'])
entryPrice = float(df.at[0, 'entryPrice'])
price = entryPrice
profitPrice = entryPrice + entryPrice * profit
stopPrice = entryPrice - entryPrice * stop

print('持有币数量：', num)
print('profitPrice：', profitPrice)
print('stopPrice：', stopPrice)

while True:
    lastPrice = ex.fapiPublicGetTickerBookTicker(params={'symbol': symbol})['askPrice']
    lastPrice = float(lastPrice)
    if lastPrice >= profitPrice:
        print('触发条件开始止盈：', lastPrice)
        exit()
        params = {
            'symbol': symbol,
            'side': 'SELL',
            'type': 'LIMIT',
            'positionSide': 'LONG',
            'price': adjustPrice(lastPrice, coin_precision),
            'quantity': num,
            'timeInForce': 'GTC',
            'timestamp': int(time.time() * 1000)
        }
        order_info = ex.fapiPrivatePostOrder(params)
        print('币安合约交易下单成功：', symbol, '平多', lastPrice, future_coin_num)
        print('下单信息：', order_info, '\n')
    elif lastPrice <= stopPrice:
        print('触发条件开始止损：', lastPrice)
        params = {
            'symbol': symbol,
            'side': 'SELL',
            'type': 'LIMIT',
            'positionSide': 'LONG',
            'price': adjustPrice(lastPrice, coin_precision),
            'quantity': num,
            'timeInForce': 'GTC',
            'timestamp': int(time.time() * 1000)
        }
        order_info = ex.fapiPrivatePostOrder(params)
        print('币安合约交易下单成功：', symbol, '平多', lastPrice, future_coin_num)
        print('下单信息：', order_info, '\n')
        exit()
    else:
        print('成本价格：%.4f，当前价格：%.4f，价差：%.4f%%' % (float(price), float(lastPrice), (lastPrice / price - 1) * 100))
        time.sleep(ex.rateLimit / 500)
