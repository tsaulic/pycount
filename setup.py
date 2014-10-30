try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'A simple python LOC count tool',
    'author': 'Tihomir Saulic',
    'url': 'http://github.com/tsaulic/pycount',
    'download_url': 'http://github.com/tsaulic/pycount',
    'author_email': 'tihomir[DOT]saulic[AT]gmail[DOT]com',
    'version': '0.4.4',
    'install_requires': ['binaryornot'],
    'packages': ['pycount'],
    'scripts': ['bin/pycount'],
    'name': 'pycount'
}

setup(**config)
