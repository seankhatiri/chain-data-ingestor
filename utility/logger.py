from datetime import datetime

from configuration.configs import Configs
from utility.singleton import Singleton


class Logger(metaclass=Singleton):
    _INFO = 'INFO'
    _DEBUG = 'DEBUG'
    _ERROR = 'ERROR'

    def __log(self, lvl, message, title):
        print(f'-------> {lvl}', datetime.now().strftime('%Y-%m-%d %H:%M:%S+'), title, message, flush=True)

    def info(self, message, title=''):
        if int(Configs.log_level) > 2:
            self.__log(self._INFO, message, title)

    def debug(self, message, title='', additional_data=None):
        if int(Configs.log_level) > 1:
            self.__log(self._DEBUG, message, title)
            print('Extra args: ', additional_data)

    def error(self, message, title='', additional_data=None):
        if int(Configs.log_level) > 0:
            self.__log(self._ERROR, message, title)
            print('Extra args: ', additional_data)
