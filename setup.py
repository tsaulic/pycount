try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'A simple python LOC count tool',
    'author': 'Tihomir Saulic',
    'url': 'https://github.com/tsaulic',
    'download_url': 'https://github.com/tsaulic',
    'author_email': 'tihomir[DOT]saulic[AT]gmail[DOT]com',
    'version': '0.1',
    'install_requires': ['nose', 'binaryornot'],
    'packages': ['pycount'],
    'scripts': [],
    'name': 'pycount'
}

setup(**config)
