"""
《邢不行-2020新版|Python数字货币量化投资课程》
无需编程基础，助教答疑服务，专属策略网站，一旦加入，永续更新。
课程详细介绍：https://quantclass.cn/crypto/class
邢不行微信: xbx9025
本程序作者: 邢不行

# 课程内容
通过案例介绍什么是API
"""


# =====神奇的网址-API示例
# okex：https://www.okex.com/api/spot/v3/instruments/BTC-USDT/ticker
# 返回结果示例：{"best_ask":"7871.9","best_bid":"7871.8","instrument_id":"BTC-USDT","product_id":"BTC-USDT","last":"7872.7","last_qty":"0.00294821","ask":"7871.9","best_ask_size":"2.47032541","bid":"7871.8","best_bid_size":"0.3586146","open_24h":"8090.4","high_24h":"8090.4","low_24h":"7637.4","base_volume_24h":"71999.67613995","timestamp":"2020-03-10T03:27:31.069Z","quote_volume_24h":"564510343.1"}

# 火币：https://api.huobi.pro/market/detail/merged?symbol=btcusdt
# 返回结果示例：{"status":"ok","ch":"market.btcusdt.detail.merged","ts":1583810974164,"tick":{"amount":71311.94804854663,"open":8082.13,"close":7890.19,"high":8082.14,"id":210146022322,"count":561789,"low":7638.0,"version":210146022322,"ask":[7890.98,0.58188],"vol":5.587285592033827E8,"bid":[7888.83,0.061314]}}

# 币安：https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT
# 返回结果示例：

# 修改免翻墙域名
# 将网址中的okex.com改为okex.me：https://www.okex.me/api/spot/v3/instruments/BTC-USDT/ticker

# 该网址之后可能会失效

# 这个就是API，官方提供给我们用来从交易所获取数据的网址


# =====修改参数
# 将okex网址中的btc改为ltc：https://www.okex.com/api/spot/v3/instruments/LTC-USDT/ticker

# 可以在神奇的网址中修改相关参数，来达到获取不同数据的目的


# =====哪里找到神奇的网址
# 交易所官网，有详细的文档。

# 交易所能提供的数据，全在官网上，可以仔细阅读，数据是量化之源。


# =====每家交易所不一样
# 每家请求的内容不一样：网址、币种的格式

# 返回的结果不一样：格式

# 能提供的数据种类不一样

# 限制也不一样

# 稳定性也不同：决定了一家交易所的技术实力


# =====其他
# 不同人使用的接口不一样：内部、大户、散户







