# coding: utf-8
import re
import time
import traceback
import urllib.request as urllib2

from urllib3.connectionpool import xrange

can_use = []


def getDL(page):
    url = 'http://www.xicidaili.com/nt/{}'.format(page)
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }

    req = urllib2.Request(url, headers=header)
    res = urllib2.urlopen(req)
    html = str(res.read())

    srclist = re.findall(
        r'<tr class=(.|\n)*?<td>(\d+\.\d+\.\d+\.\d+)</td>(.|\n)*?<td>(\d+)</td>(.|\n)*?<td>(HTTP|HTTPS)</td>', html)
    xlist = []
    for item in srclist:
        xlist.append((item[5], item[1], item[3]))
    return xlist


def testDL(ipstr):
    print("%s:%s" % (ipstr[1], ipstr[2]))
    proxy = urllib2.ProxyHandler({'http': "{}:{}".format(ipstr[1], ipstr[2])})
    opener = urllib2.build_opener(proxy)
    urllib2.install_opener(opener)

    try:
        test_url = 'http://httpbin.org/ip'
        # testUrl = 'http://2017.ip138.com/ic.asp'
        req = urllib2.Request(test_url)
        res = urllib2.urlopen(req, timeout=10).read()
        print("********************* √ {}    -- {}".format(ipstr, res))

        with open("ok.txt", "a") as f:
            # f.write("{} {} {}\n".format(ipstr[0], ipstr[1], ipstr[2]))
            f.write("'{}:{}',\n".format(ipstr[1], ipstr[2]))
            f.close()
    except Exception as e:
        print("******** ×, {} -- {}".format(ipstr, e))
    time.sleep(0.2)


def startTask():
    for page in xrange(5):
        try:
            list = getDL(page + 1)
            print(list)
            for item in list:
                testDL(item)
        except:
            traceback.print_exc()


if __name__ == '__main__':
    startTask()
