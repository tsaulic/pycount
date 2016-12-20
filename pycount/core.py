# -*- coding: utf-8 -*-
# pylint: disable=R0912,R0902,R0903


"""
   pycount.core
   ~~~~~~~~~~~~~~~

   Core pycount file

   :copyright: (c) Tihomir Saulic
   :license: DO WHAT YOU WANT TO PUBLIC LICENSE, see LICENSE for more details
"""


from __future__ import print_function

import hashlib
import os
import re
import sys
import time

from pycount.exceptions import InvalidIgnoreTypeError
from pycount.patterns import FILE_TYPE_PATTERNS
from pycount.patterns import COMMENT_PATTERNS
from pycount.patterns import BY_FILES_PATTERNS
from pycount.patterns import IGNORE_PATTERNS


try:
    from binaryornot.check import is_binary
except ImportError as an_error:
    sys.exit(an_error)


def chunk_reader(fobj, chunk_size=1024):
    """Generator that reads a file in chunks of bytes
    """
    while True:
        chunk = fobj.read(chunk_size)
        if not chunk:
            return
        yield chunk


def exact_match(phrase, word):
    """Detects whether an exact match exists between two strings.
    """
    border = r'(\s|^|$)'
    res = re.match(border + word + border, phrase, flags=re.IGNORECASE)
    return bool(res)


def isfile(obj):
    """Check whether a file or not
    """
    if isinstance(obj, str) and os.path.isfile(obj):
        return True


class Timer(object):
    """Times a Class' time between executing __enter__ and __exit__
    """
    def __init__(self):
        self.start = None
        self.end = None
        self.interval = None

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.interval = self.end - self.start


class Counter(object):
    """Main clas for counting the lines of code
    """
    def __init__(self, root=None, patterns=None, by_files=None, ignore=None):
        if root is None:
            self.root = os.getcwd()
        else:
            self.root = root

        self.files = None
        self.hashes = None
        self.results = None
        self.file_types = None
        self.total_uniques = None

        if patterns is None:
            self.patterns = FILE_TYPE_PATTERNS
        else:
            self.patterns = patterns

        if by_files is None:
            self.by_files = BY_FILES_PATTERNS
        else:
            self.by_files = by_files

        if ignore is None:
            self.ignore = IGNORE_PATTERNS
        else:
            new_ignore_list = []
            if isinstance(ignore, list):
                for ipath in ignore:
                    new_ignore_list.append(ipath)
            elif isinstance(ignore, str):
                new_ignore_list.append(ignore)
            else:
                raise InvalidIgnoreTypeError("Must use 'str' or 'list' type")
            self.ignore = IGNORE_PATTERNS + new_ignore_list

        self.comment_patterns = COMMENT_PATTERNS

    def unique(self, a_file, hashing=hashlib.sha1, unique=False):
        """Filters out duplicate files
        """
        if isfile(a_file):
            hashobj = hashing()
            for chunk in chunk_reader(open(a_file, "rb")):
                hashobj.update(chunk)
            file_id = (hashobj.digest(), os.path.getsize(a_file))
            duplicate = self.hashes.get(file_id, None)
            if duplicate:
                pass
            else:
                self.hashes[file_id] = a_file
                unique = True
            return unique

    def walker(self, fpath=None, a_file=None):
        """Takes care of finding actual files that need to be added to
           self.files
        """
        def valid_entry(entry):
            """Detects whether an entry is unique, has data and discards it
               if it's a binary file or a symbolic link
            """
            try:
                has_data = os.stat(entry).st_size > 0
            except OSError:
                has_data = False
            return bool(has_data and self.unique(entry) and \
                not is_binary(entry) and not os.path.islink(entry))
        if a_file is not None and valid_entry(a_file):
            self.files.append(a_file)
        if fpath is not None:
            for path, subpaths, files in os.walk(fpath):
                for pattern in self.ignore:
                    if pattern in subpaths:
                        subpaths.remove(pattern)
                    if pattern in files:
                        files.remove(pattern)
                for a_file in files:
                    for entry in self.by_files.keys():
                        if exact_match(a_file, entry):
                            if valid_entry(a_file):
                                single_file = os.path.join(path, a_file)
                                self.files.append(single_file)
                    if not a_file.startswith("."):
                        a_file = os.path.join(path, a_file)
                        if valid_entry(a_file):
                            self.files.append(a_file)
                            if len(self.files) < 100 and len(self.files) \
                                    % 10 == 0:
                                sys.stdout.write("\r%d unique files"
                                                 % len(self.files))
                                sys.stdout.flush()
                            elif self.files and len(self.files) % 100 == 0:
                                sys.stdout.write("\r%d unique files"
                                                 % len(self.files))
                                sys.stdout.flush()
            print("", end="\r")

    def discover(self):
        """Used to determine what type of dataset user has provided and act
           based on that information. It calls walker() to do actual file
           discovery
        """
        self.files = []
        self.hashes = {}

        if isinstance(self.root, str) and isfile(self.root):
            self.walker(a_file=self.root)
        elif isinstance(self.root, str) and not isfile(self.root):
            self.walker(fpath=self.root)
        elif isinstance(self.root, list):
            for fpath in self.root:
                if isfile(fpath):
                    self.walker(a_file=fpath)
                elif os.path.exists(fpath) and not os.path.isfile(fpath):
                    self.walker(fpath=fpath)
                else:
                    print("Invalid path specified: %s" % fpath)
        self.total_uniques = len(self.files)
        if self.total_uniques > 1:
            print(str(self.total_uniques) + " unique files")
        else:
            print(str(self.total_uniques) + " unique file")

    def is_comment(self, line, extension):
        pass

    def count(self):
        """Counts lines of code for valid files in self.patterns
        """
        self.results = {}
        self.file_types = {}

        for fpath in self.files:
            name = os.path.splitext(os.path.basename(fpath))[0]
            ext = os.path.splitext(fpath)[1]
            full_name = name + ext
            count = 0
            file_type_count = 0
            if full_name in self.by_files.keys():
                fname = full_name
            else:
                fname = name
            if fname in self.by_files.keys():
                with open(fpath, "rb") as a_file:
                    for line in a_file:
                        if line.strip():
                            count += 1
                file_type_count += 1
                try:
                    self.file_types[self.by_files[fname]] += file_type_count
                except KeyError:
                    self.file_types[self.by_files[fname]] = 0
                    self.file_types[self.by_files[fname]] += file_type_count
                try:
                    self.results[self.by_files[fname]] += count
                except KeyError:
                    self.results[self.by_files[fname]] = 0
                    self.results[self.by_files[fname]] += count
            elif ext in self.patterns.keys():
                with open(fpath, "rb") as a_file:
                    for line in a_file:
                        if line.strip():
                            count += 1
                file_type_count += 1
                try:
                    self.file_types[self.patterns[ext]] += file_type_count
                except KeyError:
                    self.file_types[self.patterns[ext]] = 0
                    self.file_types[self.patterns[ext]] += file_type_count
                try:
                    self.results[self.patterns[ext]] += count
                except KeyError:
                    self.results[self.patterns[ext]] = 0
                    self.results[self.patterns[ext]] += count
