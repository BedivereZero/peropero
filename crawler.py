#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import threading
import logging

from utils.database import DBNAME


logger = logging.getLogger(__name__)

logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s %(message)s', level=logging.DEBUG)


class Crawler(threading.Thread):
    """ crawler thread """

    API = 'http://m.weibo.cn/container/getIndex'
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
        logger.debug('checking user directory')
        user_dir = os.path.abspath(self.weiboname)
        if not os.path.exists(user_directory):
            logger.debug('create user directory {path}'.format(path=user_dir))
            os.mkdir(user_dir)

        logger.debug('getting userid from weiboname')
        rsp = requests.get(url='http:/m.weibo.cn/n/{}'.format(weiboname.encode('utf_8')))
        fid = int(re.match(r'^fid%3D(\d+)%26uicode%3D\d+', rsp.cookies.get('M_WEIBOCN_PARAMS')).group(1))
        self.userid = int(re.match(r'https://m.weibo.cn/u/(\d+)', rsp.url).group(1))

        logger.debug('checking user information')
        with sqlite3.connect(DBNAME) as cnx:
            cur = cnx.execute('SELECT `name` FROM users WHERE `userid` = ?', (self.userid,))
            row = cur.fetchone()
            if not row:
                logger.debug('create user record {}:{}'.format(self.weiboname, self.userid))
                cnx.execute('INSERT INTO users VALUES(?, ?)', (self.userid, self.weiboname)

        logger.debug('getting weibo container')
        rsp = requests.get(url=self.API, params=dict(containerid=fid))
        dat = rsp.json()
        for tab in dat['data']['tabsInfo']['tabs']:
            if tab['tab_type'] == 'weibo':
                cid = int(tab.get('containerid'))
                break

        logger.debug('getting pages')
        page = 1
        rsp = requests.get(url=self.API, headers=self.HEADERS, params=dict(containerid=cid))
        dat = rsp.json()
        while dat.get('ok'):
            pass
            page += 1
            rsp = requests.get(url=self.API, headers=self.HEADERS, params=dict(containerid=cid, page=page))
            dat = rsp.json()
