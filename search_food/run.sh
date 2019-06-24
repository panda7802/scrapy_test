#!/bin/bash

scrapy crawl get_shops
cp res_dir/shops.xlsx res_dir/shops_bak.xlsx
scrapy crawl get_shop_info
