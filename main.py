#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import requests
import sqlite3
import ConfigParser

from crawler import CrawlerThread

DBNAME = 'peropero.sqlite'

logger = logging.getLogger(__name__)


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
        logger.info('download image {url} failed, {ex}'.format(url=picture['large']['url'], ex=ex))
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
    logger.info('download image {url} succeed'.format(url=picture['large']['url']))

def main():
    """pass"""

    # load weibonames
    path = os.path.abspath('conf/weibonames.conf')
    with open(path) as fp:
        weibonames = [line.strip().decode('utf_8') for line in fp if not line.startswith('#')]

    # create database
    dbpath = os.path.abspath(DBNAME)
    if not os.path.exists(dbpath):
        create_database(dbpath)

    # start crawler thread
    for name in weibonames:
        crawler = CrawlerThread(weiboname=name)
        crawler.start()


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s %(name)s %(levelname)s %(message)s',
        level=logging.INFO,
    )
    main()
