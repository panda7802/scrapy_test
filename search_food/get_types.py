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
    get_lists()
    # from dzdp.models import DzdpCity, DzdpType, DzdpCityType
    # need_get_cities = DzdpCity.objects.filter(is_need=True)
    # need_get_types = DzdpType.objects.filter(is_need=True)
    # # 找到需要爬的城市类型
    # city_types = DzdpCityType.objects. \
    #     filter(Q(city__in=need_get_cities) & Q(type__parent_type__in=need_get_types))
    # for item in city_types:
    #     print(item)
    # print("%d , %d" % (len(need_get_cities), len(need_get_types)))
