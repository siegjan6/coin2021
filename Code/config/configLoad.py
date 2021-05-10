import os
import configparser


class Config(object):
    def __init__(self, config_file='config.ini'):
        cwd = os.getcwd().split('coin2021')[0] + 'coin2021/Code/config'
        self._path = os.path.join(cwd, config_file)
        print(self._path)
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
# apiKey = global_config.getRaw('config', 'apiKey1613')
# secret = global_config.getRaw('config', 'secret1613')
# apiKey = global_config.getRaw('config', 'apiKey171')
# secret = global_config.getRaw('config', 'secret171')
#
# apiKey = global_config.getRaw('config', 'apiKey3266')
# secret = global_config.getRaw('config', 'secret3266')

apiKey = global_config.getRaw('config', 'apiKeyZjc')
secret = global_config.getRaw('config', 'secretZjc')
