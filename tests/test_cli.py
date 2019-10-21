# coding: utf-8
# test command line interface

import logging
import sys

from unittest import TestCase
from unittest import mock


class TestCli(TestCase):

    def setUp(self):
        self.logger = logging.getLogger(__name__)
        sys.argv = list()

    def test_hello(self):
        self.logger.info('hello')
