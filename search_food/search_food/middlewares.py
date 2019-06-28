# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import logging
import random
import traceback

from scrapy import signals


class SearchFoodSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SearchFoodDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ProxyMiddleware(object):
    """
    设置Proxy
    """

    # 代理IP
    PROXIES = ['120.26.201.178:8124',
               '61.128.208.94:3128',
               '115.200.211.49:8118',
               '117.121.41.252:3128',
               '123.249.28.188:3128',
               '58.249.55.222:9797',
               '121.15.254.156:888',
               '210.26.64.44:3128',
               '115.171.203.26:9000',
               '60.211.218.78:53281',
               '211.162.70.229:3128',
               '118.187.58.35:53281',
               '183.30.204.113:9999',
               '114.115.200.87:8080',
               '218.64.69.79:8080',
               '111.198.154.116:8888',
               '122.136.212.132:53281',
               '121.15.254.150:8081',
               '121.69.46.177:9000',
               '58.17.125.215:53281',
               '58.240.220.86:53281',
               '119.176.96.134:9999',
               '211.101.154.105:43598',
               '106.12.2.99:3128',
               '116.252.39.176:53281',
               '115.171.85.36:9000',
               '119.122.214.127:9000',
               '119.123.177.119:9000',
               '27.191.234.69:9999',
               '125.46.0.62:53281',
               '124.152.32.140:53281',
               '124.232.133.199:3128',
               '14.20.235.77:34100',
               '59.37.18.243:3128',
               '116.196.90.181:3128',
               '220.180.50.14:53281'
               ]

    def __init__(self, ip):
        self.ip = ip

    @classmethod
    def from_crawler(cls, crawler):
        return cls(ip=crawler.settings.get('PROXIES'))

    def process_request(self, request, spider):
        # ip = "http://" + random.choice(self.PROXIES)
        ip = "http://%s" % self.PROXIES[1]
        if len(ip) < 10:
            logging.debug("本机")
            return
        print("this is request ip:%s , url : %s" % (ip, request.url))
        request.meta['proxy'] = ip
        # return request

    def process_response(self, request, response, spider):
        """
        对返回的response处理
        :param request:
        :param response:
        :param spider:
        :return:
        """
        # 如果返回的response状态不是200，重新生成当前request对象
        if response.status != 200 and response.status != 403 and response.status != 302:
            try:
                print("请求结果 : %d" % response.status)
                ip = "http://" + random.choice(self.PROXIES)
                print("re request ip: %s,url : %s" % (ip, response.url))
                request.meta['proxy'] = ip
                return request
            except:
                traceback.print_exc()
                logging.error(traceback.format_exc())
        return response
