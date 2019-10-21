# coding: utf-8
# test command line interface

import logging
import sys
import unittest
import unittest.mock

from peropero.cli import main


class TestCli(unittest.TestCase):

    def setUp(self):
        self.logger = logging.getLogger(__name__)
        sys.argv = list()
        patcher = unittest.mock.patch('peropero.cli.WeiboCreeper')
        self.mock_weibo_creeper = patcher.start()
        self.addCleanup(patcher.stop)

    def test_hello(self):
        self.logger.info('hello')
        self.mock_weibo_creeper.pids = []
        sys.argv = [
            'peropero',
            'weibo',
            'username',
        ]
        main()
        self.mock_weibo_creeper.assert_called_once_with('username')


if __name__ == '__main__':
    unittest.main()
