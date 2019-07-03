import _thread
import os
import random
import signal
import threading
import time
import traceback

import requests

uas = ['Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
       'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0',
       'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36 OPR/60.0.3255.170',
       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
       'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
       'Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50',
       'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)',
       'Mozilla/5.0 (Windows; U; Windows NT 6.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12',
       'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)',
       'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)',
       'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.33 Safari/534.3 SE 2.X MetaSr 1.0',
       'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)',
       'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201',
       'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E) QQBrowser/6.9.11079.201',
       'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0'
       ]

proxies = ['113.247.252.114:9090',
           '58.240.220.86:53281',
           '163.125.69.146:8888',
           '121.79.131.58:8080',
           '114.249.118.244:9000',
           '210.26.49.88:3128',
           '110.172.221.241:8080',
           '58.249.55.222:9797',
           '58.17.125.215:53281',
           '115.171.152.19:9000',
           '120.26.208.102:88',
           '121.15.254.156:888'
           ]

# global success
success = 0


def post_ticket():
    """
    开始投票
    :return:
    """
    url = 'https://jtjk.xinxife.org/index.php?m=Teams&c=IndexTeams&a=do_ticket'  # django接口路径

    parms = {
        'tickets_num_id': '442',  # 发送给服务器的内容
        'type': 1
    }

    # ip = {'http': 'http://%s" % random.choice(proxies)'}
    # ip = {'http': 'http://%s' % random.choice(proxies)}
    max = 10000000
    obj_ticket = 12345
    global success
    # proxies = []#直接灌,不进行代理
    for index in list(range(0, max)):
        tmp = ''
        try:
            headers = {  # 请求头信息
                'Referer': 'https://jtjk.xinxife.org/index.php?m=Teams&c=IndexTeams&a=teams_detail&teams_id=417',
                'User-agent': random.choice(uas),
            }
            # print(len(proxies))
            if len(proxies) > 0:
                tmp = random.choice(proxies)
                sip = 'http://%s' % tmp
                ip = {'http': sip, 'https': sip}
                resp = requests.post(url, data=parms, headers=headers, proxies=ip, timeout=2)  # POST请求
            else:
                resp = requests.post(url, data=parms, headers=headers, timeout=1)  # POST请求

            # 服务器返回的数据
            text = resp.text
            if text.__contains__("投票成功"):
                success += 1
                # success = success + 1
                print("投票成功:%d/%d \t %s,\t%s\t" % (success, obj_ticket, tmp, threading.current_thread().name))
                if success >= obj_ticket:
                    print("-----投票完成 , 一共%d票------" % obj_ticket)
                    os.kill(os.getpid(), signal.SIGKILL)
                    return
            else:
                print("投票失败 %s " % tmp)
                print(text)
            time.sleep(0.5 + random.random())
        except:
            try:
                # print("投票异常 %s , %s" % (tmp, threading.current_thread().name))
                time.sleep(0.5)
            except:
                traceback.print_exc()

    print("投票成功%d次" % success)


class TicketThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        print("开始线程：" + self.name)
        post_ticket()
        print("退出线程：" + self.name)


if __name__ == "__main__":
    # 创建多个线程
    try:
        for i in list(range(0, 30)):
            thread1 = TicketThread('t%s' % (i + 1))
            thread1.start()
        while 1:
            time.sleep(1)
            pass
    except:
        print("Error: unable to start thread")
        traceback.print_exc()
