#!/usr/bin/python
# -*- coding: utf8 -*-
""" module to manage argument request command """

from argparse import ArgumentParser
import sys

class ParseArgs(object):
    """ Default class to manage parse argument """

    def __init__(self, **kwargs):
        """Initialize default initialisation parser"""
        self.parser = ArgumentParser(**kwargs)

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
        elif method == "compte":
            return ParseCompte().get_args()
        elif method == "ecriture":
            return ParseEcriture().get_args()

class ParseBanque(ParseArgs):
    """ Class for create banque object """

    def __init__(self, **kwargs):
        """ Initialize default class """
        ParseArgs.__init__(self, **kwargs)

        # Create banque object
        self.parser_banque = self.subparsers.add_parser('banque', help='banque help')
        self.parser_banque.add_argument('cmd',
                                        help='command to pass [list, update, delete, insert]',
                                        choices=('list', 'insert', 'update', 'delete'))
        self.parser_banque.add_argument('-i', '--id', type=int,
                                        help='id of the compte',
                                        nargs=1)

    def get_args(self):
        """ Return argument """
        sys.argv[0] = 'banque'
        return self.parser.parse_args(sys.argv)

class ParseCompte(ParseArgs):
    """ Class for create compte object """

    def __init__(self, **kwargs):
        """ Initialize default class """
        ParseArgs.__init__(self, **kwargs)

        # Create compte object
        self.parser_compte = self.subparsers.add_parser('compte', help='compte help')
        self.parser_compte.add_argument('cmd',
                                        help='command to pass [list, update, delete, insert]',
                                        choices=('list', 'insert', 'update', 'delete')
                                       )
        self.parser_compte.add_argument('-i', '--id', type=int,
                                        help='id of the compte',
                                        nargs=1
                                       )
        self.parser_compte.add_argument('-t', '--type',
                                        choices=['dif', 'div', 'prs', 'prv', 'vir'],
                                        help='Type',
                                       )
        self.parser_compte.add_argument('-a', '--archive', action='store_true',
                                        help='show only archive default [no]'
                                       )
        self.parser_compte.add_argument('--all', action='store_true',
                                        help='show all default [no]'
                                       )
        self.parser_compte.add_argument('-s', '--sort',
                                        help='sort for compte',
                                       )

    def get_args(self):
        """ Return argument """
        sys.argv[0] = 'compte'
        return self.parser.parse_args(sys.argv)


class ParseEcriture(ParseArgs):
    """ Class for create ecriture object """

    def __init__(self, **kwargs):
        """ Initialize default class """
        ParseArgs.__init__(self, **kwargs)

        # Create ecriture object
        self.parser_ecriture = self.subparsers.add_parser('ecriture', help='ecriture help')
        self.parser_ecriture.add_argument('cmd',
                                          help='command to pass [list, update, delete, insert]',
                                          choices=('list', 'insert', 'update', 'delete'))
        self.parser_ecriture.add_argument('-i', '--id', type=int,
                                          help='id of ecriture',
                                         )
        self.parser_ecriture.add_argument('-c', '--compte', type=int,
                                          required=True,
                                          help='id of the compte',
                                         )
        self.parser_ecriture.add_argument('-f', '--filter',
                                          help='filter for compte, must be a number to print or sum',
                                         )
        self.parser_ecriture.add_argument('-s', '--sort',
                                          help='sort for ecriture',
                                         )
        self.parser_ecriture.add_argument('-d', '--dc',
                                          choices=["d", "c"],
                                          help='Débit/Crédit',
                                         )
        self.parser_ecriture.add_argument('-t', '--type',
                                          choices=["Pr", "Vr", "Cb", "Re", "Ch", "Li","Prs"],
                                          help='Type',
                                         )
        self.parser_ecriture.add_argument('-n', '--unvalid', action='store_true',
                                          help='show only no-valid, default [all]'
                                         )
        self.parser_ecriture.add_argument('-v', '--valid', action='store_true',
                                          help='show only valid, default [all]'
                                         )
        self.parser_ecriture.add_argument('--description',
                                          help='Description',
                                         )
    def get_args(self):
        """ Return argument """
        sys.argv[0] = 'ecriture'
        return self.parser.parse_args(sys.argv)


