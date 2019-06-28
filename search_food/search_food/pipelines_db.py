# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# import xlwt
import logging
import time

import openpyxl
from openpyxl import Workbook

from run_dzdp import get_shops
from search_food.items import ShopItem, TypeItem, DbTypeItem
import os


class DbPipeline(object):

    def __init__(self):
        print("-------start--------")
        self.f = open("tmp.txt", "w+")
        self.f.write("1")
        self.f.seek(0)
        self.f.close()

    def process_item(self, item, spider):
        # logging.debug(type(item))
        # logging.debug(type(item) is ShopItem)
        if type(item) is DbTypeItem:
            item.save()
        return item

    def close_spider(self, spider):
        print("-------close_spider--------")
        self.f = open("tmp.txt", "w+")
        self.f.write("0")
        self.f.seek(0)
        self.f.close()
