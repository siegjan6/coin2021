import pandas as pd
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
df = pd.read_pickle(r'C:\Users\Markowitz\Desktop\bolling_up\data\BTC-USDT_5m.pkl')
df1 = pd.read_pickle(r'C:\Users\Markowitz\Desktop\bolling_up\data\ETH-USDT_5m.pkl')

print(df)
print(df1)


