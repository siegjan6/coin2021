import glob
from datetime import timedelta
from program.少年意气_择时策略魔改小组.择时策略开发与回测 import Signals
from program.少年意气_择时策略魔改小组.择时策略开发与回测.Position import *
from program.少年意气_择时策略魔改小组.择时策略开发与回测.Evaluate import *
from program.少年意气_择时策略魔改小组.择时策略开发与回测.Function import *
from program.少年意气_择时策略魔改小组.择时策略开发与回测.Statistics import *
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 500)  # 最多显示数据的行数



path = r'C:\Users\jan\Documents\xingbuxing\coin2020\data\spot'  # 改成电脑本地的地址
path_list = glob.glob(path + "/*/*.csv")  # python自带的库，获得某文件夹中所有csv文件的路径
symbols = path
# 筛选出指定币种和指定时间
symbol = 'CHZ-USDT_5m'
path_list = list(filter(lambda x: symbol in x, path_list))


# =====读入数据
print(root_path + '/data/%s.pkl' % symbol)
df = pd.read_pickle(root_path + '/data/%s.pkl' % symbol)
# 任何原始数据读入都进行一下排序、去重，以防万一
df.sort_values(by=['candle_begin_time'], inplace=True)
df.drop_duplicates(subset=['candle_begin_time'], inplace=True)
df.reset_index(inplace=True, drop=True)

# =====转换为其他分钟数据
period_df = df.resample(rule=rule_type, on='candle_begin_time', label='left', closed='left').agg(
    {'open': 'first',
     'high': 'max',
     'low': 'min',
     'close': 'last',
     'volume': 'sum',
     'quote_volume': 'sum',
     'trade_num': 'sum',
     'taker_buy_base_asset_volume': 'sum',
     'taker_buy_quote_asset_volume': 'sum',
     })
period_df.dropna(subset=['open'], inplace=True)  # 去除一天都没有交易的周期
period_df = period_df[period_df['volume'] > 0]  # 去除成交量为0的交易周期
period_df.reset_index(inplace=True)
df = period_df[['candle_begin_time', 'open', 'high', 'low', 'close', 'volume', 'quote_volume', 'trade_num',
                'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume']]
df = df[df['candle_begin_time'] >= pd.to_datetime('2017-01-01')]
df.reset_index(inplace=True, drop=True)


# =====计算交易信号
df = getattr(Signals, signal_name)(df, para=para)

# =====计算实际持仓
df = position_for_OKEx_future(df)


# =====计算资金曲线
# 选取相关时间。币种上线10天之后的日期
t = df.iloc[0]['candle_begin_time'] + timedelta(days=drop_days)
df = df[df['candle_begin_time'] > t]

df = df[df['candle_begin_time'] >= pd.to_datetime('2018-01-01')]
# print(df)
# exit()

# 计算资金曲线
face_value = symbol_face_value[symbol.split('-')[0]]
df = equity_curve_for_OKEx_USDT_future_next_open(df, slippage=slippage, c_rate=c_rate, leverage_rate=leverage_rate,
                                                 face_value=face_value, min_margin_ratio=min_margin_ratio)
print(df)
print('策略最终收益：', df.iloc[-1]['equity_curve'])
# 输出资金曲线文件
df_output = df[['candle_begin_time', 'open', 'high', 'low', 'close', 'signal', 'pos', 'quote_volume', 'median', 'upper', 'lower', 'equity_curve']]
df_output.rename(columns={'median': 'line_median', 'upper': 'line_upper', 'lower': 'line_lower', 'quote_volume': 'b_bar_quote_volume',
                          'equity_curve': 'r_line_equity_curve'}, inplace=True)
df_output.to_csv(root_path + '/data/output/equity_curve/%s_%s_%s_%s.csv' % (signal_name, symbol.split('-')[0],
                                                                            rule_type, str(para)), index=False)

# =====策略评价
# 计算每笔交易
trade = transfer_equity_curve_to_trade(df)
print('逐笔交易：\n', trade)


# 计算各类统计指标
r, monthly_return = strategy_evaluate(df, trade)
print(r)
print(monthly_return)
