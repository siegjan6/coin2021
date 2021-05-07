"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行

# 课程内容
币安u本位择时策略实盘框架相关函数
"""
import ccxt
import pandas as pd
from datetime import datetime, timedelta
import time
from program.三_少年意气.番外1_币安u本位择时策略实盘.Config import *
from program.三_少年意气.番外1_币安u本位择时策略实盘 import Signals


# ==========辅助功能函数==========
# ===下次运行时间，和课程里面讲的函数是一样的
def next_run_time(time_interval, ahead_seconds=5):
    """
    根据time_interval，计算下次运行的时间，下一个整点时刻。
    目前只支持分钟和小时。
    :param time_interval: 运行的周期，15m，1h
    :param ahead_seconds: 预留的目标时间和当前时间的间隙
    :return: 下次运行的时间
    案例：
    15m  当前时间为：12:50:51  返回时间为：13:00:00
    15m  当前时间为：12:39:51  返回时间为：12:45:00
    10m  当前时间为：12:38:51  返回时间为：12:40:00
    5m  当前时间为：12:33:51  返回时间为：12:35:00
    5m  当前时间为：12:34:51  返回时间为：12:35:00

    1h  当前时间为：14:37:51  返回时间为：15:00:00
    2h  当前时间为：00:37:51  返回时间为：02:00:00

    30m  当前时间为：21日的23:33:51  返回时间为：22日的00:00:00
    5m  当前时间为：21日的23:57:51  返回时间为：22日的00:00:00

    ahead_seconds = 5
    15m  当前时间为：12:59:57  返回时间为：13:15:00，而不是 13:00:00
    """
    if time_interval.endswith('m') or time_interval.endswith('h'):
        pass
    elif time_interval.endswith('T'):
        time_interval = time_interval.replace('T', 'm')
    elif time_interval.endswith('H'):
        time_interval = time_interval.replace('H', 'h')
    else:
        print('time_interval格式不符合规范。程序exit')
        exit()

    ti = pd.to_timedelta(time_interval)
    now_time = datetime.now()
    # now_time = datetime(2019, 5, 9, 23, 50, 30)  # 指定now_time，可用于测试
    this_midnight = now_time.replace(hour=0, minute=0, second=0, microsecond=0)
    min_step = timedelta(minutes=1)

    target_time = now_time.replace(second=0, microsecond=0)

    while True:
        target_time = target_time + min_step
        delta = target_time - this_midnight
        if delta.seconds % ti.seconds == 0 and (target_time - now_time).seconds >= ahead_seconds:
            # 当符合运行周期，并且目标时间有足够大的余地，默认为60s
            break

    print('\n程序下次运行的时间：', target_time, '\n')
    return target_time


# ===依据时间间隔, 自动计算并休眠到指定时间
def sleep_until_run_time(time_interval, ahead_time=1, if_sleep=True):
    """
    根据next_run_time()函数计算出下次程序运行的时候，然后sleep至该时间
    :param time_interval:
    :param ahead_time:
    :param if_sleep:
    :return:
    """

    # 计算下次运行时间
    run_time = next_run_time(time_interval, ahead_time)

    # sleep
    if if_sleep:
        time.sleep(max(0, (run_time - datetime.now()).seconds))
        # 可以考察：print(run_time - n)、print((run_time - n).seconds)
        while True:  # 在靠近目标时间时
            if datetime.now() > run_time:
                break

    return run_time


# ==========交易所交互函数==========
# ===判断当前持仓模式
def if_oneway_mode(exchange):
    """
    判断当前合约持仓模式。必须得是单向模式。如果是双向模式，就报错。
    查询当前的持仓模式。使用函数：GET /fapi/v1/positionSide/dual (HMAC SHA256)
    判断持仓情况，False为单向持仓，True为单向持仓
    :param exchange:
    :return:
    """
    positionSide = exchange.fapiPrivateGetPositionSideDual()

    if positionSide['dualSidePosition']:
        raise ValueError("当前持仓模式为双向持仓，程序已停止运行。请去币安官网改为单向持仓。")
    else:
        print('当前持仓模式：单向持仓')


# ===获得币对精度
def usdt_future_exchange_info(exchange, symbol_config):
    """
    获取symbol_config中币种的最小下单价格、数量
    :param exchange:
    :return:
    使用接口：GET /fapi/v1/exchangeInfo
    文档：https://binance-docs.github.io/apidocs/futures/cn/#0f3f2d5ee7
    """

    # 获取u本为合约交易对的信息
    exchange_info = exchange.fapiPublic_get_exchangeinfo()

    # 转化为dataframe
    df = pd.DataFrame(exchange_info['symbols'])
    # df['最小价格单位'] = df['filters'].apply(lambda x: x[0]['minPrice'])
    # df['最小下单单位'] = df['filters'].apply(lambda x: x[1]['minQty'])
    df = df[['symbol', 'pricePrecision', 'quantityPrecision']]
    df.set_index('symbol', inplace=True)

    # 赋值
    for symbol in symbol_config.keys():
        symbol_config[symbol]['最小下单价精度'] = df.at[symbol, 'pricePrecision']

        p = df.at[symbol, 'quantityPrecision']
        symbol_config[symbol]['最小下单量精度'] = None if p == 0 else p


# ===获取当前持仓信息
def binance_update_account(exchange, symbol_config, symbol_info):
    """
    获取u本位账户的持仓信息、账户余额信息
    :param exchange:
    :param symbol_config:
    :param symbol_info:
    :return:
    接口：GET /fapi/v2/account (HMAC SHA256)
    文档：https://binance-docs.github.io/apidocs/futures/cn/#v2-user_data-2
    币安的币本位合约，不管是交割，还是永续，共享一个账户。他们的symbol不一样。比如btc的永续合约是BTCUSDT，季度合约是BTCUSDT_210625
    """
    # ===获取持仓数据===
    # 获取账户信息
    account_info = exchange.fapiPrivateGetAccount()

    # 将持仓信息转变成dataframe格式
    positions_df = pd.DataFrame(account_info['positions'], dtype=float)
    positions_df = positions_df.set_index('symbol')
    # 筛选交易的币对
    positions_df = positions_df[positions_df.index.isin(symbol_config.keys())]
    # 将账户信息转变成dataframe格式
    assets_df = pd.DataFrame(account_info['assets'], dtype=float)
    assets_df = assets_df.set_index('asset')

    # 根据持仓信息、账户信息中的值填充symbol_info
    balance = assets_df.loc['USDT', 'marginBalance']  # 保证金余额
    symbol_info['账户权益'] = balance

    symbol_info['持仓量'] = positions_df['positionAmt']
    symbol_info['持仓方向'] = symbol_info['持仓量'].apply(lambda x: 1 if float(x) > 0 else (-1 if float(x) < 0 else 0))

    symbol_info['持仓收益'] = positions_df['unrealizedProfit']
    symbol_info['持仓均价'] = positions_df['entryPrice']

    # 计算每个币种的分配资金（在无平仓的情况下）
    profit = symbol_info['持仓收益'].sum()
    symbol_info['分配资金'] = (balance - profit) * symbol_info['分配比例']

    return symbol_info


# ===通过ccxt获取K线数据
def ccxt_fetch_binance_candle_data(exchange, symbol, time_interval, limit):
    """
    获取指定币种的K线信息
    :param exchange:
    :param symbol:
    :param time_interval:
    :param limit:
    :return:
    """

    # 获取数据
    data = exchange.fapiPublic_get_klines({'symbol': symbol, 'interval': time_interval, 'limit': limit})

    # 整理数据
    df = pd.DataFrame(data, dtype=float)
    df.rename(columns={1: 'open', 2: 'high', 3: 'low', 4: 'close', 5: 'volume'}, inplace=True)
    df['candle_begin_time'] = pd.to_datetime(df[0], unit='ms')
    df['candle_begin_time_GMT8'] = df['candle_begin_time'] + timedelta(hours=8)
    df = df[['candle_begin_time_GMT8', 'open', 'high', 'low', 'close', 'volume']]

    return df


# ===单线程获取需要的K线数据，并检测质量。
def single_threading_get_binance_candle_data(exchange, symbol_config, symbol_info, time_interval, run_time, candle_num):
    """
    获取所有币种的k线数据，并初步处理
    :param exchange:
    :param symbol_config:
    :param symbol_info:
    :param time_interval:
    :param run_time:
    :param candle_num:
    :return:
    """

    symbol_candle_data = dict()  # 用于存储K线数据

    print('开始获取K线数据')
    # 遍历每一个币种
    for symbol in symbol_config.keys():
        print(symbol, '开始时间：', datetime.now(), end=' ')

        # 获取symbol该品种最新的K线数据
        df = ccxt_fetch_binance_candle_data(exchange, symbol, time_interval, limit=candle_num)

        # 如果获取数据为空，再次获取
        # if df.empty:
            # continue

        # 获取到了最新数据
        print('结束时间：', datetime.now())
        symbol_info.at[symbol, '当前价格'] = df.iloc[-1]['close']  # 该品种的最新价格
        symbol_candle_data[symbol] = df[df['candle_begin_time_GMT8'] < pd.to_datetime(run_time)]  # 去除run_time周期的数据

    return symbol_candle_data


# ==========趋势策略相关函数==========
def calculate_signal(symbol_info, symbol_config, symbol_candle_data):
    """
    计算交易信号
    :param symbol_info:
    :param symbol_config:
    :param symbol_candle_data:
    :return:
    """
    # return变量
    symbol_signal = {
        '平多': [],
        '平空': [],
        '开多': [],
        '开空': [],
        '平多开空': [],
        '平空开多': [],
    }

    # 逐个遍历交易对
    for symbol in symbol_config.keys():

        # 赋值相关数据
        df = symbol_candle_data[symbol].copy()  # 最新数据
        now_pos = symbol_info.at[symbol, '持仓方向']  # 当前持仓方向
        avg_price = symbol_info.at[symbol, '持仓均价']  # 当前持仓均价

        # 需要计算的目标仓位
        target_pos = None

        # 根据策略计算出目标交易信号。
        if not df.empty:  # 当原始数据不为空的时候
            target_pos = getattr(Signals, symbol_config[symbol]['strategy_name'])(df, now_pos, avg_price,
                                                                                  symbol_config[symbol]['para'])
            symbol_info.at[symbol, '目标持仓'] = target_pos

        # 根据目标仓位和实际仓位，计算实际操作
        if now_pos == 1 and target_pos == 0:  # 平多
            symbol_signal['平多'].append(symbol)
        elif now_pos == -1 and target_pos == 0:  # 平空
            symbol_signal['平空'].append(symbol)
        elif now_pos == 0 and target_pos == 1:  # 开多
            symbol_signal['开多'].append(symbol)
        elif now_pos == 0 and target_pos == -1:  # 开空
            symbol_signal['开空'].append(symbol)
        elif now_pos == 1 and target_pos == -1:  # 平多，开空
            symbol_signal['平多开空'].append(symbol)
        elif now_pos == -1 and target_pos == 1:  # 平空，开多
            symbol_signal['平空开多'].append(symbol)

        symbol_info.at[symbol, '信号时间'] = datetime.now()  # 计算产生信号的时间

    # 删除没有信号的操作
    for key in list(symbol_signal.keys()):
        if not symbol_signal.get(key):
            del symbol_signal[key]

    return symbol_signal


# 根据交易所的限制（最小下单单位、量等），修改下单的数量和价格
def modify_order_quantity_and_price(symbol, symbol_config, params):
    """
    根据交易所的限制（最小下单单位、量等），修改下单的数量和价格
    :param symbol:
    :param symbol_config:
    :param params:
    :return:
    """

    # 根据每个币种的精度，修改下单数量的精度
    params['quantity'] = round(params['quantity'], symbol_config[symbol]['最小下单量精度'])

    # 买单加价2%，卖单降价2%
    params['price'] = params['price'] * 1.02 if params['side'] == 'BUY' else params['price'] * 0.98
    # 根据每个币种的精度，修改下单价格的精度
    params['price'] = round(params['price'], symbol_config[symbol]['最小下单价精度'])

    return params


# 针对某个类型订单，计算下单参数。供cal_all_order_info函数调用
def cal_order_params(signal_type, symbol, symbol_info, symbol_config):
    """
    针对某个类型订单，计算下单参数。供cal_all_order_info函数调用
    :param signal_type:
    :param symbol:
    :param symbol_info:
    :param symbol_config:
    :return:
    """

    params = {
        'symbol': symbol,
        'side': binance_order_type[signal_type],
        'price': symbol_info.at[symbol, '当前价格'],
        'type': 'LIMIT',
        'timeInForce': 'GTC',
    }

    if signal_type in ['平空', '平多']:
        params['quantity'] = abs(symbol_info.at[symbol, '持仓量'])

    elif signal_type in ['开多', '开空']:
        params['quantity'] = symbol_info.at[symbol, '分配资金'] * symbol_config[symbol]['leverage'] / \
                   symbol_info.at[symbol, '当前价格']

    else:
        close_quantity = symbol_info.at[symbol, '持仓量']
        open_quantity = symbol_info.at[symbol, '分配资金'] * symbol_config[symbol]['leverage'] / \
                        symbol_info.at[symbol, '当前价格']
        params['quantity'] = close_quantity + open_quantity

    # 修改精度
    params = modify_order_quantity_and_price(symbol, symbol_config, params)

    return params


# 计算所有币种的下单参数
def cal_all_order_info(symbol_signal, symbol_info, symbol_config, exchange):
    """

    :param symbol_signal:
    :param symbol_info:
    :param symbol_config:
    :param exchange:
    :return:
    """

    symbol_order_params = []

    # 如果没有信号，跳过
    if not symbol_signal:
        print('本周期无交易指令，不执行交易操作')
        return symbol_order_params

    # 如果只有平仓，或者只有开仓，无需重新更新持仓信息symbol_info
    if set(symbol_signal.keys()).issubset(['平空', '平多']) or set(symbol_signal.keys()).issubset(['开多', '开空']):
        print('本周期只有平仓或者只有开仓交易指令，无需再次更新账户信息，直接执行交易操作')

    # 如果有其他信号，需重新更新持仓信息symbol_info，然后据此重新计算下单量
    else:
        print('本周期有复杂交易指令（例如：平开、平和开、有平和平开、有开和平开），需重新更新账户信息，再执行交易操作')

        # 更新账户信息symbol_info
        symbol_info = binance_update_account(exchange, symbol_config, symbol_info)
        print('\n更新持仓信息\n', symbol_info)

        # 标记出需要把利润算作保证金的仓位。
        for signal in symbol_signal.keys():
            for symbol in symbol_signal[signal]:
                symbol_info.at[symbol, '利润参与保证金'] = 1

        # 计算分配资金
        all_profit = symbol_info['持仓收益'].sum()  # 所有利润
        profit = (symbol_info['持仓收益'] * symbol_info['利润参与保证金']).sum()  # 参与保证金的利润
        balance = symbol_info.iloc[0]['账户权益'] - all_profit  # 初始投入资金
        balance = balance + profit  # 平仓之后的利润或损失
        symbol_info['分配资金'] = balance * symbol_info['分配比例']

    # 计算每个交易币种的各个下单参数
    for signal_type in symbol_signal.keys():
        for symbol in symbol_signal[signal_type]:
            params = cal_order_params(signal_type, symbol, symbol_info, symbol_config)

            if params['quantity'] == 0:  # 考察下单量是否为0
                print('\n', symbol, '下单量为0，忽略')
            elif params['price'] * params['quantity'] <= 5:  # 和最小下单额5美元比较
                print('\n', symbol, '下单金额小于5u，忽略')
            else:
                # 改成str
                params['price'] = str(params['price'])
                params['quantity'] = str(params['quantity'])
                symbol_order_params.append(params)

    return symbol_order_params
