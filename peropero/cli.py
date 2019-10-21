# command line interface

from argparse import ArgumentParser
from logging import DEBUG
from logging import Formatter
from logging import INFO
from logging import StreamHandler
from logging import getLogger

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
    parser.add_argument('site', help='site')
    parser.add_argument('name', help='name')
    args = parser.parse_args()
