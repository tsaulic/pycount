"""
   pycount.exceptions
   ~~~~~~~~~~~~~~~

   pycount's custom exceptions

   :copyright: (c) Tihomir Saulic
   :license: DO WHAT YOU WANT TO PUBLIC LICENSE, see LICENSE for more details
"""


class InvalidIgnoreTypeError(Exception):
    """The type passed as the ignore argument
       can only be string or list
    """
    pass
