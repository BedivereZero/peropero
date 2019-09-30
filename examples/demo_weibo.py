#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os

import requests

from peropero.creeper.weibo import WeiboCreeper


logger = logging.getLogger(__name__)
logging.captureWarnings(True)


def output_to_file():
    """test property"""
    creeper = WeiboCreeper()
    creeper.name = u'吃糖的豚豚'
    with open(str(creeper.userid), 'w') as handler:
        for pid in creeper.pids:
            handler.write(pid)
            handler.write(os.linesep)


def main():
    """main"""
    formatter = logging.Formatter(
        '%(levelname)-.4s %(asctime)s.%(msecs)03d %(name)s: %(message)s',
        '%Y-%m-%d %H:%M:%S')
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    output_to_file()


if __name__ == '__main__':
    main()
