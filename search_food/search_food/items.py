# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from dzdp.models import DzdpType, DzdpCityType, DzdpShop
from scrapy_djangoitem import DjangoItem


class SearchFoodItem(scrapy.Item):
    pass


class ShopItem(scrapy.Item):
    # define the fields for your item here like:
    # 店名
    name = scrapy.Field()
    # excel的第几行
    row_num = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 图片
    pic = scrapy.Field()
    # 好评
    good = scrapy.Field()
    # 中评
    common = scrapy.Field()
    # 差评
    bad = scrapy.Field()
    # 类型名称
    type_name = scrapy.Field()
    # 电话
    phone = scrapy.Field()
    # url
    url = scrapy.Field()


class TypeItem(scrapy.Item):
    # 名称
    name = scrapy.Field()


class DbTypeItem(DjangoItem):
    django_model = DzdpType


class DbTypeCityItem(DjangoItem):
    django_model = DzdpCityType


class DbShopItem(DjangoItem):
    django_model = DzdpShop
