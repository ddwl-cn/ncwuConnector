from datetime import datetime

import colorama


# 没啥用。。。。
def info(msg=''):
    print('\033[1;36m[INFO]\033[0m------'
          + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
          + '------\033[1;36m[{}]\033[0m'.format(msg))


def warning(msg=''):
    print('\033[1;33m[WARNING]\033[0m------'
          + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
          + '------\033[1;35m[{}]\033[0m'.format(msg))


def debug(msg=''):
    print('\033[1;34m[DEBUG]\033[0m------'
          + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
          + '------\033[1;34m[{}]\033[0m'.format(msg))


def error(msg=''):
    print('\033[1;31m[ERROR]\033[0m------'
          + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
          + '------\033[1;31m[{}]\033[0m'.format(msg))


# info('666')
# warning('666')
# debug('666')
# error('666')
