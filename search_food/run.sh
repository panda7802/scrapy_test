#!/bin/bash

#scrapy crawl get_shops
#cp res_dir/shops.xlsx res_dir/shops_bak.xlsx
#scrapy crawl get_shop_info

file_name=tmp.txt
echo "0" > $file_name
while [ 1 = 1 ] ; do
    res=`cat $file_name`
	echo "res = "  $res
    if [ $res = "1" ] ; then
		sleep 1s
		echo "--------------正在爬..."
    elif [ $res = "0" ] ; then
    	python3 get_types.py 
	else
		break
	fi
done
