import requests
import time
import pandas as pd
import datetime
import ccxt
import numpy as np

from configLoad import *
from Functions import *

pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)

class OkexV5Trading(object):

    def __init__(self, symbol_config, time_interval):

        self.globalConfig = Config()  # 初始化参数
        self.symbol_config = symbol_config
        self.time_interval = time_interval
        self.publicHeaders = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
        }

    def main(self):

        # =====获取需要交易币种的历史数据=====
        max_len = 1000  # 设定最多收集多少根K线，okex不能超过1440根
        symbol_candle_data = dict()  # 用于存储K线数据
        # 遍历获取币种历史数据
        for symbol in self.symbol_config.keys():
            # 获取币种的历史数据，会删除最新一行的数据

            symbol_candle_data[symbol] = fetch_okex_symbol_history_candle_data(self.symbol_config[symbol]['instrument_id'], self.time_interval, 500, max_try_amount=5)
            # print(symbol_candle_data[symbol])
            time.sleep(medium_sleep_time)

        # ===进入每次的循环
        while True:

            # =获取持仓数据
            # 初始化symbol_info，在每次循环开始时都初始化
            symbol_info_columns = ['账户权益', '持仓方向', '持仓量', '持仓收益率', '持仓收益', '持仓均价', '当前价格', '最大杠杆']
            symbol_info = pd.DataFrame(index=symbol_config.keys() ,columns=symbol_info_columns)  # 转化为dataframe , index=symbol_config.keys(),columns=symbol_info_columns

            # 更新账户信息symbol_info
            symbol_info = update_symbol_info(symbol_info, symbol_config)
            print('\nsymbol_info:\n', symbol_info, '\n')
            # =获取策略执行时间，并sleep至该时间
            run_time = sleep_until_run_time(self.time_interval)

            # =并行获取所有币种最近数据

            candle_num = 10  # 只获取最近candle_num根K线数据，可以获得更快的速度
            # 获取数据
            recent_candle_data = single_threading_get_data(symbol_info, symbol_config, self.time_interval,
                                                           run_time, candle_num)
            for symbol in symbol_config.keys():
                print(recent_candle_data[symbol].tail(2))

            # 将symbol_candle_data和最新获取的recent_candle_data数据合并
            for symbol in symbol_config.keys():
                df = symbol_candle_data[symbol].append(recent_candle_data[symbol], ignore_index=True)
                df.drop_duplicates(subset=['candle_begin_time_GMT8'], keep='last', inplace=True)
                df.sort_values(by='candle_begin_time_GMT8', inplace=True)  # 排序，理论上这步应该可以省略，加快速度
                df = df.iloc[-max_len:]  # 保持最大K线数量不会超过max_len个
                df.reset_index(drop=True, inplace=True)
                symbol_candle_data[symbol] = df

            # # =计算每个币种的交易信号
            symbol_signal,symbol_info = calculate_signal(symbol_info, symbol_config, symbol_candle_data)
            print('\nsymbol_info:\n', symbol_info)
            print('本周期交易计划:', symbol_signal)

            # =下单
            symbol_order = pd.DataFrame()
            # 有信号才进行下单
            if symbol_signal:
                symbol_order = single_threading_place_order(symbol_info, symbol_config,
                                                            symbol_signal)  # 单线程下单
                print('下单记录：\n', symbol_order)

                # 更新订单信息，查看是否完全成交
                time.sleep(short_sleep_time)  # 休息一段时间再更新订单信息
                symbol_order = update_order_info(symbol_config, symbol_order)
                print('更新下单记录：', '\n', symbol_order)
            #
            # 重新更新账户信息symbol_info
            time.sleep(long_sleep_time)  # 休息一段时间再更新
            symbol_info = pd.DataFrame(index=symbol_config.keys(), columns=symbol_info_columns)
            symbol_info = update_symbol_info(symbol_info, symbol_config)
            print('\nsymbol_info:\n', symbol_info, '\n')

            # 发送钉钉
            dingding_report_every_loop(symbol_info, symbol_signal, symbol_order, run_time, ['写入钉钉ID', ''])

            # 本次循环结束
            print('\n', '-' * 20, '本次循环结束，%f秒后进入下一次循环' % long_sleep_time, '-' * 20, '\n\n')
            time.sleep(long_sleep_time)


if __name__ == '__main__':

    # 更新需要交易的合约、策略参数、下单量等配置信息
    symbol_config = {
        'eth-usdt': {'instrument_id': 'ETH-USDT-210625',  # 合约代码，当更换合约的时候需要手工修改
                     'leverage': '2',  # 控制实际交易的杠杆倍数，在实际交易中可以自己修改。此处杠杆数，必须小于页面上的最大杠杆数限制
                     'strategy_name': 'bolling_new',  # 使用的策略的名称
                     'para': [390, 1.7, 0.03]},  # 策略参数
        'btc-usdt': {'instrument_id': 'BTC-USDT-210625',  # 合约代码，当更换合约的时候需要手工修改
                     'leverage': '2',  # 控制实际交易的杠杆倍数，在实际交易中可以自己修改。此处杠杆数，必须小于页面上的最大杠杆数限制
                     'strategy_name': 'bolling_new',  # 使用的策略的名称
                     'para': [350, 2.2, 0.05]},  # 策略参数
        'xrp-usdt': {'instrument_id': 'XRP-USDT-210625',  # 合约代码，当更换合约的时候需要手工修改
                     'leverage': '2',  # 控制实际交易的杠杆倍数，在实际交易中可以自己修改。此处杠杆数，必须小于页面上的最大杠杆数限制
                     'strategy_name': 'bolling_new',  # 使用的策略的名称
                     'para': [460, 4.2, 0.08]},  # 策略参数

    }

    time_interval = '1m'

    okexV5Trading = OkexV5Trading(symbol_config, time_interval)
    okexV5Trading.main()