# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
import time

from chardet import UniversalDetector
from scrapy import cmdline


def test_code():
    # l_addr = [u' ', u'\ueee5', u'\uecb6', u'\uf1b7', u'\uf888', u'\u6e38', u'\ue588', u'B', u'\ue4ff', u'\uf616',
    #           u'NJSYC-LB', u'\ue4ff', u'-', u'\uec2d', u'\ue6ec', u'\ue83e', u'\u57df ']
    l_addr = [u'\ue4ff', u'\ue4ff', u'\uec2d', u'\ue6ec']
    CHARSET = ['ASCII', 'GB', 'GB2312', 'GB12345-90', 'GBK', 'BIG5', 'GB18030', 'UCS', 'Hiragino Sans GB', 'Helvetica',
               'utf-8', 'utf-16', 'utf-32']

    detector = UniversalDetector()
    for i, item in enumerate(l_addr):
        print(i, item.encode("utf-8", 'ignore'))
        # print i, item.decode("unicode", 'ignore')
        # chardet.detect(item)
        # detector.reset()
        # detector.feed(str(item))
        # if detector.done:
        #     print("         ", detector.result)
        # detector.close()

        for c in CHARSET:
            try:
                print("       ", c, ":", item.encode(c, 'ignore'))
            except Exception as e:
                print("       ", c, "is not support")


def get_shops():
    """
    获取商店列表
    :return:
    """
    args = "scrapy crawl get_shops".split()
    cmdline.execute(args)


def get_shop_details():
    """
    获取商店详情
    :return:
    """
    args = "scrapy crawl get_shop_info".split()
    cmdline.execute(args)


if __name__ == '__main__':
    # print(1)
    # time.sleep(0.5)
    # print(2)
    get_shops()
    # get_shop_details()

    # os.system("scrapy crawl get_food")
    # os.system("scrapy crawl get_shop_info")

    print("--------------------------------")


    # args = "scrapy crawl get_food".split()
    # cmdline.execute(args)
    # test_code()
