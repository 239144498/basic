# -*- coding: UTF-8 -*-
import requests
import pprint

url = 'http://httpbin.org/cookies/set?id=123456'


# 截取封包内的Content-Length参数需要去除，Content-Length如果存在并且有效的话，则必须和消息内容的传输长度完全一致。（经过测试，如果过短则会截断，过长则会导致超时，requests会自动设置该参数
# Accept-Encoding: gzip, deflate, br;  注意requests不能解压br格式，会显示乱码，需去掉br或改用第三方模块
headers = {}
# 将字典转为CookieJar
CookieJar = requests.utils.cookiejar_from_dict({"user": "sunny"})
proxies = {"http": "127.0.0.1:8888", "https": "127.0.0.1:8888"}

r = requests.session()
# 设置默认的cookies
r.cookies = CookieJar
pprint.pprint(r.cookies.get_dict())
# verify https时是否进行证书验证
# allow_redirects 是否运行重定向
# proxies 代理服务器s
# timeout connect 和 read 的超时时间,timeout判断的并不是整个请求的总时间，而是从与服务器连接成功后，客户端开始接受服务器的数据为计算起点的，卡在dns解析上的时间是不计算的
rs = r.get(url,
           headers=headers,
           # cookies=CookieJar,
           verify=False,
           allow_redirects=False,
           timeout=(3, 7),
           # proxies=proxies
           )

#使用session会自动更新cookies
pprint.pprint(r.cookies.get_dict())

