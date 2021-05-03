"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行/西蒙斯

# 课程内容
- 列表介绍
- 列表常见操作

功能：本程序主要介绍python的常用内置数据结果，如list、dict、str等。希望以后大家只要看这个程序，就能回想起相关的基础知识。
"""


# =====list介绍
# 使用[]中括号就可以新建一个数组。
# list_var = []  # 这是一个空list
# print(list_var, type(list_var))

# list是具有顺序的一组对象，其中的元素不需要是同类型
# list_var = [1, '2', 3, 4.0, 5, 6, 'seven', [8], '九']  # list举例，其中包含了整数、小数、字符串、数组
# print(list_var)


# =====list常见操作：索引，选取list中的某个元素
# list_var = [1, '2', 3, 4.0, 5, 6, 'seven', [8], '九']  # list举例

# print(list_var[0])  # 输出排在第1个位置的元素。位置的计数是从0开始的。
# print(list_var[3])  # 输出排在第4个位置的元素。
# print(list_var[8])  # 输出排在第9个位置的元素。也就是最后一个元素。
# print(list_var[-1])  # 输出最后一个元素的另外一种方式。
# print(list_var[-2])  # 输出最后第二个位置的元素。
# print(list_var[9])  # 超出长度会报错 IndexError: list index out of range
# print(list_var[-10])  # 超出长度会报错 IndexError: list index out of range
# list_var[3] = 100  # 可以根据索引，直接修改list中对应位置的元素
# print(list_var)


# =====list常见操作：切片，选取list中的一连串元素
# list_var = [1, '2', 3, 4.0, 5, 6, 'seven', [8], '九']  # list举例
# print(list_var[3:8])  # list[a:b]，从第a个位置开始，一直到第b个位置之前的那些元素
# print(list_var[:4])  # list[:b]，从头开始，一直到第b个位置之前的那些元素
# print(list_var[3:])  # list[a:]，从第a个位置开始，一直到最后一个元素
# print(list_var[1:7:3])  # list[a:b:c]，每c个元素，选取其中的第一个


# =====list常见操作：两个list相加
# list_var1 = [1, '2', 3, 4.0, 5]
# list_var2 = [6, 'seven', [8], '九']
# print(list_var1 + list_var2)  # 两个list相加


# =====list常见操作：判断一个元素是否在list当中
# list_var = [1, '2', 3, 4.0, 5]
# print(1 in list_var)  # 判断1元素，是否在list_var中出现
# print(100 in list_var)  # 判断100元素，是否在list_var中出现


# =====list常见操作：len，max，min
# list_var = [1, 2, 3, 4, 5]
# print(len(list_var))  # list中元素的个数，或者说是list的长度
# print(len([]))  # 空list的长度是？
# print(max(list_var))  # 这个list中最大的元素，
# print(min(list_var))  # 最小的元素


# =====list常见操作：删除其中的一个元素
# list_var = [1, 2, 3, 4, 5]
# del list_var[0]  # 删除位置0的那个元素
# print(list_var)


# =====list常见操作：如何查找一个元素的在list中的位置
# list_var = [3, 5, 1, 2, 4]  # 如何才能知道1这个元素，在list中的位置是什么？
# 不知道的话，直接搜索


# =====list常见操作：append,在后方增加一个元素
# list_var = [1, '2', 3, 4.0, 5]
# list_var.append(6)
# print(list_var)
# list_var.append(['seven', [8], '九'])
# print(list_var)


# =====list常见操作：两个list合并
# list_var = [1, '2', 3, 4.0, 5]
# list_var.extend([6, 'seven', [8], '九'])
# print(list_var)


# =====list常见操作：逆序、排序、
# list_var = [3, 5, 1, 2, 4]
# list_var.reverse()
# print(list_var)
# list_var = [3, 5, 1, 2, 4]
# list_var.sort()
# print(list_var)
# list_var = [3, 5, 1, 2, 4]
# print(sorted(list_var))
# print(list_var)
