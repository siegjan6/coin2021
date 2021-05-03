import os
import configparser


class Config(object):
    def __init__(self, config_file='config.ini'):
        self._path = os.path.join(os.getcwd(), config_file)
        self._path = "config.ini"
        if not os.path.exists(self._path):
            raise FileNotFoundError("No such file: config.ini")
        self._config = configparser.ConfigParser()
        self._config.read(self._path, encoding='utf-8-sig')
        self._configRaw = configparser.RawConfigParser()
        self._configRaw.read(self._path, encoding='utf-8-sig')

    def get(self, section, name):
        return self._config.get(section, name)

    def getRaw(self, section, name):
        return self._configRaw.get(section, name)


global_config = Config()
apiKey = global_config.getRaw('config', 'apiKey')
secret = global_config.getRaw('config', 'secret')
password = global_config.getRaw('config', 'password')
short_sleep_time = int(global_config.getRaw('config', 'short_sleep_time'))  # 用于和交易所交互时比较紧急的时间sleep，例如获取数据、下单
medium_sleep_time = int(global_config.getRaw('config', 'medium_sleep_time'))  # 用于和交易所交互时不是很紧急的时间sleep，例如获取持仓
long_sleep_time = int(global_config.getRaw('config', 'long_sleep_time'))  # 用于较长的时间sleep

coin_value_table = {
    "btc-usdt": 0.01,  # 比特币合约最小单位为0.01
    "eos-usdt": 10,
    "eth-usdt": 0.1,  # 以太坊合约最小单位为0.1
    "ltc-usdt": 1,
    "bch-usdt": 0.1,
    "xrp-usdt": 100,
    "etc-usdt": 10,
    "bsv-usdt": 1,
    "trx-usdt": 1000
}

# 订单对照表
okex_order_type = {
    '1': '开多',
    '2': '开空',
    '3': '平多',
    '4': '平空',
}

# 订单状态对照表
okex_order_state = {
    '-2': '失败',
    '-1': '撤单成功',
    '0': '等待成交',
    '1': '部分成交',
    '2': '完全成交',
    '3': '下单中',
    '4': '撤单中',
}