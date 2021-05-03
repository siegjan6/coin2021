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


def update_symbol_info(exchange, symbol_info, quarterly_symbols_ID):
    """
    本函数通过ccxt_fetch_future_account()获取合约账户信息，ccxt_fetch_future_position()获取合约账户持仓信息，并用这些信息更新symbol_config
    :param exchange:
    :param symbol_info:
    :param symbol_config:
    :return:
    """
    future_info = exchange.futures_get_accounts()['info']
    df = pd.DataFrame(future_info, dtype=float).T  # 将数据转化为df格式
    exit()
    # # 通过交易所接口获取合约账户信息
    # future_account = ccxt_fetch_future_account(exchange)
    # # 将账户信息和symbol_info合并
    # if future_account.empty is False:
    #     symbol_info['账户权益'] = future_account['equity']
    #
    # # 通过交易所接口获取合约账户持仓信息
    # future_position = ccxt_fetch_future_position(exchange)
    # # 将持仓信息和symbol_info合并
    # if future_position.empty is False:
    #     # 去除无关持仓：账户中可能存在其他合约的持仓信息，这些合约不在symbol_config中，将其删除。
    #     instrument_id_list = [symbol_config[x]['instrument_id'] for x in symbol_config.keys()]
    #     future_position = future_position[future_position.instrument_id.isin(instrument_id_list)]
    #
    #     # 从future_position中获取原始数据
    #     symbol_info['最大杠杆'] = future_position['leverage']
    #     symbol_info['当前价格'] = future_position['last']
    #
    #     symbol_info['多头持仓量'] = future_position['long_qty']
    #     symbol_info['多头均价'] = future_position['long_avg_cost']
    #     symbol_info['多头收益率'] = future_position['long_pnl_ratio']
    #     symbol_info['多头收益'] = future_position['long_pnl']
    #
    #     symbol_info['空头持仓量'] = future_position['short_qty']
    #     symbol_info['空头均价'] = future_position['short_avg_cost']
    #     symbol_info['空头收益率'] = future_position['short_pnl_ratio']
    #     symbol_info['空头收益'] = future_position['short_pnl']
    #
    #     # 检验是否同时持有多头和空头
    #     temp = symbol_info[(symbol_info['多头持仓量'] > 0) & (symbol_info['空头持仓量'] > 0)]
    #     if temp.empty is False:
    #         print(list(temp.index), '当前账户同时存在多仓和空仓，请平掉其中至少一个仓位后再运行程序，程序exit')
    #         exit()
    #
    #     # 整理原始数据，计算需要的数据
    #     # 多头、空头的index
    #     long_index = symbol_info[symbol_info['多头持仓量'] > 0].index
    #     short_index = symbol_info[symbol_info['空头持仓量'] > 0].index
    #     # 账户持仓方向
    #     symbol_info.loc[long_index, '持仓方向'] = 1
    #     symbol_info.loc[short_index, '持仓方向'] = -1
    #     symbol_info['持仓方向'].fillna(value=0, inplace=True)
    #     # 账户持仓量
    #     symbol_info.loc[long_index, '持仓量'] = symbol_info['多头持仓量']
    #     symbol_info.loc[short_index, '持仓量'] = symbol_info['空头持仓量']
    #     # 持仓均价
    #     symbol_info.loc[long_index, '持仓均价'] = symbol_info['多头均价']
    #     symbol_info.loc[short_index, '持仓均价'] = symbol_info['空头均价']
    #     # 持仓收益率
    #     symbol_info.loc[long_index, '持仓收益率'] = symbol_info['多头收益率']
    #     symbol_info.loc[short_index, '持仓收益率'] = symbol_info['空头收益率']
    #     # 持仓收益
    #     symbol_info.loc[long_index, '持仓收益'] = symbol_info['多头收益']
    #     symbol_info.loc[short_index, '持仓收益'] = symbol_info['空头收益']
    #     # 删除不必要的列
    #     symbol_info.drop(['多头持仓量', '多头均价', '空头持仓量', '空头均价', '多头收益率', '空头收益率', '多头收益', '空头收益'],
    #                      axis=1, inplace=True)
    # else:
    #     # 当future_position为空时，将持仓方向的控制填充为0，防止之后判定信号时出错
    #     symbol_info['持仓方向'].fillna(value=0, inplace=True)
    #
    # return symbol_info