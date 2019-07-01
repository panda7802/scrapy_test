# -*- coding: utf-8 -*-
import logging
import sys
import time
import traceback
from imp import reload

import scrapy
from django.db.models import Q
from scrapy import Request

from dzdp.models import DzdpCity, DzdpType, DzdpCityType, DzdpShop, DzdpShopType
from search_food.items import ShopItem, TypeItem, DbShopItem
from search_food.spiders import get_types

reload(sys)


# sys.setdefaultencoding('utf-8')

def get_type_url(city_tag, type_parent_tag, type_tag, page):
    url = "http://www.dianping.com/%s/%s/%sp%d" % (city_tag, type_parent_tag, type_tag, page)
    return url


is_test = False
# 每种类型最多几页
max_type_page = 50


class GetListSpider(scrapy.Spider):
    name = 'get_lists'
    allowed_domains = ['www.dianping.com']
    start_urls = ['*']

    D_NUM = {u'\uf70d': "3", u'\uf404': "5", u'\uec2d': "0", u'\uf810': "8", u'\ue4ff': "2",
             u'\ue6ec': "4", u'\ue27b': "9", u'\ue284': "7", u'\ue65d': "7"}

    def start_requests(self):
        need_get_cities = DzdpCity.objects.filter(is_need=True)
        need_get_types = DzdpType.objects.filter(is_need=True)
        # 找到需要爬的城市类型
        city_types = DzdpCityType.objects. \
            filter(Q(city__in=need_get_cities) \
                   & Q(type__parent_type__in=need_get_types) \
                   & Q(is_max_page=False))
        for index, item in enumerate(city_types):
            # if index > 1:
            #     break
            curr_page = item.curr_page
            if curr_page < 1:
                curr_page = 1
            url = get_type_url(item.city.tag, item.type.parent_type.tag, item.type.tag, curr_page)
            print(url)
            yield Request(url, headers=get_types.def_headers, meta={'city_type': item, 'page_index': curr_page},
                          dont_filter=True)

    def parse(self, response):
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
        city_type = response.meta['city_type']
        logging.debug(city_type.type.name + " 第" + str(page_index) + "页")

        # 商店列表
        shops = response.xpath('//*[@id="shop-all-list"]//ul//li')
        for index, shop_item in enumerate(shops):
            if is_test and index > 2:
                break

            # print type(shop_item)
            shop_name = shop_item.xpath('.//h4//text()').extract()[0]
            href = shop_item.xpath('.//div[@class="tit"]//a//@href').extract()[0]
            shop_id = shop_item.css("a::attr(data-shopid)").extract()[0]
            logging.debug("%s - %s , %s : %s " % (city_type.type.name, shop_name, str(shop_id), href))

            shop_item = DzdpShop.objects.filter(shop_id=shop_id).first()
            if shop_item is None:
                try:
                    # 先获取商店提纲(列表)，然后再进行详情获取
                    item = DbShopItem()
                    item['name'] = shop_name
                    item['shop_id'] = shop_id
                    item['pic'] = -1
                    item['price'] = 0
                    item['bad'] = 0
                    item['good'] = 0
                    item['common'] = 0
                    item['type'] = response.meta['city_type'].type
                    item['city'] = response.meta['city_type'].city
                    item['phone'] = 0
                    item['url'] = href
                    item.save()
                except Exception:
                    traceback.print_exc()
                    logging.error(traceback.format_exc())

            # 存商店类型
            shop_item = DzdpShop.objects.filter(shop_id=shop_id).first()
            shop_type = DzdpShopType.objects.filter(Q(shop__id=shop_item.id) \
                                                    & Q(type__id=city_type.type.id)).first()
            if shop_type is None:
                try:
                    shop_type = DzdpShopType()
                    shop_type.shop = shop_item
                    shop_type.type = city_type.type
                    shop_type.save()
                except Exception:
                    traceback.print_exc()

            # 获取详情
            # yield Request(href, headers=self.def_headers, callback=self.parse_detail,
            #               meta={'type_name': response.meta['type_name']}, dont_filter=True)
            time.sleep(0.2)

        # 只获取前几页
        if page_index >= max_type_page:
            return
        else:
            page_index += 1

        # 等待两秒
        time.sleep(0.5)

        # 下一页
        next_page = response.xpath('//a[@class="next"]//@href').extract()
        city_type.curr_page = page_index

        if len(next_page) > 0:
            next_page_href = next_page[0]
            city_type.save()
            # logging.debug(response.meta['type_name'] + "   下一页")
            yield Request(next_page_href,
                          headers=get_types.def_headers,
                          meta={'city_type': city_type, 'page_index': page_index},
                          dont_filter=True)
        else:
            city_type['is_max_page'] = True
            city_type.save()
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
            if item in self.D_NUM:
                s_price += self.D_NUM[item]
            else:
                s_price += item

        s_price = s_price.replace("人均", "").replace("元", "").replace("：", "").replace(":", "").replace(" ", "")

        # 电话
        phone_items = response.xpath('//*[@class="expand-info tel"]//text()').extract()
        phone = ""
        for i, item in enumerate(phone_items):
            if item in self.D_NUM:
                phone += self.D_NUM[item]
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
