#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" downloader thread & manager """

import Queue
import json
import logging
import os
import requests
import sqlite3
import threading
import time

DBNAME = 'peropero.sqlite'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
}
CONF_PATH = 'conf/config.json'

logger = logging.getLogger(__name__)


class DownloadTask(object):
    """ download task """

    def __init__(self, imageid=None, userid=None, url=None, done=False):
        """ init """
        self.imageid = imageid
        self.userid = userid
        self.url = url
        self.done = done

    def done(self):
        self.done = True


class DownloadThread(threading.Thread):
    """ download thread """

    def __init__(self, tasks=None, data_dir=None):
        """ init """
        super(DownloadThread, self).__init__()
        self.tasks = tasks or Queue.Queue()
        self.data_dir = data_dir or os.path.abspath(os.curdir)

    def run(self):
        """ run """
        while True:
            try:
                task = self.tasks.get(block=True, timeout=3)
            except Queue.Empty:
                logger.debug('queue is empty, exit')
                return
            try:
                rsp = requests.get(url=task.url, headers=HEADERS)
            except requests.exceptions.RequestException as ex:
                logger.warning('download image: {} failed, {}'.format(task.url, ex))
                return

            filepath = os.path.join(self.data_dir, str(task.userid), os.path.basename(task.url))
            if not os.path.exists(os.path.dirname(filepath)):
                logger.info('creating directory: {}'.format(os.path.dirname(filepath)))
                os.makedirs(os.path.dirname(filepath))
            logger.info('saving file: {}'.format(filepath))
            with open(filepath, 'w') as fp:
                fp.write(rsp.content)

            with sqlite3.connect(DBNAME) as cnx:
                cnx.execute('UPDATE images SET `download` = ? WHERE `imageid` = ?', (True, task.imageid))


class DownloadManager(threading.Thread):
    """ download manager """

    def __init__(self):
        """ init """
        super(DownloadManager, self).__init__()

        self.tasks = Queue.Queue()

        # default options
        self.data_dir = 'peropero'
        self.speed_limit_down = 100
        self.speed_limit_down_enabled = False
        self.thread_limit = 3

        # downloader threads
        self.downloader_threads = list()

        self.load_config()

    def run(self):
        """ run """
        with sqlite3.connect(DBNAME) as cnx:
            for imageid, userid, url in cnx.execute('SELECT `imageid`, `userid`, `url` FROM images WHERE download = ?', (False,)):
                self.tasks.put(DownloadTask(imageid=imageid, userid=userid, url=url))
        while not self.tasks.empty():
            self.maintain_download_thread()
            time.sleep(1)

    def maintain_download_thread(self):
        """ maintain download thread """
        self.downloader_threads = [thread for thread in self.downloader_threads if thread.is_alive()]
        for index in xrange(len(self.downloader_threads), min(self.thread_limit, self.tasks.qsize())):
            thread = DownloadThread(tasks=self.tasks, data_dir=self.data_dir)
            logger.debug('adding new download thread {}'.format(thread.name))
            thread.start()
            self.downloader_threads.append(thread)

    def load_config(self):
        """ load config """
        global_cfg = json.load(fp=open(CONF_PATH))
        download_cfg = global_cfg.get('downloader')
        self.data_dir = download_cfg.get('data-dir')
        self.speed_limit_down = download_cfg.get('speed-limit-down')
        self.speed_limit_down_enabled = download_cfg.get('speed-limit-down-enabled')
        self.thread_limit = download_cfg.get('thread-limit')
