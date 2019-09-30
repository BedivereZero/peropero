# -*- coding: utf -*-
# test weibo


import os
from unittest import TestCase
from unittest import skip

import mock

from peropero.creeper.weibo import WeiboCreeper


class TestWeiboCreeper(TestCase):
    """test peropero.creeper.weibo.WeiboCreeper"""

    def setUp(self):
        """setup"""
        super(TestWeiboCreeper, self).setUp()
        self.name = u'吃糖的豚豚'
        self.userid = 6603400985
        self.fid = 1005056603400985
        self.containerid = 1076036603400985
        patcher = mock.patch(target='peropero.creeper.weibo.requests.get')
        self.mock_get = patcher.start()
        self.addCleanup(patcher.stop)


class TestWeiboCreeperInit(TestWeiboCreeper):
    """test peropero.creeper.weibo.WeiboCreeper.__init__"""

    def test_without_params(self):
        """test without params"""
        creeper = WeiboCreeper()
        self.assertIsNone(creeper._WeiboCreeper__name)
        self.assertIsNone(creeper._WeiboCreeper__userid)
        self.assertEqual(creeper._WeiboCreeper__min_mid, 0)

    def test_given_name(self):
        """test given name"""
        name = 'hello',
        creeper = WeiboCreeper(name)
        self.assertEqual(creeper._WeiboCreeper__name, name)

    def test_given_min_mid(self):
        min_mid = 114514
        creeper = WeiboCreeper(min_mid=min_mid)
        self.assertEqual(creeper._WeiboCreeper__min_mid, min_mid)

    def test_given_all_params(self):
        """test given all params"""
        name = 'hello'
        min_mid = 114514
        creeper = WeiboCreeper(name, min_mid)
        self.assertEqual(creeper._WeiboCreeper__name, name)
        self.assertEqual(creeper._WeiboCreeper__min_mid, min_mid)


class TestWeiboCreeperName(TestWeiboCreeper):
    """test peropero.creeper.weibo.WeiboCreeper.name"""

    def test_get_init_notset(self):
        """test get init notset"""
        creeper = WeiboCreeper()
        self.assertIsNone(creeper.name)

    def test_get_init_set(self):
        """test get init set"""
        name = 'hello'
        creeper = WeiboCreeper(name)
        self.assertEqual(creeper.name, name)


    def test_set_init_notset(self):
        """test set init notset"""
        name = 'hello'
        creeper = WeiboCreeper()
        creeper.name = name
        self.assertEqual(creeper.name, name)

    def test_set_init_set(self):
        name_old = 'hello'
        name_new = 'world'
        creeper = WeiboCreeper(name_old)
        creeper.name = name_new
        self.assertEqual(creeper.name, name_new)


class TestWeiboCreeperMinMid(TestWeiboCreeper):
    """test peropero.creeper.weibo.WeiboCreeper.min_mid"""

    def test_get_init_notset(self):
        """test get init notset"""
        creeper = WeiboCreeper()
        self.assertEqual(creeper.min_mid, 0)

    def test_get_init_set(self):
        """test get init set"""
        min_mid = 114
        creeper = WeiboCreeper(min_mid=min_mid)
        self.assertEqual(creeper.min_mid, min_mid)


    def test_set_init_notset(self):
        """test set init notset"""
        min_mid = 114
        creeper = WeiboCreeper()
        creeper.min_mid = min_mid
        self.assertEqual(creeper.min_mid, min_mid)

    def test_set_init_set(self):
        min_mid_old = 114
        min_mid_new = 514
        creeper = WeiboCreeper(min_mid=min_mid_old)
        creeper.min_mid = min_mid_new
        self.assertEqual(creeper.min_mid, min_mid_new)


class TestWeiboCreeperUserid(TestWeiboCreeper):
    """test peropero.creeper.weibo.WeiboCreeper.userid"""

    def setUp(self):
        """setup"""
        super(self.__class__, self).setUp()
        patcher = mock.patch('peropero.creeper.weibo.requests.get')
        self.mock_get = patcher.start()
        self.addCleanup(patcher.stop)
        self.url = os.path.join(WeiboCreeper.API_USERID, str(self.userid))
        self.creeper = WeiboCreeper(name=self.name)

    def test_userid_unknown(self):
        """test userid is unknown"""
        self.creeper._WeiboCreeper__userid = None
        self.mock_get.return_value.url = self.url
        userid = self.creeper.userid
        self.assertEqual(userid, self.userid)
        self.mock_get.assert_called_once_with(
            url=os.path.join(
                WeiboCreeper.API_NAME,
                self.name.encode(WeiboCreeper.ENCODING),
            ),
        )

    def test_userid_known(self):
        """test userid is known"""
        self.creeper._WeiboCreeper__userid = self.userid
        userid = self.creeper.userid
        self.assertEqual(userid, self.userid)
        self.mock_get.assert_not_called()


class TestWeiboCreeperFid(TestWeiboCreeper):
    """test peropero.creeper.weibo.WeiboCreeper.fid"""

    def setUp(self):
        """setup"""
        super(TestWeiboCreeperFid, self).setUp()
        patcher = mock.patch(target='peropero.creeper.weibo.WeiboCreeper.userid')
        self.mock_userid = patcher.start()
        self.addCleanup(patcher.stop)
        self.m_weibocn_params = 'fid%%3D%s%%26uicode%%3D10000011' % self.fid
        self.creeper = WeiboCreeper()

    def test_fid_unknown(self):
        """test fid is unknown"""
        self.creeper._WeiboCreeper__fid = None
        self.mock_get.return_value.cookies = dict(
            M_WEIBOCN_PARAMS=self.m_weibocn_params,
        )
        fid = self.creeper.fid
        self.assertEqual(fid, self.fid)
        self.mock_get.assert_called_once_with(
            url=os.path.join(
                WeiboCreeper.API_USERID,
                str(self.mock_userid),
            ),
        )

    def test_fid_known(self):
        """test fid is known"""
        self.creeper._WeiboCreeper__fid = self.fid
        fid = self.creeper.fid
        self.assertEqual(fid, self.fid)
        self.mock_get.assert_not_called()


class TestWeiboCreeperContainerid(TestWeiboCreeper):
    """ test peropero.creeper.weibo.WeiboCreeper.containerid"""

    def setUp(self):
        """setup"""
        super(TestWeiboCreeperContainerid, self).setUp()
        patcher = mock.patch(target='peropero.creeper.weibo.WeiboCreeper.fid')
        self.mock_fid = patcher.start()
        self.addCleanup(patcher.stop)
        self.json = {
            'data': {
                'tabsInfo': {
                    'tabs': [
                        {
                            'tab_type': 'weibo',
                            'containerid': self.containerid,
                        },
                    ],
                },
            },
        }
        self.creeper = WeiboCreeper()

    def test_containerid_unknown(self):
        """test containerid is unknown"""
        self.creeper._WeiboCreeper__containerid = None
        self.mock_get.return_value.json.return_value = self.json
        containerid = self.creeper.containerid
        self.assertEqual(containerid, self.containerid)
        self.mock_get.assert_called_once_with(
            url=WeiboCreeper.API,
            params=dict(containerid=self.creeper.fid),
        )

    def test_containerid_known(self):
        """test containerid is known"""
        self.creeper._WeiboCreeper__containerid = self.containerid
        containerid = self.creeper.containerid
        self.assertEqual(containerid, self.containerid)
        self.mock_get.assert_not_called()


@skip('work in progress')
class TestWiboCreeperPages(TestWeiboCreeper):
    """test peropero.creeper.weibo.WeiboCreeper.pages"""


@skip('work in progress')
class TestWeiboCreeperCards(TestWeiboCreeper):
    """test peropero.creeper.weibo.WeiboCreeper.cards"""

    def setUp(self):
        """setup"""
        self.creeper = WeiboCreeper()

    def test_success(self):
        """test success"""
        self.creeper.pages = (dict(cards=(page * 10 + card for card in range(4))) for page in range(4))
        cards = list(self.creeper.cards)
        self.assertListEqual(cards, list(range(16)))
