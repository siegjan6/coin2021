"""
邢不行2021策略分享会
币安期现套利程序
邢不行微信：xbx3636
"""
import pandas as pd
import time

pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option("display.max_rows", 500)


# 在币币账户下单
def binance_spot_place_order(exchange, symbol, long_or_short, price, amount):
    """
    :param exchange:  ccxt交易所
    :param symbol: 币币交易对代码，例如'BTC/USDT'
    :param long_or_short:  两种类型：买入、卖出
    :param price:  下单价格
    :param amount:  下单数量
    :return:
    """

    for i in range(5):
        try:
            # 买
            if long_or_short == '买入':
                order_info = exchange.create_limit_buy_order(symbol, amount, price)  # 买单
            # 卖
            elif long_or_short == '卖出':
                order_info = exchange.create_limit_sell_order(symbol, amount, price)  # 卖单
            else:
                raise ValueError('long_or_short只能是：`买入`或者`卖出`')

            print('binance币币交易下单成功：', symbol, long_or_short, price, amount)
            print('下单信息：', order_info, '\n')
            return order_info

        except Exception as e:
            print('binance币币交易下单报错，1s后重试', e)
            time.sleep(1)

    print('binance币币交易下单报错次数过多，程序终止')
    exit()


# 在期货合约账户下限价单
def binance_future_place_order(exchange, symbol, long_or_short, price, amount):
    """
    :param exchange:  ccxt交易所
    :param symbol: 合约代码，例如'BTCUSD_210625'
    :param long_or_short:  四种类型：开多、开空、平多、平空
    :param price: 开仓价格
    :param amount: 开仓数量，这里的amount是合约张数
    :return:

    timeInForce参数的几种类型
    GTC - Good Till Cancel 成交为止
    IOC - Immediate or Cancel 无法立即成交(吃单)的部分就撤销
    FOK - Fill or Kill 无法全部立即成交就撤销
    GTX - Good Till Crossing 无法成为挂单方就撤销

    """

    if long_or_short == '开空':
        side = 'SELL'
    else:
        raise NotImplemented('long_or_short目前只支持 `开空`，请参考官方文档添加其他的情况')

    # 确定下单参数
    # 开空
    params = {
        'side': side,
        'positionSide': 'SHORT',
        'symbol': symbol,
        'type': 'LIMIT',
        'price': price,  # 下单价格
        'quantity': amount,  # 下单数量，注意此处是合约张数,
        'timeInForce': 'GTC',  # 含义见本函数注释部分
    }
    # 尝试下单
    for i in range(5):
        try:
            params['timestamp'] = int(time.time() * 1000)
            order_info = exchange.dapiPrivatePostOrder(params)
            print('币安合约交易下单成功：', symbol, long_or_short, price, amount)
            print('下单信息：', order_info, '\n')
            return order_info
        except Exception as e:
            print('币安合约交易下单报错，1s后重试...', e)
            time.sleep(1)

    print('币安合约交易下单报错次数过多，程序终止')
    exit()


# binance各个账户间转钱
def binance_account_transfer(exchange, currency, amount, from_account='币币', to_account='合约'):
    """
    """

    if from_account == '币币' and to_account == '合约':
        transfer_type = 'MAIN_CMFUTURE'
    else:
        raise ValueError('未能识别`from_account`和`to_account`的组合，请参考官方文档')

    # 构建参数
    params = {
        'type': transfer_type,
        'asset': currency,
        'amount': amount,
    }

    # 开始转账
    for i in range(5):
        try:
            params['timestamp'] = int(time.time() * 1000)
            transfer_info = exchange.sapiPostAssetTransfer(params=params)
            print('转账成功：', from_account, 'to', to_account, amount)
            print('转账信息：', transfer_info, '\n')
            return transfer_info
        except Exception as e:
            print('转账报错，1s后重试', e)
            time.sleep(1)

    print('转账报错次数过多，程序终止')
    exit()



# 在期货合约账户下限价单
def binance_future_order(exchange, symbol, long_or_short, price, amount):
    """
    :param exchange:  ccxt交易所
    :param symbol: 合约代码，例如'BTCUSD_210625'
    :param long_or_short:  四种类型：开多、开空、平多、平空
    :param price: 开仓价格
    :param amount: 开仓数量，这里的amount是合约张数
    :return:

    timeInForce参数的几种类型
    GTC - Good Till Cancel 成交为止
    IOC - Immediate or Cancel 无法立即成交(吃单)的部分就撤销
    FOK - Fill or Kill 无法全部立即成交就撤销
    GTX - Good Till Crossing 无法成为挂单方就撤销

    """

    if long_or_short == '开空':
        side = 'SELL'
    else:
        raise NotImplemented('long_or_short目前只支持 `开空`，请参考官方文档添加其他的情况')

    # 确定下单参数
    # 开空
    params = {
        'side': side,
        'positionSide': 'SHORT',
        'symbol': symbol,
        'type': 'LIMIT',
        'price': price,  # 下单价格
        'quantity': amount,  # 下单数量，注意此处是合约张数,
        'timeInForce': 'GTC',  # 含义见本函数注释部分
    }
    # 尝试下单
    for i in range(5):
        try:
            params['timestamp'] = int(time.time() * 1000)
            order_info = exchange.dapiPrivatePostOrder(params)
            print('币安合约交易下单成功：', symbol, long_or_short, price, amount)
            print('下单信息：', order_info, '\n')
            return order_info
        except Exception as e:
            print('币安合约交易下单报错，1s后重试...', e)
            time.sleep(1)

    print('币安合约交易下单报错次数过多，程序终止')
    exit()
