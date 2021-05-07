"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行/西蒙斯

# 本节课程内容
- 如何遍历文件夹
- 批量获取文件名
- 批量读入csv文件
- HDF5文件简介
"""

import pandas as pd
import os

pd.set_option('expand_frame_repr', False)  # 当列太多时显示完整

df = pd.read_csv(
    r'C:\Users\Simons\Desktop\xbx_coin_2020\data\OKEX_BTC-USDT_20200302_1T.csv',
    encoding='gbk',
    skiprows=1, parse_dates=['candle_begin_time']
)

# =====批量导入EOSUSD所有天的一分钟数据
# 系统自带函数os.walk，用于遍历文件夹中的所有文件，os是python自带的系统库
# 演示os.walk

# file location存储我们要读取的数据的文件夹绝对路径
file_location = r'C:\Users\Simons\Desktop\xbx_coin_2020\data\cls-3.2'

# for root, dirs, files in os.walk(file_location):
#     # root输出文件夹，dirs输出root下所有的文件夹，files输出root下的所有的文件
#     print('当前文件夹:', root)
#     print('包含的文件夹:', dirs)
#     print('包含的文件:', files)
#     print()

# 批量读取文件名称
# file_list = []
# for root, dirs, files in os.walk(file_location):
#     for filename in files:
#         if filename.endswith('.csv'):
#             file_path = os.path.join(root, filename)
#             file_path = os.path.abspath(file_path)
#             file_list.append(file_path)

# 遍历文件名，批量导入数据
# all_data = pd.DataFrame()
# for fp in sorted(file_list):
#     print(fp)
#
#     # 导入数据
#     df = pd.read_csv(fp, skiprows=1, encoding='gbk')
#     #  合并数据
#     all_data = all_data.append(df, ignore_index=True)  # 注意此时若一下子导入很多文件，可能会内存溢出


# 对数据进行排序
# all_data.sort_values(by=['candle_begin_time'], inplace=True)
# print(all_data)

# 将数据存入hdf文件中
# all_data.to_hdf(
#     r'C:\Users\Simons\Desktop\xbx_coin_2020\data\eos_1min_data.h5',
#     key='all_data',
#     mode='w'
# )