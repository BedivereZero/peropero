#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import os
import re
import requests
import sqlite3
import threading

API = 'http://m.weibo.cn/container/getIndex'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'}
DBNAME = 'peropero.sqlite'



def create_database(path):
    """ create database """
    with open('create.sql') as fobj:
        sql = fobj.read()
    with sqlite3.connect(path) as cnx:
        cnx.executescript(sql)


def download_image(workpath, picture):
    """ download image """
    try:
        res = requests.get(
            url=picture['large']['url'],
            headers=HEADERS,
        )
    except requests.exceptions.RequestException as ex:
        logging.info('download image {url} failed, {ex}'.format(url=picture['large']['url'], ex=ex))
        download = False
    else:
        download = True

    # save image
    if download:
        filename = os.path.basename(picture['large']['url'])
        filepath = os.path.join(workpath, filename)
        with open(filepath, 'wb') as fobj:
            fobj.write(res.content)

    # update download flag
    with sqlite3.connect(DBNAME) as cnx:
        cnx.execute('UPDATE images SET download = ? WHERE imageid = ?',
            (
                download,
                picture['pid'],
            ),
        )
    logging.info('download image {url} succeed'.format(url=picture['large']['url']))

def main():
    """pass"""
    weiboname = u'咸鱼面儿'

    # create database
    dbpath = os.path.abspath(DBNAME)
    if not os.path.exists(dbpath):
        create_database(dbpath)

    # create work directory
    workpath = os.path.abspath(os.path.join('.', weiboname))
    if not os.path.exists(workpath):
        os.mkdir(workpath)
    res = requests.get(url='http://m.weibo.cn/n/{name}'.format(name=weiboname.encode('utf_8')))
    fid = int(re.match(r'^fid%3D(\d+)%26uicode%3D\d+', res.cookies.get('M_WEIBOCN_PARAMS')).group(1))
    userid = int(re.match(r'https://m.weibo.cn/u/(\d+)', res.url).group(1))

    # insert into peropero
    with sqlite3.connect(DBNAME) as cnx:
        cur = cnx.execute('SELECT * FROM users WHERE userid = {id}'.format(id=userid))
        if not cur.fetchall():
            cnx.execute('INSERT INTO users VALUES(?, ?)', (userid, weiboname))

    # get weibo container
    res = requests.get(url=API, params=dict(containerid=fid))
    cont = res.json()
    tabs = cont['data']['tabsInfo']['tabs']
    for tab in cont['data']['tabsInfo']['tabs']:
        if tab['tab_type'] == 'weibo':
            cid = tab.get('containerid')

    # get page
    page = 1
    res = requests.get(
        url=API,
        headers=HEADERS,
        params=dict(containerid=cid),
    )
    cont = res.json()
    while cont.get('ok') == 1:
        logging.info('parsing page {num:2d}'.format(num=page))
        data = cont.get('data')
        if data.get('cards'):
            for card in data.get('cards'):
                if card['card_type'] == 11:
                    # what's meaning of card_type = 11
                    return 302
                if 'retweeted_status' in card['mblog']:
                    # skip retweet
                    continue
                if 'pics' not in card['mblog']:
                    continue
                for pic in card['mblog']['pics']:
                    # insert image info into database if image has not been seen
                    with sqlite3.connect(DBNAME) as cnx:
                        cur = cnx.execute('SELECT imageid FROM images WHERE imageid = ?', (pic['pid'],))
                        record = cur.fetchone()
                        if record:
                            logging.info('image {pid} has been seen'.format(pid=pic['pid']))
                        else:
                            logging.info('adding image {pid}'.format(pid=pic['pid']))
                            cnx.execute(
                                'INSERT INTO images(imageid, userid, url) VALUES(?, ?, ?)',
                                (
                                    pic['pid'],
                                    userid,
                                    pic['large']['url'],
                                ),
                            )
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

if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s %(levelname)s %(message)s',
        level=logging.INFO,
    )
    main()
