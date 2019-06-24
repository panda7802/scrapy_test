# -*- coding: utf-8 -*-

from __future__ import absolute_import

from scrapy import cmdline
from scrapy.crawler import CrawlerRunner


def get_shop_details():
    """
    获取商店详情
    :return:
    """
    args = "scrapy crawl get_shop_info".split()
    cmdline.execute(args)
    print("-----------")


runner = CrawlerRunner()


if __name__ == '__main__':
    # crawl()

    get_shop_details()
