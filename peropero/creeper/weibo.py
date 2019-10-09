# weibo creeper

import logging
import os
import random
import re
import time

import requests

from peropero.creeper.base import BaseCreeper

logger = logging.getLogger(__name__)
logger.setLevel(logging.NOTSET)


class WeiboCreeper(BaseCreeper):
    """creeper on weibo"""

    API = 'https://m.weibo.cn/container/getIndex'
    API_NAME = 'https://m.weibo.cn/n'
    API_USERID = 'https://m.weibo.cn/u'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
    }

    def __init__(self, name=None, min_mid=0):
        """init"""
        super(self.__class__, self).__init__()
        self.__name = name
        self.__userid = None
        self.__fid = None
        self.__containerid = None
        self.__min_mid = min_mid

    @property
    def name(self):
        """"name"""
        return self.__name

    @name.setter
    def name(self, value):
        """name"""
        self.__name = value

    @property
    def min_mid(self):
        """minimum mid"""
        return self.__min_mid

    @min_mid.setter
    def min_mid(self, value):
        """minimum mid"""
        self.__min_mid = value

    @property
    def userid(self):
        """userid"""
        if self.__userid is None:
            rsp = requests.get(url=os.path.join(self.API_NAME.encode(self.ENCODING), self.name.encode(self.ENCODING)))
            self.__userid = int(os.path.basename(rsp.url))
            logger.info('userid: %s', self.__userid)
        return self.__userid

    @property
    def fid(self):
        """fid"""
        if self.__fid is None:
            rsp = requests.get(url=os.path.join(self.API_USERID.encode(self.ENCODING), str(self.userid).encode(self.ENCODING)))
            m_weibocn_params = rsp.cookies.get('M_WEIBOCN_PARAMS')
            mobj = re.match(r'^fid%3D(\d+)%26uicode%3D\d+', m_weibocn_params)
            self.__fid = int(mobj.group(1))
            logger.info('fid: %s', self.__fid)
        return self.__fid

    @property
    def containerid(self):
        """containerid"""
        if self.__containerid is None:
            rsp = requests.get(url=self.API.encode(self.ENCODING), params=dict(containerid=self.fid))
            for tab in rsp.json()['data']['tabsInfo']['tabs']:
                if tab['tab_type'] == 'weibo':
                    self.__containerid = int(tab['containerid'])
                    logger.info('containerid: %s', self.__containerid)
                    break
        return self.__containerid

    @property
    def pages(self):
        """pages"""
        loop = 3
        page = 0
        while loop:
            rsp = requests.get(self.API.encode(self.ENCODING), headers=self.HEADERS, params=dict(containerid=self.containerid, page=page))
            if rsp.status_code in range(200, 300):
                content = rsp.json()
                if content.get('ok'):
                    yield content['data']
                    time.sleep(random.randint(4, 16))
                    page = page + 1
                    loop = 3
                else:
                    loop = 0
            else:
                loop = loop - 1
                time.sleep(random.randint(60, 300))

    @property
    def cards(self):
        """cards"""
        for page in self.pages:
            logger.debug('page: %r', page)
            for card in page['cards']:
                yield card

    @property
    def pids(self):
        """pids"""
        for card in self.cards:
            logger.debug('card: %r', card)
            if card['card_type'] == 11:
                logger.debug('skip for card_type is 11')
                continue
            if 'retweeted_status' in card['mblog']:
                logger.debug('skip for retweeted_status')
                continue
            if not card['mblog']['pic_num']:
                logger.debug('skip for no picture')
                continue
            logger.debug('card itemid: %r', card['itemid'])
            for pic in card['mblog']['pics']:
                yield pic['pid']
