#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" downloader thread & manager """

import json
import threading
import sqlite3
import Queue

DBNAME = 'peropero.sqlite'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
}


class DownloadTask(object):
    """ download task """

    def __init__(self, imageid=None, url=None, done=False):
        """ init """
        self.imageid = imageid
        self.url = url
        self.done = done

    def done(self):
        self.done = True


class DownloadThread(threading.Thread):
    """ download thread """

    def __init__(self, tasks=None):
        """ init """
        super(DownloadThread, self).__init__()
        self.tasks = tasks or Queue.Queue()

    def run(self):
        """ run """
        try:
            task = self.tasks.get(block=True, timeout=3)
        except Queue.Empty:
            logger.debug('queue is empty, exit')
            return
        try:
            rsp = requests.get( url=task.url, headers=HEADERS)
        except requests.exceptions.RequestException as ex:
            pass



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

        self.load_config()

    def run(self):
        """ run """
        with sqlite3.connect(DBNAME) as cnx:
            for imageid, url in cnx.execute('SELECT `imageid`, `url` FROM images WHERE download = ?', False):
                self.tasks.put(DownloadTask(imageid=imageid, url=url))
        while not self.tasks.empty():
            self.maintain_download_thread()
            time.sleep(1)

    def maintain_download_thread(self):
        """ maintain download thread """

    def load_config(self):
        """ load config """
        global_cfg = json.load(fp=open(CONF_PATH))
        download_cfg = global_cfg.get('downloader')
        self.data_dir = download_cfg.get('data-dir')
        self.speed_limit_down = download_cfg.get('speed-limit-down')
        self.speed_limit_down_enabled = download_cfg.get('speed-limit-down-enabled')
        self.thread_limit = download_cfg.get('thread-limit')
