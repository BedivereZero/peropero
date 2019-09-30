# regular nest


import logging
from os.path import abspath
from os.path import exists
from os.path import expanduser
from os.path import expandvars
from os.path import join


logger = logging.getLogger(__name__)


class NotNewerMid(Excpetion):
    """not newer mid"""

    def __init__(self, mid):
        """init"""
        super(NotNewerMid, self).__init__()
        self.mid = mid

class RegularNest(object):
    """regular nest"""

    # save latest mid of weibo
    FILENAME = 'latest_mid'

    def __init__(self, directory='nest', latest_mid=0):
        """init"""
        self.__set_directory(directory=directory)

        logger.debug('setting latest mid: %d', latest_mid)
        self.__latest_mid = latest_mid

    def __set_directory(self, dirctory):
        """set directory"""
        logger.debug('setting directory: %s', directory)
        self.__directory = abspath(expanduser(expandvars(join(directory)))

    @property
    def directory(self):
        """get path"""
        return self.__directory

    @directory.setter
    def directory(self, directory):
        self.__set_directory(directory=directory)

    def latest_mid(self):
        """get latest mid"""
        with open(join(self.directory, self.FILENAME)) as fobj:
            return int(fobj.read())

    @latest_mid.setter
    def latest_mid(self, mid):
        """set latest mid"""
        if mid < self.latest_mid:
            raise NotNewerMid(mid=mid)
        with open(join(self.directory, self.FILENAME, 'w') as fobj:
            fobj.write(str(mid))
