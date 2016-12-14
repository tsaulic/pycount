#-*- coding: utf-8 -*-


from __future__ import print_function


def check_requirements():
    import sys
    version = getattr(sys, "version_info", (0,))
    if version < (2, 6):
        raise ImportError("pycount requires python 2.6 or later.")

check_requirements()
