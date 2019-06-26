# -*- coding: utf-8 -*-

# Scrapy settings for search_food project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import logging

BOT_NAME = 'search_food'

SPIDER_MODULES = ['search_food.spiders']
NEWSPIDER_MODULE = 'search_food.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'search_food (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False
COOKIES_ENABLED = True
ROBOTSTXT_OBEY = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'search_food.middlewares.SearchFoodSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'search_food.middlewares.SearchFoodDownloaderMiddleware': 543,
    'search_food.middlewares.ProxyMiddleware': 543,  # IP代理
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 'search_food.pipelines.SearchFoodPipeline': 300,
    # 'search_food.pipelines.ShopPipeline': 300,
    'search_food.pipelines_db.DbPipeline': 300,

}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


# LOG_FILE = "dzdp.log"
# LOG_LEVEL = "DEBUG"

# USER_AGENT = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0"

HTTPERROR_ALLOWED_CODES = [304, 403]
# HTTPERROR_ALLOWED_CODES = list(range(0, 999))
# print(HTTPERROR_ALLOWED_CODES)

logger = logging.getLogger()  # 不加名称设置root logger
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s: - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

# 使用FileHandler输出到文件
fh = logging.FileHandler('log.txt')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)

# 使用StreamHandler输出到屏幕
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)

# 添加两个Handler
logger.addHandler(ch)
logger.addHandler(fh)

# 代理IP
PROXIES = ['125.73.220.18:49128',
           '124.202.166.171:82',
           '60.217.158.163:8060',
           '218.60.8.83:3129',
           '183.3.221.10:3128',
           '210.34.24.103:3128',
           '182.92.105.136:3128',
           '111.13.134.22:80',
           '115.239.248.181:3128',
           '117.127.0.202:8080',
           '39.137.77.66:80',
           '119.41.236.180:8010',
           '39.137.77.68:8080',
           '114.55.92.9:9999',
           '101.37.118.54:8888',
           '101.251.216.103:8080',
           '39.137.107.98:80',
           '111.77.101.152:8118',
           '114.115.214.122:8080',
           '114.115.200.87:8080',
           '119.180.143.207:8060',
           '47.94.213.22:8888',
           '112.84.178.21:8888',
           '120.79.161.204:80',
           '202.112.51.51:8082',
           '120.234.63.196:3128',
           '120.210.219.74:8080',
           '124.250.26.129:8080',
           '218.60.8.98:3129',
           '39.135.24.11:80',
           '175.10.24.82:3128',
           '101.231.104.82:80',
           '210.22.5.117:3128',
           '27.208.91.251:8060',
           '106.2.238.2:3128',
           '117.127.16.208:8080',
           '119.122.214.127:9000',
           '112.246.235.69:8060',
           '221.4.172.162:3128',
           '120.79.147.254:9000',
           '101.16.240.179:8080',
           '117.191.11.74:80'
           ]
