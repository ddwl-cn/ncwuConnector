from datetime import datetime


# 没啥用。。。。
def info(msg=''):
    print('[INFO]------'
          + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
          + '------[{}]'.format(msg))
