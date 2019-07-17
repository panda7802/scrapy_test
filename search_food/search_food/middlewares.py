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
    PROXIES = ['14.20.235.230:9797',
'14.20.235.44:808',
'58.208.235.48:53281',
'211.101.154.105:43598',
'125.123.18.156:9000',
'140.143.48.49:1080',
'112.80.41.86:8888',
'101.231.234.38:8080',
'124.207.82.166:8008',
'111.230.254.195:8118',
'58.246.3.178:53281',
'59.44.247.194:9797',
'60.211.218.78:53281',
'111.224.84.54:9000',
'115.171.202.72:9000',
'119.176.96.134:9999',
'221.4.150.7:8181',
'210.26.49.88:3128',
'58.244.52.235:8080',
'218.241.219.226:9999']

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
