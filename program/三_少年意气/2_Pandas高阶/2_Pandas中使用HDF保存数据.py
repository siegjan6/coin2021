"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行/西蒙斯

# 本节课程内容
- HDF5文件介绍
- 如何存储、读取HDF5
"""

import pandas as pd
import os

pd.set_option('expand_frame_repr', False)  # 当列太多时显示完整


# =====将数据存入hdf文件
# 批量读取文件名称
file_list = []
# 存储csv文件的文件夹路径
file_location = r'C:\Users\Simons\Desktop\xbx_coin_2020\data\cls-3.2'

# for root, dirs, files in os.walk(file_location):
#     for filename in files:
#         if filename.endswith('.csv'):
#             file_path = os.path.join(root, filename)
#             file_path = os.path.abspath(file_path)
#             file_list.append([filename, file_path])

# 创建hdf文件
# h5_store = pd.HDFStore('eos_1min_data.h5', mode='w')

# 批量导入并且存储数据
# for filename, file_path in sorted(file_list):
#     # BITFINEX_EOSUSD_20170701_1T.csv
#     date = filename.split('_')[2]
#     print(date, filename, file_path)
#     df = pd.read_csv(file_path, encoding='gbk', skiprows=1, parse_dates=['candle_begin_time'])
#
#     # 存储数据到hdf
#     h5_store['eos_' + date] = df.iloc[:100]

# 关闭hdf文件
# h5_store.close()

# =====读取hdf数据
# 创建hdf文件
# h5_store = pd.HDFStore('eos_1min_data.h5', mode='r')

# h5_store中的key
# print(h5_store.keys())

# 读取某个key指向的数据
# print(h5_store.get('eos_20170702'))
# print(h5_store['eos_20170702'])

# 关闭hdf文件
# h5_store.close()
