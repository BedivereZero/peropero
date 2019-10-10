# command line interface

from argparse import ArgumentParser
from logging import DEBUG
from logging import Formatter
from logging import INFO
from logging import StreamHandler
from logging import getLogger

from peropero.creeper.weibo import WeiboCreeper


ENCODING = 'utf_8'
FORMAT = '%(levelname)-.3s %(asctime)s.%(msecs)03d %(name)s: %(message)s'
DATEFORMAT = '%Y%m%d.%H%M%S'


formatter = Formatter(FORMAT, DATEFORMAT)
handler = StreamHandler()
handler.setFormatter(formatter)
logger = getLogger(__name__)
logger.addHandler(handler)


def main():
    """main"""

    parser = ArgumentParser(description='peropero')
    parser.add_argument('-d', '--debug', help='debug', action='store_true')
    parser.add_argument('-n', '--name', help='name', type=lambda s: unicode(s, ENCODING))
    args = parser.parse_args()

    logger.setLevel(DEBUG if args.debug else INFO)

    logger.debug('name: %s', args.name)
