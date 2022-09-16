import ddddocr
import requests
import re
from ncwuConnector.loggers import info
'''
用于自主服务网站的一键下线

其实可以登录一次后保存cookie到本地免去下次登录的
'''

# 校园网源地址
origin_url = 'http://192.168.0.170:8900'
# 登录页面地址
login_url = 'http://192.168.0.170:8900/login'
# 用户主页地址
home_url = 'http://192.168.0.170:8900/home'
# 一键下线请求地址
onekey_url = 'http://192.168.0.170:8900/home/onekey'


# 识别登录页面的验证码
def ImgToString(img):
    # 保存图片到本地
    with open('../code.jpg', 'wb') as f:
        f.write(img.content)
        f.flush()
    f.close()
    # 识别并返回验证码
    ocr = ddddocr.DdddOcr()
    with open('../code.jpg', 'rb') as f:
        img_bytes = f.read()
    f.close()
    return ocr.classification(img_bytes)


# 设备在线情况
def checkStatus(html=""):
    if html.find('没有找到数据') != -1:
        info('当前还没有设备在线，可以直接登录')
        return False
    return True


# 直接登录自助服务网站下线所有在线设备
def Logout(username, password):
    # 登录请求头
    header1 = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '180',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': '192.168.0.170:8900',
        'Origin': origin_url,
        'Referer': origin_url,
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36 Edg/101.0.1210.39'
    }

    # 创建session 保持本次会话
    session = requests.session()
    # 访问登录页面并获取验证码图片
    response = session.get(origin_url)
    # print(response)
    code_url = 'http://192.168.0.170:8900' \
               + re.search('<img id="loginform-verifycode-image" src="(.*?)" alt="">', response.text).group(1)
    # print(code_url)
    img = session.get(code_url)
    # 识别图片内容并返回

    code = ImgToString(img)
    username = username
    password = password
    # 每次页面刷新会有一个新的csrf
    csrf = re.search('<meta name="csrf-token" content="(.*?)">', response.text).group(1)

    data1 = {
        '_csrf': csrf,
        'LoginForm[username]': username,
        'LoginForm[password]': password,
        'LoginForm[verifyCode]': code,
    }

    # 携带账户信息 发起登录请求
    response = session.post(login_url, headers=header1, data=data1, allow_redirects=True)

    if not checkStatus(response.text):
        return 1
    info('当前已有设备在线，正在一键下线')
    # 获取当前页面csrf_token
    csrf = re.search('<meta name="csrf-token" content="(.*?)">', response.text).group(1)

    data = {
        '_csrf': csrf
    }
    # 携带csrf_token 发起一键下线请求
    response = session.post(onekey_url, data=data, allow_redirects=True)

    info('一键下线成功')
    return 0
