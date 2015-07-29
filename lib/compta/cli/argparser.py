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
        self.parser.add_argument('-d', '--debug', help='Debug', action='store_true')
        self.parser.add_argument('-p', '--prompt', help='Prompt', action='store_true')
        self.subparsers = self.parser.add_subparsers(title='database',
                                                     dest='database',
                                                     help='Medthod to get information'
                                                    )
    def get_args(self):
        """ Return argument """

        options = self.parser.parse_args()
        return options

    def set_banque(self):
        """ Initialize banque """
        self.parser_banque = self.subparsers.add_parser('banque', help='banque help')
        self.parser_banque.add_argument('cmd',
                                        help='command to pass [list, update, delete, create]',
                                        choices=('list', 'create', 'update', 'delete'))
        self.parser_banque.add_argument('-f', '--filter', 
                                        help='filter to apply',
                                        nargs='+')
        self.parser_banque.add_argument('-a', '--attribut', 
                                        help='filter on attribut',
                                        nargs='+')
        self.parser_banque.add_argument('-s', '--sort', 
                                        help='filter on sort',
                                        nargs='+')

    def get_banque(self):
        """ Return argument banque """
        sys.argv[0] = 'banque'
        return self.parser.parse_args(sys.argv)

    def set_compte(self):
        """ Initialize compte """
        self.parser_compte = self.subparsers.add_parser('compte', help='compte help')
        self.parser_compte.add_argument('cmd',
                                        help='command to pass [list, update, delete, create]',
                                        choices=('list', 'create', 'update', 'delete')
                                       )
        self.parser_compte.add_argument('-f', '--filter', 
                                        help='filter to apply',
                                        nargs='+')
        self.parser_compte.add_argument('-a', '--attribut', 
                                        help='filter on attribut',
                                        nargs='+')
        self.parser_compte.add_argument('-s', '--sort', 
                                        help='filter on sort',
                                        nargs='+')

    def get_compte(self):
        """ Return argument compte"""
        sys.argv[0] = 'compte'
        return self.parser.parse_args(sys.argv)

    def get_categorie(self):
        """ Return argument categorie"""
        sys.argv[0] = 'categorie'
        return self.parser.parse_args(sys.argv)

    def set_categorie(self):
        """ Initialize categorie """
        self.parser_categorie = self.subparsers.add_parser('categorie', help='categorie help')
        self.parser_categorie.add_argument('cmd',
                                        help='command to pass [list, update, delete, create]',
                                        choices=('list', 'create', 'update', 'delete')
                                       )
        self.parser_categorie.add_argument('-f', '--filter', 
                                        help='filter to apply',
                                        nargs='+')
        self.parser_categorie.add_argument('-a', '--attribut', 
                                        help='filter on attribut',
                                        nargs='+')
        self.parser_categorie.add_argument('-s', '--sort', 
                                        help='filter on sort',
                                        nargs='+')

    def set_ecriture(self):
        """ Initialize ecriture """
        self.parser_ecriture = self.subparsers.add_parser('ecriture', help='ecriture help')
        self.parser_ecriture.add_argument('cmd',
                                          help='command to pass [list, update, delete, create]',
                                          choices=('list', 'create', 'update', 'delete')
                                         )
        self.parser_ecriture.add_argument('-f', '--filter', 
                                          help='filter to apply',
                                          nargs='+')
        self.parser_ecriture.add_argument('-a', '--attribut', 
                                          help='filter on attribut [nom, type, dc, date, valide, compte_id]',
                                          nargs='+')
        self.parser_ecriture.add_argument('-s', '--sort', 
                                          help='filter on sort',
                                          nargs='+')
    
    def get_ecriture(self):
        """ Return argument """
        sys.argv[0] = 'ecriture'
        return self.parser.parse_args(sys.argv)

    def get_montant(self):
        """ Return argument montant"""
        sys.argv[0] = 'montant'
        return self.parser.parse_args(sys.argv)

    def set_montant(self):
        """ Initialize montant """
        self.parser_categorie = self.subparsers.add_parser('montant', help='categorie help')
        self.parser_categorie.add_argument('cmd',
                                        help='command to pass [list, update, delete, create]',
                                        choices=('list', 'create', 'update', 'delete')
                                       )
        self.parser_categorie.add_argument('-f', '--filter', 
                                        help='filter to apply',
                                        nargs='+')
        self.parser_categorie.add_argument('-a', '--attribut', 
                                        help='filter on attribut',
                                        nargs='+')
        self.parser_categorie.add_argument('-s', '--sort', 
                                        help='filter on sort',
                                        nargs='+')

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
        elif method == "montant":
            parse.set_montant()
            return parse.get_montant()
        elif method == "categorie":
            parse.set_categorie()
            return parse.get_categorie()
        else:
            parse.set_banque()
            parse.set_compte()
            parse.set_categorie()
            parse.set_ecriture()
            parse.set_montant()
            return parse.get_args()

class ParseEcriture(ParseArgs):
    """ Class for create ecriture object """

    def __init__(self, **kwargs):
        """ Initialize default class """
        ParseArgs.__init__(self, **kwargs)


