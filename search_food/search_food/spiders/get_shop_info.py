# -*- coding: utf-8 -*-
import logging
import traceback

import re
from random import choice

import openpyxl
import requests
import scrapy
from scrapy import Request

from search_food.items import ShopItem
from search_food.spiders import value


class GetShopInfoSpider(scrapy.Spider):
    name = 'get_shop_info'
    allowed_domains = ['dianping.com']
    start_urls = ['http://www.dianping.com/shop/97475643/']

    # D_NUM = {u'\uf70d': "3", u'\uf404': "5", u'\uec2d': "0", u'\uf810': "8", u'\ue4ff': "2",
    #          u'\ue6ec': "4", u'\ue27b': "9", u'\ue284': "7", u'\ue65d': "7"}

    cookies = []

    def_headers = {
        'Host': 'www.dianping.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.54 Safari/536.5',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Cookie': '',
        'Upgrade-Insecure-Requests': '1',
        # 'If-Modified-Since': 'Thu, 06 Jun 2019 02:14:22 GMT',
        # 'If-None-Match': 'ff8885b489bd97885a1514203d07193a',
        'Cache-Control': 'max-age=0'
    }

    def get_css_link(self, url):
        """
            请求评论首页，获取css样式文件和html文件
        """
        try:
            logging.debug(url)
            res = requests.get(url, headers=self.def_headers)
            html = res.text
            html = html.replace(">", ">\n")
            css_link = re.search(r'<link re.*?css.*?href="(.*?svgtextcss.*?)">', html).groups()
            css_link = 'http:' + css_link[0]
            return html, css_link
        except Exception:
            traceback.print_exc()

    # 是否有重定向
    have_re = False

    def start_requests(self):
        # yield Request(self.start_urls[0],
        #               headers=self.def_headers, meta={'type_name': 'aa'},
        #               callback=self.parse)
        wb = openpyxl.load_workbook("./res_dir/shops.xlsx")
        sheep_names = wb.sheetnames
        for tmp_sheep_name in sheep_names:
            ws = wb.get_sheet_by_name(tmp_sheep_name)
            # if self.have_re:
            #     break
            for row_num, row in enumerate(list(ws.rows)[1:]):
                # if self.have_re:
                #     break
                name = row[0].value
                shop_url = row[8].value
                logging.debug("%s , %d : %s" % (name, row_num, shop_url))
                yield Request(shop_url, headers=self.def_headers,
                              meta={'type_name': tmp_sheep_name, 'row_num': row_num},
                              callback=self.parse)

    def parse(self, response):
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
            self.have_re = True
            logging.debug("被重定向：%s" % response.url)
            return
        logging.debug(name + " ========= " + response.url)
        # return

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
        item['row_num'] = response.meta['row_num']

        # logging.debug(item)
        yield item

        # TODO 地址暂不获取
        # html, css_link = self.get_css_link(response.url)
        # logging.debug(css_link)
        # logging.debug(html)
        # addr = response.xpath('//*[@id="address"]').extract()
        # print addr
