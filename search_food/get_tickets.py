import os
import re
import time
import urllib.request as urllib2

file_full_dir = "/home/pangt/res_dir"
obj_path = file_full_dir + "/res.txt"
if not os.path.exists(obj_path):
    if not os.path.exists(file_full_dir):
        os.makedirs(file_full_dir)

f = open(obj_path, "w+")


def get_ticket_by_city(city_id, city_name, all_res):
    url = 'https://jtjk.xinxife.org/index.php?m=Teams&c=IndexTeams&a=index&now_stage=1&city_id=%d' % city_id
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }

    req = urllib2.Request(url, headers=header)
    res = urllib2.urlopen(req)
    html = str(res.read().decode('utf-8'))

    # srclist = re.findall(
    #     r'<tr class=(.|\n)*?<td>(\d+\.\d+\.\d+\.\d+)</td>(.|\n)*?<td>(\d+)</td>(.|\n)*?<td>(HTTP|HTTPS)</td>', html)
    srclist_ticket = re.findall(
        r'<span class="show_num">(\d+)', html)
    xlist = []
    for item in srclist_ticket:
        xlist.append(int(item))
    # print(xlist)

    srclist_player = re.findall(
        r'<p class="tp_p">表演者：(.*)', html)
    xlist_player = []
    for item in srclist_player:
        s = str(item).split("<")[0]
        xlist_player.append(s)
    # print(xlist_player)

    # all_len = len((xlist_player))
    res = []
    for index, item in enumerate(xlist_player):
        # print("%s : %d" % (item, xlist[index]))
        # res.append({'name': item, "ticket": xlist[index]})
        res.append((item, xlist[index]))
        all_res.append(("%s-%s" % (city_name, item), xlist[index]))

    res.sort(key=lambda x: x[1], reverse=True)

    if city_name == "南京":
        for index, item in enumerate(res):
            f.write("%d.\t%s: %d\n" % (index + 1, item[0], item[1]))
            print("%d.\t%s: %d" % (index + 1, item[0], item[1]))
        else:
            f.write("不关心\n")
            print("不关心")


if __name__ == "__main__":
    city_ids = {"石家庄": 30, "贵阳": 29, "郑州": 28, "长沙": 27, "南京": 26, "泉州": 25,
                "太原": 20, "呼和浩特": 17, "北京": 16, "哈尔滨": 15}

    f.write("%s排名: \n" % (time.strftime("%H:%M:%S")))
    print("%s排名: " % (time.strftime("%H:%M:%S")))
    all_res = []
    for city_name in city_ids:
        f.write("--------%s--------\n" % city_name)
        print("--------%s--------" % city_name)
        get_ticket_by_city(city_ids[city_name], city_name, all_res)

    f.write("----------------放眼全国---------------\n")
    print("----------------放眼全国---------------")
    all_res.sort(key=lambda x: x[1], reverse=True)

    for index, item in enumerate(all_res):
        f.write("%d.\t%s: %d\n" % (index + 1, item[0], item[1]))
        print("%d.\t%s: %d" % (index + 1, item[0], item[1]))

    f.close()
