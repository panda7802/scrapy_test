# -*- coding: utf-8 -*-
import logging
import random
import re
import time
import traceback
import urllib

import scrapy
from scrapy import Request

from dzdp.models import DzdpShop
from search_food.spiders import get_types


# def_cookie = {
#     's_ViewType': '10',
#     '_lxsdk_cuid': '16b8d5ede3fc8-02e6c6ce1198328-70226752-13c680-16b8d5ede3f6e',
#     '_lxsdk': '16b8d5ede3fc8-02e6c6ce1198328-70226752-13c680-16b8d5ede3f6e',
#     '_hc.v': 'f134a75b-e4c8-bc9a-fef8-5a204c0a1d0b.1561444934',
#     '_lxsdk_s': '16b92c99bb7-bb-a2b-591%7C%7C79'
# }

## chrom的cookie
# def_cookie = {
#     's_ViewType': '10',
#     '_lxsdk_cuid': '16b9170d664c8-08638a5d100908-3f72045a-13c680-16b9170d664bb',
#     '_lxsdk': '16b9170d664c8-08638a5d100908-3f72045a-13c680-16b9170d664bb',
#     '_hc.v': 'c5894a62-bebd-65c3-1e63-485d6b1c4eb8.1561513220',
#     '_lxsdk_s': '16b92c46963-99f-700-931%7C%7C136'
# }


class GetShopInfoSpider(scrapy.Spider):
    name = 'get_shop2db'
    allowed_domains = ['dianping.com']
    start_urls = ['http://www.dianping.com/shop/97475643/']

    D_NUM = {u'\uf70d': "3", u'\uf404': "5", u'\uec2d': "0", u'\uf810': "8", u'\ue4ff': "2",
             u'\ue6ec': "4", u'\ue27b': "9", u'\ue284': "7", u'\ue65d': "7"}

    cookies = []

    # 是否有重定向
    have_re = False

    def start_requests(self):
        s = "_lxsdk_s=16b97dc5e21-e3d-4a2-5f1%7C%7C1"
        # s = "_lxsdk_s=16b97dd2f21-379-52-1cd%7C%7C1"
        # s = "_lxsdk_cuid=16b983f2ed2c8-0e0d047a2ec123-3f72045a-13c680-16b983f2ed2c8; _lxsdk=16b983f2ed2c8-0e0d047a2ec123-3f72045a-13c680-16b983f2ed2c8; _hc.v=e3704ee1-d39a-a68f-34ad-53348b86d271.1561627407; _lxsdk_s=16b983f2e01-596-a7b-c3b%7C%7C36"
        # s = "_lxsdk_cuid=16b983f2ed2c8-0e0d047a2ec123-3f72045a-13c680-16b983f2ed2c8; _lxsdk=16b983f2ed2c8-0e0d047a2ec123-3f72045a-13c680-16b983f2ed2c8; _hc.v=e3704ee1-d39a-a68f-34ad-53348b86d271.1561627407; _lxsdk_s=16b983f2e01-596-a7b-c3b%7C%7C52"
        def_cookie = {}
        for item in s.split(";"):
            if item is None:
                continue
            if len(item.strip()) > 3:
                def_cookie[item.split("=")[0].strip()] = item.split("=")[1].strip()

        # shops = DzdpShop.objects.filter(pic__lt=0).all()
        shops = DzdpShop.objects.filter(pic=-1).all()
        for index, shop in enumerate(shops):
            # if index > 0:
            #     break
            try:
                head = get_types.def_headers
                head['User-Agent'] = \
                    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.102 Safari/537.36 Vivaldi/2.6.1566.44'
                # head['User-Agent'] = random.choice(get_types.uas)
                # 设置cookie
                cookie = def_cookie
                # 凭借多年的开发经验判断的
                # cookie['_lxsdk_s'] = '16b9bd099a3-5ea-439-50e%%7C%%7C%d' % (index / 10 + 30)
                cookie['_lxsdk_s'] = "16bb1465863-7b0-379-da8%%7C%%7C%d" % (index / 10 + 100)
                # print(cookie)
                yield Request(shop.url, headers=head, cookies=cookie, \
                              meta={'shop': shop}, dont_filter=True)
                # 伪造每次间隔时间不同
                if self.have_re:
                    time.sleep(random.random() * 10)
                else:
                    time.sleep(random.random() * 2)
            except Exception:
                traceback.print_exc()
                logging.error(traceback.format_exc())

    def parse(self, response):
        """
        获取详情
        :param response:
        :return:
        """
        try:
            if response.status == 404:
                shop = response.meta['shop']
                logging.error("%s 不存在 : %s" % (shop.name, shop.url))
                shop.pic = -2
                shop.save()
                return

            if response.status != 200:
                self.have_re = True
                logging.error("Get shop error , url : %s , status : %d" % (response.url, response.status))
                return

            # 店名
            name = response.xpath('//*[@class="shop-name"]/text()').extract_first()
            if None is name:
                self.have_re = True
                logging.error("被重定向：%s" % response.url)
                return
            else:
                self.have_re = False
            logging.debug(name + " ========= " + response.url)

            shop = response.meta['shop']

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

            # # 获取地址
            # try:
            #     # url = "http://www.dianping.com/ajax/json/shopDynamic/shopAside?shopId=%s" % shop.shop_id
            #     url = "http://www.dianping.com/ajax/json/shopDynamic/shopAside?shopId=113163779"
            #     # head = {'User-Agent': random.choice(get_types.uas)}
            #     head = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0'}
            #     print(url)
            #     url_request = urllib.request.Request(url=url, headers=head)
            #     url_request_open = urllib.request.urlopen(url_request)
            #     print(url_request_open)
            #     # 响应状态码
            #     print(url_request_open.status)
            #     if url_request_open.status == 200:
            #         # 相应原因
            #         print(url_request_open.reason)
            #         # 读取内容并解码
            #         print(url_request_open.read().decode())
            # except:
            #     traceback.print_exc()
            #     logging.error(traceback.format_exc())

            # 存储
            shop.pic = pic.replace(")", "").replace("(", "")
            if re.match("\d+(\.\d+)?", s_price) is None:
                shop.price = 0
            else:
                shop.price = float(s_price)
            shop.bad = int(bad.replace(")", "").replace("(", ""))
            shop.good = int(good.replace(")", "").replace("(", ""))
            shop.common = int(common.replace(")", "").replace("(", ""))
            shop.phone = phone
            logging.debug("准备存 : %s " % str(shop))
            shop.save()
        except:
            traceback.print_exc()
            logging.error(traceback.format_exc())
