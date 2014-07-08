#!/usr/bin/env python
#-*- coding: utf-8 -*-


"""
   pycount.pycount
   ~~~~~~~~~~~~~~~

   Core pyCount file

   :copyright: (c) Tihomir Saulic
   :license: BSD, see LICENSE for more details
"""


from __future__ import print_function

import hashlib
import os


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

    def unique(self, filepath, hash=hashlib.sha1, unique=False):
        hashobj = hash()
        for chunk in self.chunk_reader(open(filepath, 'rb')):
                    hashobj.update(chunk)
        file_id = (hashobj.digest(), os.path.getsize(filepath))
        duplicate = self.hashes.get(file_id, None)
        if duplicate:
            print("Duplicate found: %s and %s" % (filepath, duplicate))
        else:
            self.hashes[file_id] = filepath
            unique = True
        return unique

    def discover(self):
        self.files = []
        self.hashes = {}
        for path, subpath, files in os.walk(self.root):
            for a_file in files:
                filepath = os.path.join(path, a_file)
                if os.stat(filepath).st_size > 0 and self.unique(filepath):
                    self.files.append(filepath)
