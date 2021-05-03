from datetime import timedelta
from multiprocessing import Pool, cpu_count
from datetime import datetime
from program.少年意气_择时策略魔改小组.择时策略开发与回测 import Signals
from program.少年意气_择时策略魔改小组.择时策略开发与回测.Position import *
from program.少年意气_择时策略魔改小组.择时策略开发与回测.Evaluate import *
from program.少年意气_择时策略魔改小组.择时策略开发与回测.Function import *
from program.少年意气_择时策略魔改小组.择时策略开发与回测.Statistics import *
from functools import partial
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
# 遗传算法库
from gaft import GAEngine
from gaft.components import BinaryIndividual
from gaft.components import Population
from gaft.operators import TournamentSelection
from gaft.operators import UniformCrossover
from gaft.operators import FlipBitBigMutation

# Built-in best fitness analysis.
from gaft.analysis.fitness_store import FitnessStore
from gaft.analysis.console_output import ConsoleOutput

# =====回测固定参数
tag = ''  # 本次回测标记
description = '回测数据基于币安usdt现货的分钟数据（~-2020年8月31日），在okex的usdt本位交割合约进行交易回测。' \
              'pos:position_for_OKEx_future, equity:equity_curve_for_OKEx_USDT_future_next_open'

leverage_rate = 2
slippage = 1 / 1000  # 滑点 ，可以用百分比，也可以用固定值。建议币圈用百分比，股票用固定值
c_rate = 5 / 10000  # 手续费，commission fees，默认为万分之5。不同市场手续费的收取方法不同，对结果有影响。比如和股票就不一样。
min_margin_ratio = 1 / 100  # 最低保证金率，低于就会爆仓
symbol_face_value = {'BTC': 0.01, 'EOS': 10, 'ETH': 0.1, 'LTC': 1,  'XRP': 100}
drop_days = 10  # 币种刚刚上线10天内不交易



# =====批量遍历策略参数
# ===单次循环
def calculate_by_one_loop(para, df, signal_name, symbol, rule_type):
    _df = df.copy()
    # 计算交易信号
    _df = getattr(Signals, signal_name)(_df, para=para)
    # 计算实际持仓
    _df = position_for_OKEx_future(_df)
    # 币种上线10天之后的日期
    t = _df.iloc[0]['candle_begin_time'] + timedelta(days=drop_days)
    _df = _df[_df['candle_begin_time'] > t]
    # 计算资金曲线
    face_value = symbol_face_value[symbol]
    _df = equity_curve_for_OKEx_USDT_future_next_open(_df, slippage=slippage, c_rate=c_rate,
                                                      leverage_rate=leverage_rate,
                                                      face_value=face_value,
                                                      min_margin_ratio=min_margin_ratio)

    # 保存策略收益
    rtn = pd.DataFrame()
    rtn.loc[0, 'para'] = str(para)
    r = _df.iloc[-1]['equity_curve']
    rtn.loc[0, '累计净值'] = r  # 最终收益
    rtn.loc[0, '年化收益'], rtn.loc[0, '最大回撤'], rtn.loc[0, '年化收益回撤比'] = return_drawdown_ratio(_df)
    # 删除最大回撤为0的参数
    if rtn.loc[0, '最大回撤']<0.001 and rtn.loc[0, '年化收益']<1.01:
        rtn.loc[0, '年化收益回撤比']=0
    
    print(signal_name, symbol, rule_type, para, '策略收益：', r)
    global para_curve_df
    para_curve_df=para_curve_df.append(rtn)
    return rtn


if __name__ == '__main__':
    # 全局变量
    global para_curve_df
    
    
    
    for signal_name in ['signal_simple_bolling']:
        for symbol in ['BTC', 'ETH']:
            for rule_type in ['4H', '2H', '1H', '30T', '15T']:
                para_curve_df=pd.DataFrame()
                print(signal_name, symbol, rule_type)
                print('开始遍历该策略参数：', signal_name, symbol, rule_type)

                # ===读入数据
                df = pd.read_pickle(root_path + '/data/%s-USDT_5m.pkl' % symbol)
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
                df = df[df['candle_begin_time'] >= pd.to_datetime('2018-01-01')]
                df.reset_index(inplace=True, drop=True)

                # ===获取策略参数组合
                para_list = getattr(Signals, signal_name+'_para_list')()

                # ===并行回测
                start_time = datetime.now()  # 标记开始时间

                # 利用partial指定参数值
                part = partial(calculate_by_one_loop, df=df, signal_name=signal_name, symbol=symbol, rule_type=rule_type)

            
                
                # 将各参数范围加入para_ranges中
                para_ranges = []
                minval=np.min(para_list,axis=0)
                maxval=np.max(para_list,axis=0)
                for i in range(minval.shape[0]):
                    para_ranges.append([minval[i],maxval[i]])

                # Define population.
                indv_template = BinaryIndividual(ranges=para_ranges, eps=0.001)
                population = Population(indv_template=indv_template, size=50).init()

                # Create genetic operators.
                #selection = RouletteWheelSelection()
                selection = TournamentSelection()
                crossover = UniformCrossover(pc=0.8, pe=0.5)
                mutation = FlipBitBigMutation(pm=0.1, pbm=0.55, alpha=0.6)

                # Create genetic algorithm engine.
                # Here we pass all built-in analysis to engine constructor.
                engine = GAEngine(population=population, selection=selection,
                                crossover=crossover, mutation=mutation,
                                analysis=[ConsoleOutput, FitnessStore])

                # Define fitness function.
                @engine.fitness_register
                def fitness(indv):
                    para = indv.solution
                    return float(part(para).loc[0, '年化收益回撤比'])
                # ng:遗传代数，越大，计算结果越好，也更费算力
                engine.run(ng=100)
                
               


                # # ===输出
                para_curve_df.sort_values(by='年化收益回撤比', ascending=False, inplace=True)
                print(para_curve_df.head(10))

                # ===存储参数数据
                p = root_path + '/data/output/para/%s-%s-%s-%s-%s.csv' % (signal_name, symbol, leverage_rate, rule_type, tag)
                pd.DataFrame(columns=[description]).to_csv(p, index=False,encoding="utf_8_sig")
                para_curve_df.to_csv(p, index=False, mode='a',encoding="utf_8_sig")