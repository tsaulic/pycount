#-*- coding: utf-8 -*-


from __future__ import print_function


def check_requirements():
    import sys
    version = getattr(sys, "version_info", (0,))
    if version < (2, 6):
        raise ImportError("pycount requires python 2.6 or later.")
    if version >= (3, 0):
        print("WARNING: pycount might not work well with python 3 "
              "as it was not tested.")

check_requirements()
