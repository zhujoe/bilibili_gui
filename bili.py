# -*- coding: utf-8 -*-
# -----------------------------
# 作者：朱旭晖
# 时间：2017.8.17
# 从哔哩哔哩上获取推荐的视频
# -----------------------------
import requests

def get_bili():
    url = 'http://bangumi.bilibili.com/jsonp/timeline_v2?callback=jQuery17207487528945785016_1444194560857&_=1444194615330'
    data = requests.get(url)
    data_json = data.json()
    # count = data_json['count']
    list = []
    num = 0
    for item in data_json['list']:

        listitem = {}
        listitem['name'] = item['title'][0:10]
        listitem['url'] = 'http://www.bilibili.com' + item['url']

        listitem['img'] = item['cover']
        fname = './img/' + str(num) + '.jpg'
        pic = requests.get(listitem['img'])
        fp = open(fname, 'wb')
        fp.write(pic.content)
        fp.close()

        listitem['hot'] = item['favorites']
        list.append(listitem)
        num += 1

        if num == 50:
            return list
    return list


