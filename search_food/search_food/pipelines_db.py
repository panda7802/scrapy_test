# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# import xlwt
import logging

import openpyxl
from openpyxl import Workbook

from search_food.items import ShopItem, TypeItem, DbTypeItem
import os


class DbPipeline(object):

    def __init__(self):
        print("-------start--------")

    def process_item(self, item, spider):
        # logging.debug(type(item))
        # logging.debug(type(item) is ShopItem)
        if type(item) is DbTypeItem:
            item.save()
        return item

    def close_spider(self, spider):
        print("-------close_spider--------")
