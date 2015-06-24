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

    def set_banque(self):
        """ Initialize banque """
        self.parser_banque = self.subparsers.add_parser('banque', help='banque help')
        self.parser_banque.add_argument('cmd',
                                        help='command to pass [list, update, delete, insert]',
                                        choices=('list', 'insert', 'update', 'delete'))
        self.parser_banque.add_argument('-i', '--id', type=int,
                                        help='id of the compte',
                                        nargs=1)

    def get_banque(self):
        """ Return argument banque """
        sys.argv[0] = 'banque'
        return self.parser.parse_args(sys.argv)

    def set_compte(self):
        """ Initialize compte """
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

    def get_compte(self):
        """ Return argument """
        sys.argv[0] = 'compte'
        return self.parser.parse_args(sys.argv)

    def set_ecriture(self):
        """ Initialize ecriture """

        # Create ecriture object
        self.parser_ecriture = self.subparsers.add_parser('ecriture', help='ecriture help')
        self.parser_ecriture.add_argument('cmd',
                                          help='command to pass [list, update, delete, insert, split]',
                                          choices=('list', 'insert', 'update', 'delete', 'split'))
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
                                          choices=["Pr", "Vr", "Cb", "Re", "Ch", "Li", "Prs"],
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
        self.parser_ecriture.add_argument('--nom',
                                          help='Nom',
                                         )
        self.parser_ecriture.add_argument('--montant',
                                          help='Montant',
                                         )
        self.parser_ecriture.add_argument('--date',
                                          help='Date [YYYY/MM/DD]',
                                         )
        self.parser_ecriture.add_argument('--categorie',
                                          help='Categorie',
                                         )
        self.parser_ecriture.add_argument('--ec',
                                          help='Ecriture Categorie id',
                                         )
    def get_ecriture(self):
        """ Return argument """
        sys.argv[0] = 'ecriture'
        return self.parser.parse_args(sys.argv)

    @staticmethod
    def get_method(method):
        """ Static method to create fabric """

        parse = ParseArgs()
        if method == "banque":
            parse.set_banque()
            return parse.get_banque()
        elif method == "compte":
            parse.set_compte()
            return parse.get_compte()
        elif method == "ecriture":
            parse.set_ecriture()
            return parse.get_ecriture()
        else:
            parse.get_banque()
            parse.get_compte()
            parse.get_ecriture()
            return parse.get_args()

class ParseEcriture(ParseArgs):
    """ Class for create ecriture object """

    def __init__(self, **kwargs):
        """ Initialize default class """
        ParseArgs.__init__(self, **kwargs)


