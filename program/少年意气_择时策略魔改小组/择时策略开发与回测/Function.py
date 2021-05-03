"""
《邢不行-2020新版|Python数字货币量化投资课程》
择时策略魔改研究小组（第1期）
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9585
本程序作者: 邢不行
"""
import os

# 获取项目根目录
_ = os.path.abspath(os.path.dirname(__file__))  # 返回当前文件路径

root_path = os.path.abspath(os.path.join(_, '../../..'))  # 返回根目录文件夹


# dir = os.path.dirname(__file__)
# dir = os.path.abspath(dir)
# dir = os.path.join(dir,'../../..')
# dir = os.path.abspath(dir)
#
# print(dir)


def gen_echarts_data(df_klines, df_trade, signal_name, symbol, rule_type):
    df_klines = df_klines.copy()
    df_trade = df_trade.copy()

    df_klines = df_klines[['candle_begin_time', 'open', 'close', 'low', 'high', 'median', 'upper', 'lower']]
    df_klines['candle_begin_time'] = df_klines['candle_begin_time'].apply(str)
    kdata_list = df_klines.values.tolist()

    df_trade.reset_index(drop=False, inplace=True)
    df_trade = df_trade.rename(columns={"index": "start_bar"})
    df_trade = df_trade[['signal', 'change', 'start_bar', 'end_bar', 'start_price', 'end_price']]
    df_trade['change'] = df_trade['change'].apply(lambda x: str(round(x * 100, 2)) + "%")
    df_trade['start_bar'] = df_trade['start_bar'].apply(str)
    df_trade['end_bar'] = df_trade['end_bar'].apply(str)
    df_trade['signal'] = df_trade['signal'].apply(int)
    arry_list = df_trade.values.tolist()

    js_file = root_path + '/data/output/echarts_data.js'

    with open(js_file, 'w') as f:
        f.write("var chart_title = '{}_{}_{}';\n".format(signal_name, symbol.split('-')[0], rule_type))
        f.write("\n\n")
        f.write("// format [date, open, close, low, high, median, upper, lower]\n")
        f.write("var kdata = {};\n".format(kdata_list))
        f.write("\n\n")
        f.write("// format [signal, change%, start_bar, end_bar, start_price, end_price]\n")
        f.write("var trade_data = {};\n".format(arry_list))