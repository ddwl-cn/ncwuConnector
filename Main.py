# -*- coding: utf-8 -*-
import logging
import os
import subprocess
import sys
import time
import traceback
from datetime import datetime

from ncwuConnector.WIFI_Switch import WiFi
from ncwuConnector.login_ncwu import Login, __login
from ncwuConnector.logout_ncwu import Logout
from ncwuConnector.loggers import info


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

    p = subprocess.Popen("ping -n 2 www.baidu.com", stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, shell=False)
    out, err = p.communicate()

    # 如果没有ping通说明没有登录应该登录
    if p.returncode != 0:
        check_WIFI()
        # 先在自助中心下线 再尝试上线

        if Logout(username, password) == 0:
            # 成功下线 稍缓一会儿
            time.sleep(2)

        info('正在尝试 {} 号通道登录'.format(cnt))
        Login(str(cnt), username, password)
        # 检验是否正常上网
        p = subprocess.Popen("ping -n 2 www.baidu.com", stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, shell=True)
        out, err = p.communicate()

        if p.returncode != 0:
            return tryConnect(cnt + 1)
        else:
            info('{} 号通道登录成功'.format(cnt))

    return True


if __name__ == '__main__':

    __stderr__ = sys.stderr

    sys.stderr = open('error.txt', 'w+')

    time.sleep(1)

    # 你的用户名密码
    arr = []
    try:
        # 账号 密码 放在同级的account.txt中
        file = open('account.txt', encoding='utf-8')
        for line in file:
            arr.append(line.strip())
        # 关闭文件
        file.close()
        username = arr[0]
        password = arr[1]
    except Exception as e:
        info('同级路径下未检测到"account.txt.txt" 或 文件格式有误，请检查后手动运行！')
        traceback.print_exc()
        exit(-1)

    while True:
        try:
            if tryConnect(1):
                info('当前网络状况良好')
            else:
                break
        except Exception as e:
            info('远程主机连接失败, 等待再次尝试...')
            traceback.print_exc()
        time.sleep(5)

    info('遇到了意料之外的错误')
