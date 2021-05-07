"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行

# 课程内容
介绍择时策略实盘的整体思路
"""
import pandas as pd
import ccxt
from program.三_少年意气.四_择时策略实盘初阶.Function import *


# 大象放进冰箱只需要3步。


# =====配置运行相关参数=====
exchange = ccxt.okex()  # 交易所api
time_interval = '15m'  # 目前支持5m，15m，30m，1h，2h等
# 以及其他各类参数，例如钉钉id等


# =====配置交易相关参数=====
# symbol_config，更新需要交易的合约、策略参数、下单量等配置信息
symbol_config = {
    'eth-usdt': {'instrument_id': 'ETH-USDT-200626',  # 合约代码，当更换合约的时候需要手工修改
                 'leverage': '3',  # 控制实际交易的杠杆倍数，在实际交易中可以自己修改。此处杠杆数，必须小于页面上的最大杠杆数限制
                 'strategy_name': 'real_signal_random',  # 使用的策略的名称
                 'para': [10]},  # 策略参数
    'eos-usdt': {'instrument_id': 'EOS-USDT-200327',
                 'leverage': '3',
                 'strategy_name': 'real_signal_simple_bolling',  # 不同币种可以使用不同的策略
                 'para': [20, 2]},
}


# =====获取需要交易币种的历史数据=====
# 因为okex每次最多只能获取300根K线数据，不能满足有些策略的参数需求。
# 但是OKEx可以根据k线开始的时间，获取之前的k线，最多可以获取1440根k线数据。大致可以满足我们的需求。
# 所以需要在程序刚开始运行的时候，不断获取300K根K线，并且往前推，总共获取1440根K线数据。
# 如果参数超过1440，那么需要使用本地文件存储数据，逻辑相同。
symbol_candle_data = {
    'eth-usdt': pd.DataFrame(),  # 此处的交易对，要和symbol_config中一一对应
    'eos-usdt': pd.DataFrame()
}  # 是一个dict，用于存放每个币种的1440根K线数据


# =====在每根K线结束时，进行一次循环，无穷无尽=====
while True:

    # ===获取持仓数据===
    # 通过update_symbol_info()函数，从okex获取目前账户的持仓数据
    symbol_info = update_symbol_info()
    # symbol_info样例：
    #             账户权益       可转资金    持仓方向  持仓量  持仓收益率  持仓收益   持仓均价   当前价格
    # eos-usdt    32.230619    28.631619    -1     100   0.002778  0.010    3.6000    3.605
    # eth-usdt   27.8543325   25.6097325    -1     100   0.051855  0.117    225.6300  224.340

    # ===根据当前时间，获取策略下次执行时间，例如16:45。并sleep至该时间===
    run_time = sleep_until_run_time()
    #  run_time输出案例：2020-03-01 16:45:00

    # ===获取所有币种最近数据===
    # 因为我们之前已经获取了带有所有历史数据的symbol_candle_data，所以再每次循环的时候，只需获取最近candle_num根K线数据，可以获得更快的速度
    candle_num = 10  # 理论上只需要2根，冗余
    # 逐个获取每个交易对的K线数据
    recent_candle_data = single_threading_get_data(candle_num)  # 当跑多个币种的时候，例如6个，逐个获取速度会很慢，影响后续的交易，所以可以并行，第四章可能会讲。
    # 将symbol_candle_data和最新获取的recent_candle_data合并，组成完整数据，放到symbol_candle_data中
    # 并删除symbol_candle_data中一些老的数据，防止程序运行一段时间后，数据过于庞大

    # ===计算每个币种的交易信号===
    # 根据策略逐个计算每个交易对的信号
    symbol_signal = calculate_signal()  # 一般来说，计算信号的速度较快，逐个币种串行计算信号即可。有需要也可以改成并行，加快速度。
    # symbol_signal输出案例，有信号时：{'eth-usdt': [4], 'eos-usdt': [4, 1]}。注意，一个币种可能同时发出两个信号
    # symbol_signal输出案例，无信号时：{}

    # ===下单===
    if symbol_signal:
        # 根据交易信号，逐个下单
        symbol_order = single_threading_place_order()  # 逐个下单稍慢，需要并行，第四章可能会讲。
        # symbol_order输出案例：
        #      订单号         symbol   信号价格         信号时间
        # 4477216442563585  eos-usdt  3.5740  2020-03-01 16:55:00.883864
        # 4477216441472001  eth-usdt  233.98  2020-03-01 16:55:00.996635

        # 根据订单号，查询是否成交
        symbol_order = update_order_info()  # 根据订单id，查询订单成交情况
        # symbol_order输出案例：
        #      订单号         symbol   信号价格     信号时间 订单状态 开仓方向 委托数量 成交数量 委托价格 成交均价  委托时间
        # 4477216442563585  eos-usdt  3.5740 16:55:00.8  完全成交  平空    100     100   3.645  3.582  08:55:01.300Z
        # 4477216441472001  xrp-usdt  0.2339 16:55:00.9  完全成交  平空    100     100   0.2385 0.2341 08:55:01.280Z

    # ===下单完成之后，再次更新通过update_symbol_info()函数，从okex获取目前账户的持仓数据===
    symbol_info = update_symbol_info()

    # ===通过钉钉发送策略报告===
    dingding_report_every_loop()

    # 本次循环结束


"""

重要的几个全局变量。整个程序就是围绕这几个变量进行的。

1. 手工配置的symbol_config，更新需要交易的合约、策略参数、下单量等配置信息
symbol_config = {
    'btc-usdt': {'instrument_id': 'BTC-USDT-200327',  # 合约代码
                 'size': '100',  # 下单数量，注意此处是合约张数
                 'leverage': '10',  # 此处杠杆数，必须和页面上设置的相同。
                 'strategy_name': 'real_signal_random',  # 使用的策略的名称
                 "para": [10, 1, 5]},  # 算法参数分别为
    'eos-usdt': {'instrument_id': 'EOS-USDT-200327',
                 'size': '100',  # 每张合约对应0.1个eos，大约30美金
                 'leverage': '10',
                 'strategy_name': 'signal_bolling_with_stop_lose',  # 使用的策略的名称
                 "para": [20, 2, 5]},
}


2. 保存持仓信息的symbol_info
            账户权益       可转资金    持仓方向  持仓量  持仓收益率  持仓收益   持仓均价   当前价格
eos-usdt    32.230619    28.631619    -1     100   0.002778  0.010    3.6000    3.605
eth-usdt   27.8543325   25.6097325    -1     100   0.051855  0.117    225.6300  224.340


3. 保存数据的symbol_candle_data
symbol_candle_data = {
    'btc-usdt': pd.DataFrame(),
    'eos-usdt': pd.DataFrame()


4. 保存交易信号的symbol_signal
symbol_signal输出案例：{'eth-usdt': [4], 'eth-usdt': [4, 1]}


5. 保存订单执行信息的symbol_order：
     订单号         symbol   信号价格     信号时间 订单状态 开仓方向 委托数量 成交数量 委托价格 成交均价  委托时间
4477216442563585  eos-usdt  3.5740 16:55:00.8  完全成交  平空    100     100   3.645  3.582  08:55:01.300Z
4477216441472001  xrp-usdt  0.2339 16:55:00.9  完全成交  平空    100     100   0.2385 0.2341 08:55:01.280Z

"""