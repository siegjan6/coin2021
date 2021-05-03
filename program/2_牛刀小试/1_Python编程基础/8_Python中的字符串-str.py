"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行/西蒙斯

# 课程内容
- 字符与字符串
- 字符串中的转义
- 字符串常见操作

功能：本程序主要介绍python的常用内置数据结果，如list、dict、str等。希望以后大家只要看这个程序，就能回想起相关的基础知识。
"""

# =====字符
# class_name = '邢不行量化'
# symbol = 'BTC/USDT'
# trade_coin_name = '比特币'
# email = 'xingbuxing@quantclass.cn'
# phone = '18820198888'

# =====字符串转义，特殊字符的表达
# print('what is up')  # 如何输入what's up
# print('what\'s up\t')  # 使用\对特殊字符进行转义。转义也可以用于表达不可见字符，例如tab符号：\t。
# print('\\')  # 如果要表达\本身，也需要转义，写为\\。

# Windows中的地址
# print('/Users/Shared/xbx-coin-2020/xbx_coin_2020/data/OKEX_20200302_5T.csv')  # mac下的地址表达
# print('C:\Users\Simons\Desktop\xbx_coin_2020\data\OKEX_20200302_5T.csv')  # win下的地址表达
# print(r'C:\Users\Simons\Desktop\xbx_coin_2020\data\OKEX_20200302_5T.csv')  # 在字符串的开始加r（Raw String），使得字符串中不发生转义。


# =====字符串常见操作：字符串相加，相乘
# str1 = 'btc'
# str2 = 'usdt'
# print(str1 + str2)  # 字符串可以直接相加
# print(str1 * 3)  # 字符串可以乘以整数
# print('*' * 30)


# =====字符串常见操作：startswith、endswith
# symbol = 'btcusdt'
# print(symbol.startswith('btc'))  # 判断字符串是否是以'btc'开头
# print(stock_code.startswith('b'))
# print(stock_code.startswith('BTC'))
# print(stock_code.endswith('usdt'))


# =====字符串常见操作：判断
# name = '邢不行'
# print('行' in name)  # 判断字符串中是否包含'行'
# print('x' in name)


# =====字符串常见操作：替换
# symbol = 'btcusdt'
# print(symbol.replace('btc', 'eth'))  # 将字符串中的'btc'替换成'eth'
# print('ethusdt, xrpusdt'.replace('usdt', 'btc'))


# =====字符串常见操作：split
# symbol = 'btcusdt, ethusdt, xrpusdt'
# print(symbol.split(', '))
# print(symbol.split(', ')[0])
# print(symbol.split('usdt'))
# 逆操作
# symbol_list = ['btcusdt', 'ethusdt', 'xrpusdt']
# print(', '.join(symbol_list))


# =====字符串常见操作：strip
# symbol = '  btcusd  '
# print(symbol)
# print(symbol.strip())  # 去除两边的空格

# symbol = 'btcusdt'
# print(symbol)
# print(symbol.strip('usdt'))  # 去除首末的usd
# print(symbol.strip('btc'))  # 去除首末的btc


# =====字符串的选取：把字符串当做list
# name = '邢不行量化课程'
# print(name[0])
# print(name[:3])
# print(name[3:])
# print(len(name))
# print(name[-1])


# =====字符串的高级拼接，除了加号之外，如何穿插
# 最常用方法：%s
# today = '20200302'
# print(r'C:\Users\Simons\Desktop\xbx_coin_2020\data\OKEX_%s_5T.csv' % today)
#
# rule_type = '1H'
# print(r'C:\Users\Simons\Desktop\xbx_coin_2020\data\OKEX_%s_%s.csv' % (today, rule_type))
