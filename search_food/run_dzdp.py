# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
import sys

import django
from scrapy import cmdline


def get_types():
    """
    获取类型列表
    :return:
    """
    args = "scrapy crawl get_types".split()
    cmdline.execute(args)
    print("-----------")


def get_lists():
    """
    获取类型列表和商店列表
    :return:
    """
    args = "scrapy crawl get_lists".split()
    cmdline.execute(args)
    print("-----------")


def get_shops():
    """
    获取类型列表和商店列表
    :return:
    """
    f1 = open("tmp.txt", "w+")
    from dzdp.models import DzdpShop
    # 是否有需要爬的数据
    tmp_shop = DzdpShop.objects.filter(pic__lt=0).first()
    if tmp_shop is not None:
        f1.close()
        args = "scrapy crawl get_shop2db".split()
        cmdline.execute(args)
        print("-----------")
    else:
        f1.write("2")
    f1.close()


if __name__ == '__main__':
    DJANGO_PROJECT_PATH = '../../lxdzx_server'
    DJANGO_SETTINGS_MODULE = 'lxdzx_server.settings'
    sys.path.insert(0, DJANGO_PROJECT_PATH)
    os.environ['DJANGO_SETTINGS_MODULE'] = DJANGO_SETTINGS_MODULE
    # os.environ.setdefault("DJANGO_SETTINGS_MODULE", DJANGO_SETTINGS_MODULE    )
    # application = django.core.handlers.wsgi.WSGIHandler()
    print("===========setting over===========")
    django.setup()

    # get_types()
    # get_lists()
    get_shops()
