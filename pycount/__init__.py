#!/usr/bin/env python
#-*- coding: utf-8 -*-


from __future__ import print_function

import pycount


def check_requirements():

    import sys

    version = getattr(sys, "version_info", (0,))
    if version < (2, 6):
        raise ImportError("pyCount requires python 2.6 or later.")
    if version >= (3, 0):
        print("WARNING: pyCount might not work well with python 3.")


check_requirements()
