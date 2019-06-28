import random
import re
import traceback
import urllib.request as urllib2

import requests


def test_url():
    def_headers = {
        'Host': 'www.dianping.com',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Cookie': 'Cookie__mta=142037261.1560844813116.1560844813116.1560844813116.1; cy=5; cye=nanjing; _lxsdk_cuid=16b1afa8f30c8-0d5154320b3f228-70226752-13c680-16b1afa8f31c8; _lxsdk=16b1afa8f30c8-0d5154320b3f228-70226752-13c680-16b1afa8f31c8; _hc.v=d2bf0bc8-ef22-e77a-8572-7fdd38678f60.1559525758; s_ViewType=10; hibext_instdsigdipv2=1; aburl=1; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_s=16b8c61cc3a-668-fd3-248%7C%7C122',
        'Upgrade-Insecure-Requests': '1',
        # 'If-Modified-Since': 'Tue, 25 Jun 2019 02:05:48 GMT',
        # 'If-None-Match': '62bbb6c1a987e5ba38c537d1f798c1c9',
        'Cache-Control': 'max-age=0'
    }
    url = 'http://www.dianping.com/shop/23995696?a=1'
    request = urllib2.Request(url=url, headers=def_headers)
    res = urllib2.urlopen(request)
    page_source = res.read().decode('utf-8', 'ignore')
    print(page_source)


def test_ip():
    import random
    s_ips = '''220.180.50.14:53281@HTTP#[未知]安徽省合肥市巢湖市 电信
61.178.238.122:63000@HTTP#[未知]甘肃省兰州市城关区 电信
118.24.89.206:1080@HTTP#[未知]广西柳州市高新区 视虎科技有限公司
14.155.113.250:9000@HTTP#[未知]广东省深圳市 电信
47.92.248.139:3128@HTTP#[未知]河北省 阿里云
183.245.98.6:8118@HTTP#[普匿]浙江省温州市 移动
221.226.94.218:110@HTTP#[未知]江苏省南京市 电信
116.252.39.176:53281@HTTP#[未知]广西南宁市 电信
123.207.91.165:1080@HTTP#[未知]广东省广州市 腾讯云
222.162.172.38:8060@HTTP#[未知]吉林省吉林市 联通
218.89.234.40:8118@HTTP#[普匿]四川省成都市 电信
193.112.17.112:1080@HTTP#[普匿]广东省广州市 腾讯云
112.17.157.51:8060@HTTP#[未知]浙江省 移动
58.243.50.184:53281@HTTP#[未知]安徽省合肥市 联通
27.208.31.4:8060@HTTP#[未知]山东省威海市 联通
60.205.207.205:3128@HTTP#[高匿]北京市 阿里云BGP服务器
117.127.0.202:8080@HTTP#[未知]江西省吉安市 广电网
183.234.241.105:8118@HTTP#[普匿]广东省东莞市 移动
180.150.191.150:8888@HTTP#[未知]北京市 北京天地祥云科技有限公司联通数据中心
221.4.150.7:8181@HTTP#[未知]广东省佛山市 联通
39.137.77.66:80@HTTP#[高匿]北京市 移动
203.130.46.108:9090@HTTP#[透明]北京市 网宿科技
221.1.200.242:35630@HTTP#[未知]山东省菏泽市曹县 联通
111.13.134.23:80@HTTP#[未知]北京市 移动
182.92.105.136:3128@HTTP#[未知]北京市 阿里巴巴
140.207.50.246:47938@HTTP#[未知]上海市 联通
222.85.28.130:40505@HTTP#[未知]河南省许昌市禹州市 电信
222.160.5.206:8080@HTTP#[未知]吉林省四平市 联通
47.107.160.99:8118@HTTP#[未知]浙江省杭州市 阿里云
218.22.7.62:53281@HTTP#[未知]安徽省合肥市 电信
124.232.133.199:3128@HTTP#[透明]湖南省长沙市 电信IDC机房
124.202.166.171:82@HTTP#[未知]北京市 网宿科技股份有限公司鹏博士集团旗下宽带通用CDN节点
218.60.8.83:3129@HTTP#[未知]辽宁省沈阳市 联通
39.137.77.68:8080@HTTP#[高匿]北京市 移动
111.231.18.136:1080@HTTP#[普匿]上海市 腾讯云
117.191.11.72:8080@HTTP#[高匿]新疆 移动
210.34.24.103:3128@HTTP#[透明]福建省宁德市 宁德师范学院
101.251.216.103:8080@HTTP#[未知]北京市海淀区 北龙中网(北京)科技有限公司(BGP)
60.217.158.163:8060@HTTP#[未知]山东省威海市荣成市 联通
60.216.60.234:8060@HTTP#[未知]山东省 BGP大带宽业务机柜段
114.249.119.9:9000@HTTP#[未知]北京市 联通
111.13.134.22:80@HTTP#[未知]北京市 移动
183.161.29.127:8060@HTTP#[未知]安徽省安庆市 电信
39.137.107.98:80@HTTP#[高匿]北京市 移动
222.217.68.17:56509@HTTP#[未知]广西柳州市 电信
59.48.237.6:8060@HTTP#[未知]山西省吕梁市孝义市 G
183.3.221.10:3128@HTTP#[未知]广东省深圳市 电信
117.141.155.241:53281@HTTP#[未知]广西 移动
114.55.92.9:9999@HTTP#[透明]浙江省杭州市 阿里云BGP数据中心
114.115.200.87:8080@HTTP#[透明]北京市海淀区 联通
101.132.149.193:8080@HTTP#[普匿]上海市 阿里云
111.11.100.13:8060@HTTP#[未知]河北省 移动
111.63.135.109:80@HTTP#[未知]河北省 移动
218.28.238.165:3128@HTTP#[透明]河南省郑州市 联通
222.223.182.66:8000@HTTP#[未知]河北省沧州市 电信
60.205.202.3:3128@HTTP#[透明]北京市 阿里云BGP服务器
114.115.214.122:8080@HTTP#[透明]北京市海淀区 联通
119.41.236.180:8010@HTTP#[未知]海南省三亚市 电信
118.24.246.249:80@HTTP#[未知]广西柳州市高新区 视虎科技有限公司
223.99.163.130:63000@HTTP#[未知]山东省 移动
111.77.101.152:8118@HTTP#[普匿]江西省萍乡市 电信
210.22.176.146:47578@HTTP#[高匿]上海市 联通
115.231.130.3:9999@HTTP#[高匿]浙江省杭州市 电信
124.156.108.71:82@HTTP#[未知]浙江省宁波市 中移铁通
61.164.39.67:53281@HTTP#[未知]浙江省杭州市 电信
113.207.69.68:80@HTTP#[未知]重庆市 联通
139.217.134.187:8080@HTTP#[未知]北京市 微软(中国)有限公司
221.1.205.74:8060@HTTP#[未知]山东省菏泽市 联通
49.64.86.43:8080@HTTP#[高匿]江苏省苏州市 电信
39.135.24.11:80@HTTP#[高匿]北京市 移动
116.196.90.176:3128@HTTP#[未知]北京市 电信
49.51.70.42:1080@HTTP#[未知]上海市浦东新区 盛大计算机(上海)有限公司
47.104.179.212:8080@HTTP#[普匿]山东省青岛市 阿里云
222.72.166.235:53281@HTTP#[未知]上海市奉贤区 电信
119.180.143.207:8060@HTTP#[未知]山东省 联通
175.10.24.82:3128@HTTP#[未知]湖南省长沙市 电信
112.65.52.28:9000@HTTP#[未知]上海市徐汇区 联通漕河泾数据中心
47.94.213.22:8888@HTTP#[未知]北京市 阿里云
124.207.82.166:8008@HTTP#[未知]北京市朝阳区 鹏博士长城宽带
123.207.217.104:1080@HTTP#[未知]广东省广州市 腾讯云
120.132.53.21:8888@HTTP#[未知]北京市 天地祥云云谷数据中心(亦庄经济开发区经海二路28号1号楼6楼)
47.111.8.157:80@HTTP#[未知]浙江省杭州市 阿里云
118.24.88.240:1080@HTTP#[未知]广西柳州市高新区 视虎科技有限公司
120.234.63.196:3128@HTTP#[未知]广东省佛山市 移动
218.60.8.98:3129@HTTP#[未知]辽宁省沈阳市 联通
111.231.87.160:8088@HTTP#[未知]上海市 腾讯云
110.189.152.86:31061@HTTP#[未知]四川省自贡市 电信
42.228.3.158:8080@HTTP#[未知]河南省郑州市 联通
118.25.214.123:8888@HTTP#[普匿]河北省廊坊市 中移铁通
120.210.219.74:8080@HTTP#[高匿]安徽省合肥市 移动
218.89.14.142:8060@HTTP#[未知]四川省乐山市 电信
118.24.128.46:1080@HTTP#[未知]广西柳州市高新区 视虎科技有限公司
163.204.246.221:9999@HTTP#[未知]广东省汕尾市陆丰县 联通
59.172.27.6:38380@HTTP#[高匿]湖北省武汉市 电信
112.84.178.21:8888@HTTP#[高匿]江苏省扬州市 联通
139.199.153.25:1080@HTTP#[未知]广东省广州市 深圳市腾讯计算机系统有限公司IDC机房(电信)
218.108.175.15:80@HTTP#[透明]浙江省杭州市 华数宽带
163.125.156.107:8888@HTTP#[未知]广东省深圳市 联通
210.22.5.117:3128@HTTP#[透明]广东省深圳市 联通
101.231.104.82:80@HTTP#[未知]上海市 电信
    '''
    use_ips = []
    IPAgents = s_ips.split("\n")
    for tmp_ip in IPAgents:
        tmp_ip = tmp_ip.split("@")[0]
        import urllib.request
        proxy = urllib.request.ProxyHandler({"http": "http://" + tmp_ip})
        opener = urllib.request.build_opener(proxy)
        urllib.request.install_opener(opener)
        try:
            data = urllib.request.urlopen('http://www.baidu.com', timeout=2).read().decode('utf-8', 'ignore')
            if len(data) > 5000:
                print(tmp_ip + ':可用')
                # print(data)
                use_ips.append(tmp_ip)
            else:
                print(tmp_ip + ':无效')
        except:
            print(tmp_ip + ':无效！！!')

    print("--------可用-----------")
    for use_ip in use_ips:
        print('\'%s\',' % use_ip)


def get_cookie():
    s = "s_ViewType=10; _lxsdk_cuid=16b8d5ede3fc8-02e6c6ce1198328-70226752-13c680-16b8d5ede3f6e; _lxsdk=16b8d5ede3fc8-02e6c6ce1198328-70226752-13c680-16b8d5ede3f6e; _hc.v=f134a75b-e4c8-bc9a-fef8-5a204c0a1d0b.1561444934; cy=5; cye=nanjing"
    dic = {}
    for item in s.split(";"):
        dic[item.split("=")[0].strip()] = item.split("=")[1].strip()
    print(dic)


if __name__ == '__main__':
    # t = random.random()
    # print(t)
    # test_ip()
    # get_cookie()
    # print("%x" % random.randint(0x100, 0xfff))
    # print("%x%x" % (random.randint(0x100, 0xfff), random.randint(0x100, 0xfff)))
    print('16b9%x%x-%x-%x-c3b%%7C%%7C%d' % (
        (random.randint(0x1000, 0xffff), random.randint(0x100, 0xfff), random.randint(0x100, 0xfff),
         random.randint(0x10, 0xfff), 99)))

    # l = []
    # for i in list(range(10)):
    #     print(i)
    #     l.append(i)
    # print(type(list(range(0,1))))
    # print(type(l))
