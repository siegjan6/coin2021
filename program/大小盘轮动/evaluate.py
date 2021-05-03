import pandas as pd
import numpy as np


def equity_curve_for_OKEx_USDT_future_next_open(df, slippage=1/1000,c_rate=5/10000,leverage_rate=3,face_value=0.01,min_margin_ratio=1/100):
    """
    计算持仓的开始时间
    计算持仓时能买入多少张
    计算买入后剩余的钱（扣除买入手续费）
    计算卖出的手续费
    计算盈亏（滑点的计算）
    计算净值 （收盘价）
    计算最小最大净值（最高最低）计算爆仓用
    """

    df['next_open'] = df['open'].shift(-1)
    df['next_open'].fillna(value=df['close'],inplace=True)

    #开仓（开空，开多）K线
    condition1 = df['pos'] != 0
    condition2 = df['pos'] != df['pos'].shift(1)
    open_pos_condition = condition1 & condition2

    condition3 = df['pos'] != df['pos'].shift(-1)
    close_pos_condition = condition3 & condition1

    df.loc[open_pos_condition, 'start_time'] = df['candle_begin_time']
    # df['start_time'].fillna(method='ffill',inplace=True)
    df.loc[df['pos']==0, 'start_time'] = pd.NaT

    # ===计算资金曲线
    initial_cash = 10000  # 初始资金
    # ---在开仓时
    # 以开盘价计算合约数量 （当资金量大可以用5分钟均价）   :   多少张 = 价格 / 单张价格
    df.loc[open_pos_condition, 'contract_num'] = initial_cash * leverage_rate / ( face_value * df['open'])
    df['contract_num'] = np.floor(df['contract_num'])  # 取整

    df.loc[open_pos_condition,'open_pos_price'] = df['open'] * (1 + slippage * df['pos'])  # 滑点价
    df['cash'] = initial_cash - df['open_pos_price'] * face_value * df['contract_num'] * c_rate  # 剩余钱 = 保证金 （扣除手续费）

    for _ in ['contract_num', 'open_pos_price', 'cash']:
        df[_].fillna(method='ffill',inplace=True)
    df.loc[df['pos'] == 0,['contract_num', 'open_pos_price', 'cash']] = None

    #=== 在平仓时
    df.loc[close_pos_condition,'close_pos_price'] = df['next_open'] * (1 - slippage * df['pos'])
    df.loc[close_pos_condition,'close_pos_fee'] = df['close_pos_price'] * face_value * df['contract_num'] * c_rate


    #===计算利润
    # 开仓至今持仓盈亏
    df['profit'] = face_value * df['contract_num'] * (df['close'] - df['open_pos_price']) * df['pos']

    # 平仓时理论额外处理（
    df.loc[close_pos_condition, 'profit'] = face_value * df['contract_num'] * (df['close_pos_price'] - df['open_pos_price'] ) * df['pos']

    # 账户净值
    df['net_value'] = df['cash'] + df['profit']

    #计算爆仓
    df.loc[df['pos'] == 1, 'price_min'] = df['low']
    df.loc[df['pos'] == -1, 'price_min'] = df['high']
    df['profit_min'] = face_value * df['contract_num'] * (df['price_min'] - df['open_pos_price']) * df['pos']
    #账户最小净值
    df['net_value_min'] = df['cash'] + df['profit_min']
    #计算保证金
    df['margin_ratio'] = df['net_value_min'] / (face_value * df['contract_num'] * df['price_min'])
    #是否爆仓
    df.loc[df['margin_ratio'] <= (min_margin_ratio+c_rate),'是否爆仓'] = 1

    #平仓时扣除手续费
    df.loc[close_pos_condition,'net_value'] -= df['close_pos_fee']

    df['是否爆仓'] = df.groupby('start_time')['是否爆仓'].fillna(method='ffill')
    df.loc[df['是否爆仓'] == 1, 'net_value'] = 0

    df['equity_change'] = df['net_value'].pct_change()
    df.loc[open_pos_condition, 'equity_change'] = df.loc[open_pos_condition, 'net_value'] / initial_cash - 1  # 开仓日的收益率
    df['equity_change'].fillna(value=0, inplace=True)
    df['equity_curve'] = (1 + df['equity_change']).cumprod()

    # =====删除不必要的数据，并存储
    df.drop(['next_open', 'contract_num', 'open_pos_price', 'cash', 'close_pos_price', 'close_pos_fee',
             'profit', 'net_value', 'price_min', 'profit_min', 'net_value_min', 'margin_ratio', '是否爆仓'],
            axis=1, inplace=True)

    print(df)
    return df

