from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='neopets',
    version='0.0.3',
    url='http://neopets.com/',
    author='Ghosts',
    author_email='jakeryh@gmail.com',
    
    keywords='neopets',
    packages=find_packages(),
    install_requires=['BeautifulSoup4', 'HTMLParser']
)
