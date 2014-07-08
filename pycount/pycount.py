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

    def discover(self):
        for path, subpath, files in os.walk(self.root):
            for a_file in files:
                print(os.path.join(path, a_file))