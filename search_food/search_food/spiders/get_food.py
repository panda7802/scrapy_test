# -*- coding: utf-8 -*-
import logging
import sys
import time
import traceback
from imp import reload

import scrapy
from scrapy import Request

from search_food.items import ShopItem, TypeItem
from search_food.spiders import value

reload(sys)
# sys.setdefaultencoding('utf-8')


class GetFoodSpider(scrapy.Spider):
    name = 'get_shops'
    allowed_domains = ['www.dianping.com']
    start_urls = ['http://www.dianping.com/nanjing/ch10']

    is_test = False
    # 每种类型最多几页d
    max_type_page = 10

    D_NUM = {u'\uf70d': "3", u'\uf404': "5", u'\uec2d': "0", u'\uf810': "8", u'\ue4ff': "2",
             u'\ue6ec': "4", u'\ue27b': "9", u'\ue284': "7", u'\ue65d': "7"}

    # 类型信息
    type_info = {}
    type_names = []

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

    def start_requests(self):
        yield Request(self.start_urls[0],
                      headers=self.def_headers,
                      callback=self.parse_types)

    def parse(self, response):
        pass

    def parse_types(self, response):
        """
        获取类型
        :param response:
        :return:
        """
        if response.status != 200:
            logging.error("get err ,url : " + response.url)
            return

        types = response.xpath('//div[@id="classfy"]//a')
        for index, type_item in enumerate(types):
            if self.is_test and index > 1:
                  break

            try:
                href = str(type_item.xpath("./@href").extract()[0])
                type_name = str(type_item.xpath("./span//text()").extract()[0])
                # logging.debug(type_name + " : " + str(href))
                self.type_names.append(type_name)
                self.type_info[type_name] = href
            except Exception:
                traceback.print_exc()

        logging.debug("result : -------")
        for index, key in enumerate(self.type_names):
            logging.debug(str(index) + " : " + key + " : " + self.type_info[key])

            # 存类型
            type_item = TypeItem()
            type_item['name'] = key
            yield type_item

            yield Request(self.type_info[key],
                          headers=self.def_headers, meta={'type_name': key, 'page_index': 1},
                          callback=self.parse_list, dont_filter=True)

            time.sleep(0.5)

    def parse_list(self, response):
        """
        获取列表
        :param response:
        :return:
        """
        if response.status != 200:
            logging.debug("get err ,url : " + response.url)
            return

        # 本类型第几页
        page_index = int(response.meta['page_index'])
        logging.debug(response.meta['type_name'] + " 第" + str(page_index) + "页")

        # 商店列表
        shops = response.xpath('//*[@id="shop-all-list"]//ul//li')
        for index, shop_item in enumerate(shops):
            if self.is_test and index > 2:
                break

            # print type(shop_item)
            shop_name = shop_item.xpath('.//h4//text()').extract()[0]
            href = shop_item.xpath('.//div[@class="tit"]//a//@href').extract()[0]
            shop_id = shop_item.css("a::attr(data-shopid)").extract()[0]
            logging.debug(shop_name + " . " + str(shop_id) + " : " + href)

            # 先获取商店提纲(列表)，然后再进行详情获取
            item = ShopItem()
            item['name'] = shop_name
            item['pic'] = 0
            item['price'] = 0
            item['bad'] = 0
            item['good'] = -1
            item['common'] = 0
            item['type_name'] = response.meta['type_name']
            item['phone'] = 0
            item['url'] = href
            item['row_num'] = "-1"

            yield item

            # 获取详情
            # yield Request(href, headers=self.def_headers, callback=self.parse_detail,
            #               meta={'type_name': response.meta['type_name']}, dont_filter=True)
            # time.sleep(0.5)

        if self.is_test:
            return

        # 只获取前5页
        if page_index >= self.max_type_page:
            return
        else:
            page_index += 1

        # 等待两秒
        time.sleep(2)

        # 下一页
        next_page = response.xpath('//a[@class="next"]//@href').extract()
        if len(next_page) > 0:
            next_page_href = next_page[0]
            # logging.debug(response.meta['type_name'] + "   下一页")
            yield Request(next_page_href,
                          headers=self.def_headers,
                          meta={'type_name': response.meta['type_name'], 'page_index': page_index},
                          callback=self.parse_list, dont_filter=True)
        else:
            logging.debug("-----------已经到最后一页-----------")

    def parse_detail(self, response):
        """
        获取详情
        :param response:
        :return:
        """
        if response.status != 200:
            logging.debug("get err ,url : " + response.url)
            return

        # 店名
        name = response.xpath('//*[@class="shop-name"]/text()').extract_first()
        if None is name:
            return
        logging.debug(name)

        # # 获取坐标
        # map_img = response.xpath('//*[@class="aside-bottom"]').extract()
        # logging.debug(map_img)
        #
        # return

        # 价格,注意：此处text()为俩斜杠
        price_items = response.xpath('//*[@id="avgPriceTitle"]//text()').extract()
        s_price = ""
        for i, item in enumerate(price_items):
            if item in value.D_NUM:
                s_price += value.D_NUM[item]
            else:
                s_price += item

        s_price = s_price.replace("人均", "").replace("元", "").replace("：", "").replace(":", "").replace(" ", "")

        # 电话
        phone_items = response.xpath('//*[@class="expand-info tel"]//text()').extract()
        phone = ""
        for i, item in enumerate(phone_items):
            if item in value.D_NUM:
                phone += value.D_NUM[item]
            else:
                phone += item

        phone = phone.replace("电话", "").replace(":", "").replace("：", "")

        # 图片
        pic = response.xpath('//*[@class="filter-item J-filter-pic"]//span/text()').extract_first() or "0"
        # 好评
        good = response.xpath('//*[@class="filter-item J-filter-good"]//span/text()').extract_first() or "0"
        # 中评
        common = response.xpath('//*[@class="filter-item J-filter-common"]//span/text()').extract_first() or "0"
        # 差评
        bad = response.xpath('//*[@class="filter-item J-filter-bad"]//span/text()').extract_first() or "0"

        # 存储
        item = ShopItem()
        item['name'] = name
        item['pic'] = pic.replace(")", "").replace("(", "")
        item['price'] = s_price
        item['bad'] = bad.replace(")", "").replace("(", "")
        item['good'] = good.replace(")", "").replace("(", "")
        item['common'] = common.replace(")", "").replace("(", "")
        item['type_name'] = response.meta['type_name']
        item['phone'] = phone
        item['url'] = response.url
        item['row_num'] = "-1"

        # logging.debug(item)
        yield item

        # TODO 地址暂不获取
        # html, css_link = self.get_css_link(response.url)
        # logging.debug(css_link)
        # logging.debug(html)
        # addr = response.xpath('//*[@id="address"]').extract()
        # print addr
