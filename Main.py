# -*- coding: utf-8 -*-
import atexit
import logging
import os
import random
import subprocess
import sys
import time
import traceback
import ctypes
import atexit

import colorama
from datetime import datetime

import ncwuConnector.login_ncwu
from ncwuConnector.WIFI_Switch import WiFi
from ncwuConnector.login_ncwu import Login, Logout
from ncwuConnector.logout_ncwu import Logout
from ncwuConnector.loggers import info, warning, debug, error


def err_exit():
    error('遇到了未知的错误')
    os.system('pause')
    exit(-1)


atexit.register(err_exit)
IPaddress = ['8.8.8.8', '114.114.114.114', 'www.baidu.com', 'www.tencent.com']


def ping(index=1):
    p = subprocess.Popen("ping -n 2 {}".format(IPaddress[index]), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, shell=False)
    out, err = p.communicate()
    return p.returncode


def check_WIFI():
    wifi = WiFi()
    # 打印网卡名称
    wifi_msg = wifi.wifi_connect_status()
    if not wifi_msg:
        info('wifi暂未连接, 即将自动连接到NCWU')
    else:
        info('wifi连接状态正常')
    wifi.connect_wifi(r"NCWU", r"")


def tryConnect(cnt):
    # 超过5次仍然没有连通则退出
    if cnt > 5:
        return False
    # 如果没有ping通说明没有登录应该登录
    if ping(random.randint(0, len(IPaddress) - 1)) != 0:
        check_WIFI()
        # 先在自助中心下线 再尝试上线
        if Logout(username, password) == 0:
            # 成功下线 稍缓一会儿
            time.sleep(0.5)
        info('正在尝试 {} 号通道登录'.format(cnt))
        Login(str(cnt), username, password)
        # 检验是否正常上网
        if ping(random.randint(0, len(IPaddress) - 1)) != 0:
            return tryConnect(cnt + 1)
        else:
            info('{} 号通道登录成功'.format(cnt))
    return True


if __name__ == '__main__':
    colorama.init(autoreset=True)
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)
    # 标准错误输出
    __stderr__ = sys.stderr
    sys.stderr = open('error.txt', 'w+')
    # 开机等待一秒
    time.sleep(1)
    # 获取用户名密码
    arr = []
    try:
        # 账号 密码 放在同级的account.txt中
        file = open('account.txt', encoding='utf-8')
        for line in file:
            arr.append(line.strip())
        file.close()
        username = arr[0]
        password = arr[1]
    except Exception as e:
        error('同级路径下未检测到"account.txt.txt" 或 文件格式有误，请检查后手动运行！')
        traceback.print_exc()
        os.system('pause')
        exit(-1)

    while True:
        try:
            if tryConnect(1):
                info('当前网络状况良好')
            else:
                break
        except Exception as e:
            warning('远程主机连接失败, 等待再次尝试...')
            traceback.print_exc()
            continue
        time.sleep(3)
