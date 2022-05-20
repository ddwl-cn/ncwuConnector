# -*- coding: utf-8 -*-
import time

from pywifi import const, PyWiFi, Profile


class WiFi(object):
    # 创建对象自动初始化
    def __init__(self):
        wifi = PyWiFi()                     # 创建一个无线对象
        self.iface = wifi.interfaces()[0]   # 获取当前机器第一个无线网卡

    # 查看wifi的连接状态
    def wifi_connect_status(self):
        """
        判断本机是否有无线网卡，以及连接状态
        :return:已连接或存在网卡返回1，否则返回0
        """
        ret_list = []
        # 判断是否连接成功
        if self.iface.status() in \
                [const.IFACE_CONNECTED, const.IFACE_CONNECTING, const.IFACE_INACTIVE]:
            return self.iface.name()        # 连接成功显示连接设备
        else:
            return False       # 连接失败返回失败信息

    """
    扫描附近wifi
        乱码问题：
        把wifi_info.ssid重新编码为gb18030
        wifi_info.ssid.encode('raw_unicode_escape','strict').decode('gb18030')
        我也不清楚他为什么不全用unicode
        ssid出来应该是unicode  但是  你往profile里面写的时候  必须是gb18030
        所以这么一个操作
        你会发现gb18030在控制台和py的某些控件上输出是乱码  是因为 控制台是utf-8
        想在这上面输出中文的话你得encode('raw_unicode_escape','strict').decode()
    """
    def scan_wifi(self, scantime=1):
        """
        :param scantime:    指定扫描时间，默认扫描时间为1秒
        :return:            返回的是一个network dictionary,key=bssid,value=ssid
        """
        self.iface.scan()                                           # 扫描附近wifi
        time.sleep(scantime)
        basewifi = self.iface.scan_results()
        dict = {}
        for i in basewifi:
            dict[i.bssid] = i.ssid.encode(encoding='raw_unicode_escape', errors='strict').decode()
        return dict

    # 链接到指定wifi
    def connect_wifi(self, wifi_ssid, password):
        profile = Profile()                                         # 配置文件
        profile.ssid = wifi_ssid                                    # wifi名称
        profile.auth = const.AUTH_ALG_OPEN                          # 需要密码 校园网wifi连接一般不需要密码吧...

        if '' == password:
            profile.akm.append(const.AKM_TYPE_NONE)                 # 加密类型无密码
        else:
            profile.akm.append(const.AKM_TYPE_WPAPSK)               # 加密类型

        profile.cipher = const.CIPHER_TYPE_CCMP                     # 加密单元
        profile.key = password                                      # wifi密码

        self.iface.remove_all_network_profiles()                    # 删除其他配置
        tmp_profile = self.iface.add_network_profile(profile)       # 加载配置

        self.iface.connect(tmp_profile)                             # link start
        time.sleep(1)                                               # 尝试1s是否成功
        isok = True
        if self.iface.status() == const.IFACE_CONNECTED:
            return isok                                             # 连接成功
        else:
            isok = False                                            # 连接失败设置isok = False
        self.iface.disconnect()                                     # 避免超时后连接成功手动断开一下，因为在一定时间内连接失败用户会继续重试连接
        time.sleep(1)
        return isok
