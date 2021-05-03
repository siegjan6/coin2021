"""
《邢不行-2020新版|Python数字货币量化投资课程》
择时策略魔改研究小组（第1期）
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9585
本程序作者: 邢不行
"""

from program.少年意气_择时策略魔改小组.择时策略开发与回测.Function import *
from program.少年意气_择时策略魔改小组.择时策略开发与回测.Statistics import *
import glob
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 500)  # 最多显示数据的行数


# 策略名称
strategy_name = 'signal_simple_bolling'  # signal_simple_bolling signal_xingbuxing

# 每个币种、时间周期的策略数量
strategy_num = 3

# 遍历所有策略结果
rtn = pd.DataFrame()
path_list = glob.glob(root_path + '/data/output/para/*.csv')  # python自带的库，或者某文件夹中所有csv文件的路径
for path in path_list:

    if strategy_name not in path:
        continue

    # 读取最优参数，选择排名前strategy_num的
    df = pd.read_csv(path, skiprows=1, nrows=strategy_num)

    df['strategy_name'] = strategy_name
    filename = path.split('/')[-1][:-4]
    df['symbol'] = filename.split('-')[1]
    df['leverage'] = filename.split('-')[2]
    df['周期'] = filename.split('-')[3]
    df['tag'] = filename.split('-')[4]

    rtn = rtn.append(df, ignore_index=True)

# 输出策略详细结果
rtn = rtn[['strategy_name', 'symbol', '周期', 'leverage', 'para', '累计净值', '年化收益', '最大回撤', '年化收益回撤比']]
rtn.sort_values(by=['strategy_name', 'symbol', '周期', '年化收益回撤比'], ascending=[1, 1, 1, 0], inplace=True)
print(rtn)
rtn.to_csv(root_path + '/data/所有策略最优参数.csv', index=False)

# 输出策略
summary = rtn.groupby(['strategy_name', 'symbol'])[['年化收益回撤比']].mean().reset_index()
print(summary)
summary.to_csv(root_path + '/data/策略总体评价.csv', index=False)
