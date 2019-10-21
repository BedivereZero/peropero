# command line interface

import argparse
import logging

from peropero.creeper.weibo import WeiboCreeper
from peropero import __version__


def main():
    """main"""
    fmt = '%(levelname)-.3s %(asctime)s.%(msecs)03d %(name)s: %(message)s'
    datefmt = '%Y%m%d.%H%M%S'
    formatter = logging.Formatter(fmt, datefmt)
    handler = logging.FileHandler('peropero.log')
    handler.setFormatter(formatter)
    logger = logging.getLogger('peropero')
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    parser = argparse.ArgumentParser(description='peropero')
    parser.add_argument('--version', action='store_true', help='version')

    subparsers = parser.add_subparsers(help='sub-command help')

    parser_weibo = subparsers.add_parser('weibo', help='weibo')
    parser_weibo.set_defaults(creeper=WeiboCreeper)
    parser_weibo.add_argument('name', nargs='+', help='names')

    parser_twitter = subparsers.add_parser('twitter', help='twitter')
    parser_twitter.set_defaults(creeper=lambda s: print(s))
    parser_twitter.add_argument('name', nargs='+', help='names')

    args = parser.parse_args()

    if args.version:
        print(__version__)
        return

    creeper = args.creeper(args.name)
    for pid in creeper.pids:
        print(pid)
