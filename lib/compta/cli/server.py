#!/usr/bin/python
# -*- coding: utf8 -*-
""" Module to manage compte """

import sys
import re
import copy
from datetime import date,datetime

#from simplejson.scanner import JSONDecodeError
#from json import dumps

from sqlalchemy import inspect
from sqlalchemy.orm.properties import ColumnProperty
from sqlalchemy.sql.sqltypes import String as DBString
from sqlalchemy.sql.sqltypes import Integer as DBInteger
from sqlalchemy.sql.sqltypes import Date as DBDate
from sqlalchemy.sql.sqltypes import Boolean as DBBoolean
#from sqlalchemy.sql.sqltypes import float as DBFloat

#from compta.db.categorie import Categorie

from compta.cli.argparser import ParseArgs
from compta.cli.http_server import RequestServer


class Server(object):
    """ Default class to manage database """

    def __init__(self, parser=None):
        """ Init class to manage parse argument """

        if not parser:
            self.options = ParseArgs.get_method("all")
        else:
            self.options = parser
        self.filter = None
        self.sort = None
        self.attribut = {}
        self.rest_method = None
        self.parse_args()

    def parse_args(self):
        """ parse data """
        self.filter = {}
        if self.options.filter:
            for filter in self.options.filter:
                tmp_filter = filter.split('=')
                if len(tmp_filter) == 1:
                    self.filter['filter'] = tmp_filter[0]
                else:
                    self.filter[tmp_filter[0]] = tmp_filter[1]
        if self.options.cmd == 'list':
            if self.options.sort:
                self.sort = self.options.sort
        if self.options.cmd != 'list':
            if self.options.attribut:
                for attribut in self.options.attribut:
                    tmp_attr = attribut.split('=')
                    self.attribut[tmp_attr[0]] = tmp_attr[1]

    def list(self):
        """ get data by rest method """
        self.rqst = RequestServer.get_method(self.rest_method,
                                             self.filter,
                                             self.sort,
                                             self.attribut
                                            )

    def create(self):
        """ create data by rest method """
        if self.check_args(self.options.prompt):
            self.rqst = RequestServer.post_method(self.rest_method,
                                                  self.attribut,
                                                 )
        else:
            print "Erreur de saisie pour l'ajout"
            sys.exit(1)

    def update(self):
        """ create data by rest method """
        self.rqst = RequestServer.put_method(self.rest_method,
                                             self.filter,
                                             self.attribut
                                            )

    def launch_cmd(self, cmd=None):
        """ launch command to execute """
        if not cmd:
            cmd = self.options.cmd
        if self.options.cmd == "list":
            self.list()
        elif self.options.cmd == "create":
            self.create()
        elif self.options.cmd == "update":
            self.update()

    def check_args(self, prompt=False):
        """ Method to check wich argument is mandatory

            Do an introspection in database
            Check for witch argument give by parse_arg if arugment is missing

            If prompt is True, display en prompt to give argument, test it and save it
            return True if OK
            else False
        """
        #attrs = dict((key,value) for key,value in self.attribut.items())
        attrs = copy.deepcopy(self.attribut)
        for database in self.database:
            mapper = inspect(database)
            for column in mapper.attrs:
                if isinstance(column, ColumnProperty) and \
                        not column.columns[0].primary_key:
                    if not attrs.has_key(column.key) and \
                            not column.columns[0].foreign_keys and \
                            not column.columns[0].nullable:
                        if prompt:
                            data = unicode(raw_input("%s [%s]: " % (column.key,
                                                                    column.columns[0].key
                                                                   )
                                                    )
                                          )
                            data = self.check_type_data(column.columns[0], data)
                            if data is None:
                                print "Type non reconnue pour %s (%s)" % (column.key, column.columns[0].type)
                                return False
                            self.attribut[column.key] = data
                        else:
                            return False
                    elif attrs.has_key(column.key):
                        del(attrs[column.key])
        if attrs:
            print "champs non reconnu %s" % attrs
            return False
        return True

    def check_type_data(self, type_data, data):
        """Check datatype to see if is correct before to send to database"""
        if isinstance(type_data.type, DBString):
            if type_data.key:
                lst_enums = ["%s" % enum for enum in type_data.key.split(",")]
                if data in lst_enums:
                    return data
            if len(data) <= type_data.type.length:
                return data
        elif isinstance(type_data.type, DBInteger):
            if re.match(r"^\d+$", data):
                return data
            elif re.match(r"^\d+([\.,]\d{1,2})?$", data):
                return data
        elif isinstance(type_data.type, DBDate):
            date_now = datetime.now()
            date_data = None
            re_date = re.match(r"^(?P<year>201[0-9])\/(?P<month>\d{1,2})\/(?P<day>\d{1,2})$", data)
            if re_date:
                date_data = "%s/%s/%s" % (re_date.group('year'),
                                          re_date.group('month'),
                                          re_date.group('day')
                                         )
            re_date = re.match(r"^(?P<day>\d{1,2})\/(?P<month>\d{1,2})(\/(?P<year>201[0-9]))?$", data)
            if re_date:
                if re_date.group('year'):
                    date_data = "%s/" % re_date.group('year')
                else:
                    date_data = "%s/" % str(date.today().year)
                date_data += "%s/%s" % (re_date.group('month'),
                                        re_date.group('day')
                                       )
            try:
                if date_data and date_now > datetime.strptime(date_data, "%Y/%m/%d"):
                    return date_data
            except Exception:
                pass
        elif isinstance(type_data.data, DBBoolean):
            if re.match(r"(0|Off|False)", data):
                return False
            elif re.match(r"(1|On|True)", data):
                return True
        return None

def main():
    """ Main function """
    parse_args = ParseArgs.get_method("all")
    if parse_args.database == 'compte':
        from compta.cli.compte import Compte
        compte = Compte(parse_args)
        compte.launch_cmd()
    if parse_args.database == 'banque':
        from compta.cli.banque import Banque
        banque = Banque(parse_args)
        banque.launch_cmd()
    if parse_args.database == 'ecriture':
        from compta.cli.ecriture import Ecriture
        ecriture = Ecriture(parse_args)
        ecriture.launch_cmd()
    if parse_args.database == 'categorie':
        from compta.cli.categorie import Categorie
        categorie = Categorie(parse_args)
        categorie.launch_cmd()

if __name__ == '__main__':
    main()



