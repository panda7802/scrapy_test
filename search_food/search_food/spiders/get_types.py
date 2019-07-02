# -*- coding: utf-8 -*-
import logging
import traceback

import scrapy
from django.db.models import Q
from scrapy import Request

from dzdp.models import DzdpCity, DzdpType, DzdpCityType
from search_food.items import DbTypeItem, DbTypeCityItem

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

def_headers = {
    # 'Host': 'www.dianping.com',
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    # 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0',
    # 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36 OPR/60.0.3255.170',
    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    # 'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate',
    # 'Connection': 'keep-alive',
    # 'Cookie': '__mta=142037261.1560844813116.1560844813116.1560844813116.1; cy=5; cye=nanjing; _lxsdk_cuid=16b1afa8f30c8-0d5154320b3f228-70226752-13c680-16b1afa8f31c8; _lxsdk=16b1afa8f30c8-0d5154320b3f228-70226752-13c680-16b1afa8f31c8; _hc.v=d2bf0bc8-ef22-e77a-8572-7fdd38678f60.1559525758; s_ViewType=10; hibext_instdsigdipv2=1; aburl=1; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_s=16b8c61cc3a-668-fd3-248%7C%7C122',
    # 'Upgrade-Insecure-Requests': '1',
    # 'If-Modified-Since': 'Tue, 25 Jun 2019 02:05:48 GMT',
    # 'If-None-Match': '62bbb6c1a987e5ba38c537d1f798c1c9',
    # 'Cache-Control': 'max-age=0'
}

is_test = False
# 每种类型最多几页d
max_type_page = 50


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
                    item['tag'] = href[href.rfind("/") + 1:]
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
