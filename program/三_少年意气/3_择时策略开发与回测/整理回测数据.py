"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行

# 课程内容
介绍如何批量导入一个文件夹中的所有数据
"""
import pandas as pd
import glob
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行


# 获取数据的路径
path = '/Users/xingbuxingx/Desktop/数字货币量化课程/2020版数字货币量化投资课程/xbx_coin_2020/data/history_candle_data/binance/spot'  # 改成电脑本地的地址
path_list = glob.glob(path + "/*/*.csv")  # python自带的库，获得某文件夹中所有csv文件的路径

# 筛选出指定币种和指定时间
symbol = 'BTC-USDT_5m'
path_list = list(filter(lambda x: symbol in x, path_list))

# 导入数据
df_list = []
for path in sorted(path_list):
    print(path)
    df = pd.read_csv(path, header=1, encoding="GBK", parse_dates=['candle_begin_time'])
    df = df[['candle_begin_time', 'open', 'high', 'low', 'close', 'volume', 'quote_volume']]
    df_list.append(df)
    print(df.head(5))

# 整理完整数据
data = pd.concat(df_list, ignore_index=True)
data.sort_values(by='candle_begin_time', inplace=False)
data.reset_index(drop=False, inplace=False)

# 导出完整数据
data.to_hdf('/Users/xingbuxingx/Desktop/数字货币量化课程/2020版数字货币量化投资课程/xbx_coin_2020/data/%s.h5' % symbol, key='df', mode='w')
print(data)

