#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import re
import requests
import sqlite3
import threading

DBNAME = 'peropero.sqlite'


logger = logging.getLogger(__name__)

# logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s %(message)s', level=logging.DEBUG)


class CrawlerThread(threading.Thread):
    """ crawler thread """

    API = 'https://m.weibo.cn/container/getIndex'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
    }

    def __init__(self, weiboname=None):
        """ init """
        super(self.__class__, self).__init__()

        self.weiboname = weiboname
        self.userid = None

    def run(self):
        """ run """
        logger.info('getting userid from weiboname')
        rsp = requests.get(url='https://m.weibo.cn/n/{}'.format(self.weiboname.encode('utf_8')))
        fid = int(re.match(r'^fid%3D(\d+)%26uicode%3D\d+', rsp.cookies.get('M_WEIBOCN_PARAMS')).group(1))
        self.userid = int(re.match(r'https://m.weibo.cn/u/(\d+)', rsp.url).group(1))

        logger.info('adding user information')
        with sqlite3.connect(DBNAME) as cnx:
            cur = cnx.execute('SELECT `name` FROM users WHERE `userid` = ?', (self.userid,))
            row = cur.fetchone()
            if not row:
                logger.info('create user record {}:{}'.format(self.weiboname.encode('utf_8'), self.userid))
                cnx.execute('INSERT INTO users VALUES(?, ?)', (self.userid, self.weiboname))

        logger.info('getting weibo container')
        rsp = requests.get(url=self.API, params=dict(containerid=fid))
        dat = rsp.json()
        for tab in dat['data']['tabsInfo']['tabs']:
            if tab['tab_type'] == 'weibo':
                cid = int(tab.get('containerid'))
                break

        logger.info('getting pages')
        page = 1
        rsp = requests.get(url=self.API, headers=self.HEADERS, params=dict(containerid=cid))
        dat = rsp.json()
        while dat.get('ok'):
            for card in dat['data']['cards']:
                import json
                if card['card_type'] is 11:
                    logger.debug('skip: card_type = 11')
                    continue
                if 'retweeted_status' in card['mblog']:
                    logger.debug('skip: retweeted')
                for pic in card['mblog'].get('pics', list()):
                    with sqlite3.connect(DBNAME) as cnx:
                        cur = cnx.execute('SELECT imageid FROM images WHERE imageid = ?', (pic['pid'],))
                        if cur.fetchone():
                            logger.debug('image {pid} has been seen'.format(pid=pic['pid']))
                        else:
                            logger.info('adding image {pid}'.format(pid=pic['pid']))
                            cur.execute('INSERT INTO images(imageid, userid, url) VALUES(?, ?, ?)', (pic['pid'], self.userid, pic['large']['url']))
            page += 1
            rsp = requests.get(url=self.API, headers=self.HEADERS, params=dict(containerid=cid, page=page))
            dat = rsp.json()
