#!/usr/bin/python
# -*- coding: utf8 -*-
""" module to manage request on server """

from argparse import ArgumentParser
import sys     
import os      
import string
import requests

from decimal import Decimal
from datetime import datetime

class RequestServer(object):
    """ Default class to manage parse argument """

    def __init__(self, method, *args, **kwargs):
        """Initialize default initialisation parser"""
        self.request = requests.request(method, *args, **kwargs)
    
    def get_status(self):
        """ Return argument """

        return self.request.status_code

    @staticmethod
    def get_method(method):
        if method == "get":
            pass

#class ParseBanque(ParseArgs):
#    """ Class for create banque object """
#
#    def __init__(self, **kwargs):
#        """ Initialize default class """
#        ParseArgs.__init__(self, **kwargs)
#
#        """ Return banque """
#        self.parser_banque = self.subparsers.add_parser('banque', help='banque help')
#        self.parser_test = self.subparsers.add_parser('test', help='banque help')
#        self.parser_banque.add_argument('cmd', help='command to pass [list, update, delete, insert]', choices=('list','update'))
#        self.parser_banque.add_argument('-i', '--id', type=int, help='id of the compte', nargs=1)
#
#    def get_args(self):
#        """ Return argument """
#        sys.argv[0] = 'banque'
#        return self.parser.parse_args(sys.argv)


