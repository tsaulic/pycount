"""Pycount setup.py script
"""

import codecs
import os

from setuptools import setup


HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    """
    Build an absolute path from *parts* and and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    with codecs.open(os.path.join(HERE, *parts), "rb", "utf-8") as a_file:
        return a_file.read()

setup(
    name='pycount',
    description='Python lines of code counter',
    license='MIT License',
    url='https://github.com/tsaulic/pycount',
    version='0.6.14',
    author='Tihomir Saulic',
    author_email='tihomir.saulic@gmail.com',
    maintainer='Tihomir Saulic',
    maintainer_email='tihomir.saulic@gmail.com',
    long_description=read('README'),
    packages=['pycount'],
    package_data={'pycount': ['LICENSE']},
    scripts=['bin/pycount'],
    package_dir={'pycount': 'pycount'},
    zip_safe=False,
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers'
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ),
    install_requires='binaryornot',
)
