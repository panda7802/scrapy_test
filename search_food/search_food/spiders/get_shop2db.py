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
from search_food.spiders import get_types, value


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
    start_urls = ['http://www.dianping.com/shop/3083005']

    cookies = []

    # 是否有重定向
    have_re = False

    def_cookie = {}
    addr_cookie = {}

    def count_cookie(self, s):
        """
        计算cookie
        :param s:
        :return:
        """
        res = {}
        for item in s.split(";"):
            if item is None:
                continue
            if len(item.strip()) > 3:
                res[item.split("=")[0].strip()] = item.split("=")[1].strip()
        return res

    def start_requests(self):
        s = "_lxsdk_s=16c18827427-45e-4d9-36d%7C%7C1"
        self.def_cookie = self.count_cookie(s)
        s = "pvhistory=6L+U5ZuePjo8L2Vycm9yL2Vycm9yX3BhZ2U+OjwxNTYzNzg1MjU2NzMzXV9b; m_flash2=1; cityid=1"
        self.addr_cookie = self.count_cookie(s)

        # shops = DzdpShop.objects.filter(pic__lt=0).all()
        # shops = DzdpShop.objects.filter(pic=-1).all()
        shops = DzdpShop.objects.order_by('-lastGetTime').all()[:5]
        for index, shop in enumerate(shops):
            # if index > 0:
            #     break
            if self.have_re:
                break
            try:
                head = get_types.def_headers
                # head['User-Agent'] = \
                #     'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.102 Safari/537.36 Vivaldi/2.6.1566.44'
                # head['User-Agent'] = random.choice(get_types.uas)
                # 设置cookie
                cookie = self.def_cookie
                # 凭借多年的开发经验判断的
                cookie['_lxsdk_s'] = "16bfeb03934-c5e-f83-8a0%%7C%%7C%d" % (index / 10 + 100)

                # 测试用
                # yield Request(self.start_urls[0], headers=head, cookies=cookie,
                #               meta={'shop': shop}, dont_filter=True)
                # return

                yield Request(shop.url, headers=head, cookies=cookie,
                              meta={'shop': shop}, dont_filter=True)

                # 随机ua
                # yield Request(shop.url, headers={'User-Agent': random.choice(get_types.uas)},
                #               meta={'shop': shop}, dont_filter=True)

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
            # int(phone)
            # 图片
            pic = response.xpath('//*[@class="filter-item J-filter-pic"]//span/text()').extract_first() or "0"
            # 好评
            good = response.xpath('//*[@class="filter-item J-filter-good"]//span/text()').extract_first() or "0"
            # 中评
            common = response.xpath('//*[@class="filter-item J-filter-common"]//span/text()').extract_first() or "0"
            # 差评
            bad = response.xpath('//*[@class="filter-item J-filter-bad"]//span/text()').extract_first() or "0"

            # 存储
            shop.pic = pic.replace(")", "").replace("(", "")
            if re.match("\d+(\.\d+)?", s_price) is None:
                shop.price = 0
            else:
                print("url : %s , s_price : %s " % (response.url, s_price))
                shop.price = float(s_price)
            shop.bad = int(bad.replace(")", "").replace("(", ""))
            shop.good = int(good.replace(")", "").replace("(", ""))
            shop.common = int(common.replace(")", "").replace("(", ""))
            shop.phone = phone
            # int(phone)
            # logging.debug("保存 : %s " % str(shop))
            # shop.save()

            # 获取地址
            addr_url = "http://m.dianping.com/shop/%s/map" % shop.shop_id
            print(addr_url)
            yield Request(addr_url, headers=get_types.def_headers,
                          cookies=self.addr_cookie,
                          meta={'shop': shop}, dont_filter=True, callback=self.parse_addr)
        except:
            traceback.print_exc()
            logging.error(traceback.format_exc())

    def parse_addr(self, response):
        """
        获取地址
        :param response:
        :return:
        """
        shop = response.meta['shop']
        try:
            print("---------addr-----------")
            if response.status != 200:
                self.have_re = True
                logging.error("Get addr error , url : %s , status : %d" % (response.url, response.status))
                return

            html = response.text
            s_pre = "address\":\""
            addr_start_index = html.index(s_pre) + len(s_pre)
            tmp = html[addr_start_index:]
            addr_end_index = tmp.index("\"")
            addr = tmp[:addr_end_index]
            shop.addr = addr
            print("%s : %s" % (shop.name, addr))
        except:
            traceback.print_exc()
            logging.error(traceback.format_exc())
        finally:
            logging.debug("保存 : %s " % str(shop))
            shop.save()
