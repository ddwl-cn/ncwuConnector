# -*- coding: utf-8 -*-
import logging
import sys
from datetime import datetime

import requests
import time
import re

from ncwuConnector.encryption import get_base64, get_xencode, get_md5, get_sha1
from ncwuConnector.loggers import info, debug

'''
此代码在：https://blog.csdn.net/qq_20534023/article/details/124159181
的基础上进行修改
'''

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 '
                  'Safari/537.36 '
}
# 不同的地点ac_id就不同 例如在宿舍常常是1 实验楼就会变成2
# 体现在WIFI名称上就是NCWU1 和 NCWU2的区别

init_url = "http://192.168.0.170/srun_portal_pc?ac_id={}&theme=basic"

get_challenge_api = "http://192.168.0.170/cgi-bin/get_challenge"

srun_portal_api = "http://192.168.0.170/cgi-bin/srun_portal"

n = '200'
type = '{}'
ac_id = '{}'

enc = "srun_bx1"


# 多重拼接
def __get_chksum(acid, username):
    chkstr = token + username
    chkstr += token + hmd5
    chkstr += token + ac_id.format(acid)
    chkstr += token + ip
    chkstr += token + n
    chkstr += token + type.format(acid)
    chkstr += token + i
    return chkstr


def __get_info(acid, username, password):
    info_temp = {
        "username": username,
        "password": password,
        "ip": ip,
        "acid": ac_id.format(acid),
        "enc_ver": enc
    }
    i = re.sub("'", '"', str(info_temp))
    i = re.sub(" ", '', i)
    return i


def __init_getip(acid, action=None):
    global ip
    init_res = requests.get(init_url.format(acid), headers=header)
    # info("初始化获取ip")
    ip = re.search('id="user_ip" value="(.*?)"', init_res.text).group(1)
    info('{}ip：'.format(action) + ip)


def __get_token(username):
    # info("获取token信息")
    global token
    get_challenge_params = {
        "callback": "jQuery112404953340710317169_" + str(int(time.time() * 1000)),
        "username": username,
        "ip": ip,
        "_": int(time.time() * 1000),
    }
    get_challenge_res = requests.get(get_challenge_api, params=get_challenge_params, headers=header)
    token = re.search('"challenge":"(.*?)"', get_challenge_res.text).group(1)


def __do_complex_work(acid, username, password):
    global i, hmd5, chksum
    i = __get_info(acid, username, password)
    i = "{SRBX1}" + get_base64(get_xencode(i, token))
    hmd5 = get_md5(password, token)
    chksum = get_sha1(__get_chksum(acid, username))
    # debug("所有加密工作已完成")


def __login(acid, username):
    srun_portal_params = {
        'callback': 'jQuery11240645308969735664_' + str(int(time.time() * 1000)),
        'action': 'login',
        'username': username,
        'password': '{MD5}' + hmd5,
        'ac_id': ac_id.format(acid),
        'ip': ip,
        'chksum': chksum,
        'info': i,
        'n': n,
        'type': type.format(acid),
        'os': 'windows+10',
        'name': 'windows',
        'double_stack': '0',
        '_': int(time.time() * 1000)
    }
    rad_user_info = "http://192.168.0.170/cgi-bin/rad_user_info?"
    rad_user_info += srun_portal_params.get("callback")

    srun_portal_res = requests.get(srun_portal_api, params=srun_portal_params, headers=header)
    # debug(srun_portal_res.text)
    rad_user_res = requests.get(rad_user_info, headers=header)


def __logout(acid, username):
    srun_portal_params = {
        'callback': 'jQuery11240645308969735664_' + str(int(time.time() * 1000)),
        'action': 'logout',
        'username': username,
        'ac_id': ac_id.format(acid),
        'ip': ip,
        'os': 'windows+10',
        'name': 'windows',
        'double_stack': '0',
        '_': int(time.time() * 1000)
    }
    srun_portal_res = requests.get(srun_portal_api, params=srun_portal_params, headers=header)
    # debug(srun_portal_res.text)


# 登录校园网
def Login(acid='1', username='', password=''):
    __init_getip(acid, '登录')
    __get_token(username)
    __do_complex_work(acid, username, password)
    __login(acid, username)


# 注销 只是本地注销 没什么用
# 主要是靠logout_ncwu.py中的一键下线功能
def Logout(acid='1', username=''):
    __init_getip(acid, '登出')
    __get_token(username)
    __logout(acid, username)

