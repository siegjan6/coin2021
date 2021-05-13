
import ccxt
import pandas as pd
"""
获取现货数据
             free  locked
asset                    
LTC      0.000010     0.0
BNB      0.897109     0.0
USDT     0.037928     0.0
BAT    318.220000     0.0
DOGE   101.100000     0.0
"""
def update_account(exchange):
    # 获取账户信息
    account_info = exchange.privateGetAccount()
    # 将持仓信息转变成dataframe格式
    positions_df = pd.DataFrame(account_info['balances'], dtype=float)
    positions_df = positions_df.set_index('asset')
    positions_df = positions_df[positions_df['free'] > 0]
    return positions_df

def getSymbolFree(exchange, symbol):
    df = update_account(exchange)
    if symbol in df.index.values:
        return df.at[symbol, 'free']
    return 0
