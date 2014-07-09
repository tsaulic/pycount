#!/usr/bin/env python
#-*- coding: utf-8 -*-


"""
   pycount.pycount
   ~~~~~~~~~~~~~~~

   Core pyCount file

   :copyright: (c) Tihomir Saulic
   :license: GPL 2.0, see LICENSE for more details
"""


from __future__ import print_function

import hashlib
import os
import sys

try:
    from binaryornot.check import is_binary
except ImportError as an_error:
    sys.exit(an_error)


class Counter(object):
    """Main clas for counting the lines of code
    """
    def __init__(self, root=None, patterns=None):
        if root is None:
            self.root = os.getcwd()
        else:
            self.root = root

        if patterns is None:
            self.patterns = {
                '.htm': 'HTML',
                '.html': 'HTML',
                '.py': 'PYTHON'
            }
        else:
            self.patterns = patterns

    def chunk_reader(self, fobj, chunk_size=1024):
        """Generator that reads a file in chunks of bytes
        """
        while True:
            chunk = fobj.read(chunk_size)
            if not chunk:
                return
            yield chunk

    def unique(self, a_file, hashing=hashlib.sha1, unique=False):
        """Filters out duplicate files
        """
        hashobj = hashing()
        for chunk in self.chunk_reader(open(a_file, "rb")):
            hashobj.update(chunk)
        file_id = (hashobj.digest(), os.path.getsize(a_file))
        duplicate = self.hashes.get(file_id, None)
        if duplicate:
            #print("Duplicate found: %s and %s" % (a_file, duplicate))
            pass
        else:
            self.hashes[file_id] = a_file
            unique = True
        return unique

    def discover(self):
        """Discovers all files and performs basic filters to include only
           valid files in the list
        """
        self.files = []
        self.hashes = {}
        for path, subpath, files in os.walk(self.root):
            if '/.' not in path:
                for a_file in files:
                    if not a_file.startswith('.'):
                        a_file = os.path.join(path, a_file)
                        non_empty = os.stat(a_file).st_size > 0
                        if non_empty and self.unique(a_file) and not \
                                is_binary(a_file):
                            self.files.append(a_file)

    def count(self):
        """Counts lines of code for valid files in self.patterns
           Generates and prints a decent looking breakdown report for lines
           of code for all existent languages under our path
        """
        results = {}
        for path in self.files:
            ext = os.path.splitext(path)[1]
            count = 0
            if ext in self.patterns.keys():
                with open(path, "r") as a_file:
                    for line in a_file:
                        if line.strip():
                            count += 1
                try:
                    results[self.patterns[ext]] = results[self.patterns[ext]] \
                        + count
                except KeyError:
                    results[self.patterns[ext]] = 0
        print('Language          LOC')
        print('-' * 21)
        for key, value in results.items():
            print('{0:9}     {1:7d}'.format(key, value))
        print('-' * 21)
        print('{0:1} {1:17d}'.format('SUM', sum(results.values())))
