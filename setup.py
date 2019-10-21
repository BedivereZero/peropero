# setup

from setuptools import find_packages
from setuptools import setup

from peropero import __version__


with open('requirements.txt') as f:
    INSTALL_REQUIRES = f.readlines()

setup(
    name='peropero',
    version=__version__,
    description='Crawler for weibo',
    author_email='BedivereZero@gmail.com',
    author='BedivereZero',
    url='https://github.com/BedivereZero/peropero',
    install_requires=INSTALL_REQUIRES,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'peropero = peropero.cli:main',
        ],
    },
    zip_safe=True,
)
