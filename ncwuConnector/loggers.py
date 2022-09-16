from datetime import datetime

import colorama


# 没啥用。。。。
def info(msg=''):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print('\033[1;36m[INFO]\033[0m'.ljust(35, '-')
          + time
          + '------------------------\033[1;36m[{}]\033[0m'.format(msg))


def warning(msg=''):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print('\033[1;33m[WARNING]\033[0m'.ljust(35, '-')
          + time
          + '------------------------\033[1;33m[{}]\033[0m'.format(msg))


def debug(msg=''):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print('\033[1;34m[DEBUG]\033[0m'.ljust(35, '-')
          + time
          + '------------------------\033[1;34m[{}]\033[0m'.format(msg))


def error(msg=''):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print('\033[1;31m[ERROR]\033[0m'.ljust(35, '-')
          + time
          + '------------------------\033[1;31m[{}]\033[0m'.format(msg))


# info('666')
# warning('666')
# debug('666')
# error('666')
