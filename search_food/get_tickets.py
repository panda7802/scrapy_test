import re
import urllib.request as urllib2

if __name__ == "__main__":
    url = 'https://jtjk.xinxife.org/index.php?m=Teams&c=IndexTeams&a=index&now_stage=1&city_id=26'
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
        # print(s)
        # ss = s.encode('raw_unicode_escape')
        # print(ss)
        # print(ss.decode('utf-8'))
        xlist_player.append(s)
    # print(xlist_player)

    # all_len = len((xlist_player))
    res = []
    for index, item in enumerate(xlist_player):
        # print("%s : %d" % (item, xlist[index]))
        # res.append({'name': item, "ticket": xlist[index]})
        res.append((item, xlist[index]))

    res.sort(key=lambda x: x[1], reverse=True)
    # print(res)

    print("目前排名:")
    for index, item in enumerate(res):
        print("%d . %s : %d" % (index + 1, item[0], item[1]))
