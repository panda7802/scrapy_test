# -*- coding: utf-8 -*-
import logging
import traceback

import scrapy
from django.db.models import Q
from scrapy import Request

from dzdp.models import DzdpCity, DzdpType, DzdpCityType
from search_food.items import DbTypeItem, DbTypeCityItem

def_headers = {
    'Host': 'www.dianping.com',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0',
    'Accept': ' text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Cookie': '',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0'
}

is_test = False
# 每种类型最多几页d
max_type_page = 10


class GetTypesSpider(scrapy.Spider):
    name = 'get_types'
    allowed_domains = ['*']
    start_urls = ['http://*/']

    def start_requests(self):

        # 需要获取的城市
        need_get_cities = DzdpCity.objects.filter(is_need=True)
        need_get_types = DzdpType.objects.filter(is_need=True)
        for city in need_get_cities:
            for dzdp_type in need_get_types:
                # print(dzdp_type)
                url = "http://www.dianping.com/%s/%s" % (city.tag, dzdp_type.tag)
                # print(url)
                yield Request(url, headers=def_headers, meta={"city": city, "type": dzdp_type})

    def parse(self, response):
        # print(response.url)
        # print(response.meta['city'])
        # print(response.meta['type'])
        # print("--------")

        # item = DbTypeItem()
        # item['name'] = 'aaa'
        # return

        types = response.xpath('//div[@id="classfy"]//a')
        for index, type_item in enumerate(types):
            if is_test and index > 1:
                break

            try:
                href = str(type_item.xpath("./@href").extract()[0])
                type_name = str(type_item.xpath("./span//text()").extract()[0])

                logging.debug(type_name + " : " + str(href))
                # 插入到类型表中
                dzdp_type = DzdpType.objects.filter(name=type_name).first()
                if dzdp_type is None:
                    item = DbTypeItem()
                    item['name'] = type_name
                    item['tag'] = href[href.rfind("/")+1:]
                    item['parent_type'] = response.meta['type']
                    item.save()
                    dzdp_type = DzdpType.objects.filter(name=type_name).first()

                dzdp_city_type = DzdpCityType.objects \
                    .filter(Q(city=response.meta['city']) & Q(type=response.meta['type'])).first()
                if dzdp_city_type is None:
                    item = DbTypeCityItem()
                    item['city'] = response.meta['city']
                    item['type'] = dzdp_type
                    item.save()

            except Exception:
                traceback.print_exc()
                logging.error(traceback.format_exc())

        # logging.debug("result : -------")
        # for index, key in enumerate(self.type_names):
        #     logging.debug(str(index) + " : " + key + " : " + self.type_info[key])
        #
        #     # 存类型
        #     type_item = DbTypeItem()
        #     type_item['name'] = key
        #     # yield type_item
        #
        #     # yield Request(self.type_info[key],
        #     #               headers=self.def_headers, meta={'type_name': key, 'page_index': 1},
        #     #               callback=self.parse_list, dont_filter=True)
        #     #
        #     # time.sleep(0.5)
