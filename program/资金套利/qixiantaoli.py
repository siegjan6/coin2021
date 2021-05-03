import pandas
import time
import datetime
import ccxt

time_interval = 5  # 数据抓取间隔时间
diff_target = 0.08  # 目标开仓期现价差 0.08代表8%价差
exchange = ccxt.binance()
symbols = exchange.dapiPublicGetExchangeInfo()['symbols']  # 币本位所有交易对

quarterly_symbols_ID = []  # 初始化当季交易对
for symbol in symbols:
    if '06' in symbol['symbol']:  # 目标合约时间 06代表6月当季
        quarterly_symbols_ID.append(symbol['symbol'])  # 获取币本位当季交易对
print(quarterly_symbols_ID)
while True:
    quarterly_symbols_price_list = []  # 初始化当季交易对的价格信息列表
    markPrice_indexPrice = exchange.dapiPublicGetPremiumIndex()  # 获取所有币本位合约的价格信息
    for price in markPrice_indexPrice:
        if price['symbol'] in quarterly_symbols_ID:
            quarterly_symbols_price_dict = price
            quarterly_symbols_price_dict['diff'] = (float(price['markPrice']) - float(price['indexPrice'])) / float(
                price['indexPrice'])  # (期货价格-现货价格)/现货价格
            quarterly_symbols_price_list.append(quarterly_symbols_price_dict)  # 获取当季交易对的价格信息
    df = pandas.DataFrame(quarterly_symbols_price_list)[['symbol', 'diff', 'markPrice', 'indexPrice']].sort_values(
        'diff')
    print(df.to_string(index=False))  # 打印当季交易对的价格信息，可注释掉
    max_diff = df['diff'].max()  # 最高价差
    if max_diff > diff_target:  # 最高价差是否大于目标价差
        print(datetime.datetime.now())
        print('====最大价差：' + str(max_diff) + ' >目标价差：' + str(diff_target) + '，开始交易，下面插入交易代码' + "====")
        print(df[df['diff'] == max_diff].to_string(index=False))  # 打印最高价差的交易对、价差值等相关信息
    else:
        print('最大价差：' + str(max_diff) + ' <目标价差：' + str(diff_target) + ', '
              + str(time_interval) + '秒后重新抓取最大价差')
    time.sleep(time_interval)
