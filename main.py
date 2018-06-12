#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import re
import requests
import sqlite3

API = 'http://m.weibo.cn/container/getIndex'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'}


def create_database(path):
    """ create database """
    with open('create.sql') as fobj:
        sql = fobj.read()
    with sqlite3.connect(path) as cnx:
        cnx.executescript(sql)

def main():
    """pass"""
    weiboname = '咸鱼面儿'
    # create database
    dbpath = os.path.abspath('peropero.sqlite')
    if not os.path.exists(dbpath):
        create_database(dbpath)
    workpath = os.path.abspath(os.path.join('.', weiboname))
    if not os.path.exists(workpath):
        os.mkdir(workpath)
    res = requests.get(url='http://m.weibo.cn/n/{name}'.format(name=weiboname))
    cookie = res.headers.get('Set-Cookie')
    fid = int(re.match(r'^fid%3D(\d+)%26uicode%3D\d+', res.cookies.get('M_WEIBOCN_PARAMS')).group(1))
    userid = int(re.match(r'https://m.weibo.cn/u/(\d+)', res.url).group(1))
    # insert into peropero
    print(fid)
    return 0
    res = requests.get(url=API, params=dict(containerid=fid))
    cont = res.json()
    tabs = cont['data']['tabsInfo']['tabs']
    for tab in cont['data']['tabsInfo']['tabs']:
        if tab['tab_type'] == 'weibo':
            cid = tab.get('containerid')
    page = 1
    res = requests.get(
        url=API,
        headers=HEADERS,
        params=dict(containerid=cid),
    )
    cont = res.json()
    result = dict()
    result.update(cont)
    while cont.get('ok') == 1:
        data = cont.get('data')
        if data.get('cards'):
            for card in data.get('cards'):
                if card['card_type'] == 11:
                    # what's meaning of card_type = 11
                    return 302
                if 'retweeted_status' in card['mblog']:
                    # skip retweet
                    continue
                # print(card['mblog'].get('mid'), 'pics' in card['mblog'])
                if 'pics' not in card['mblog']:
                    continue
                print('parsering {text}'.format(text=card['mblog'].get('raw_text')))
                for pic in card['mblog']['pics']:
                    res = requests.get(
                        url=pic['large']['url'],
                        headers=HEADERS,
                    )
                    filename = os.path.basename(pic['large']['url'])
                    filepath = os.path.join(workpath, filename.encode('utf-8'))
                    with open(filepath, 'wb') as fobj:
                        fobj.write(res.content)

        else:
            break
        page += 1
        res = requests.get(
            url=API,
            headers=HEADERS,
            params=dict(
                containerid=cid,
                page=page,
            ),
        )
        cont = res.json()
        result.update(cont)
    json.dump(
        obj=result,
        fp=open('temp.json', 'w'),
        indent=2,
        sort_keys=True,
    )

if __name__ == '__main__':
    main()
