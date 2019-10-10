# setup

from setuptools import find_packages
from setuptools import setup


with open('requirements.txt') as f:
    INSTALL_REQUIRES = f.readlines()

with open('test-requirements.txt') as f:
    TEST_REQUIRES = f.readlines()


setup(
    name='peropero',
    version='0.0.1',
    description='Crawler for weibo',
    author_email='BedivereZero@gmail.com',
    author='BedivereZero',
    url='https://github.com/BedivereZero/peropero',
    install_requires=INSTALL_REQUIRES,
    packages=find_packages(),
    tests_require=TEST_REQUIRES,
    entry_points={
        'console_scripts': [
            'peropero = peropero.cli:main',
        ],
    },
    zip_safe=True,
)
