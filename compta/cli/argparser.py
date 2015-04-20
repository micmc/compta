#!/usr/bin/python
# -*- coding: utf8 -*-
""" module to manage argument request command """

from argparse import ArgumentParser
import sys

class ParseArgs(object):
    """ Default class to manage parse argument """

    def __init__(self, **kwargs):
        """Initialize default initialisation parser"""
        self.parser = ArgumentParser( **kwargs)

        self.parser.add_argument('-d', help='Debug')

        self.subparsers = self.parser.add_subparsers(help='Medthod to get information')

    def get_args(self):
        """ Return argument """

        options = self.parser.parse_args()
        return options

    @staticmethod
    def get_method(method):
        """ Static method to create fabric """

        if method == "banque":
            return ParseBanque().get_args()

class ParseBanque(ParseArgs):
    """ Class for create banque object """

    def __init__(self, **kwargs):
        """ Initialize default class """
        ParseArgs.__init__(self, **kwargs)

        # Create banque object
        self.parser_banque = self.subparsers.add_parser('banque', help='banque help')
        self.parser_test = self.subparsers.add_parser('test', help='banque help')
        self.parser_banque.add_argument('cmd',
                                        help='command to pass [list, update, delete, insert]',
                                        choices=('list', 'update'))
        self.parser_banque.add_argument('-i', '--id', type=int,
                                        help='id of the compte',
                                        nargs=1)

    def get_args(self):
        """ Return argument """
        sys.argv[0] = 'banque'
        return self.parser.parse_args(sys.argv)


