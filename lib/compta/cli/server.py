#!/usr/bin/python
# -*- coding: utf8 -*-
""" Module to manage compte """

import sys
import re
#from simplejson.scanner import JSONDecodeError
#from json import dumps

from sqlalchemy import inspect
from sqlalchemy.orm.properties import ColumnProperty
from sqlalchemy.sql.sqltypes import String as DBString

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
        self.attribut = None
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
            self.attribut = {}
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
        #if self.rqst.status_code == 404:
        #    print "%s : information non trouvé" % (self.rest_method)
        #    sys.exit(1)

    def create(self):
        """ create data by rest method """
        if self.check_args():
            self.rqst = RequestServer.post_method(self.rest_method,
                                                  self.attribut,
                                                 )
        #if self.rqst.status_code == 404:
        #    print "%s : information non trouvé" % (self.rest_method)
        #    sys.exit(1)

    def update(self):
        """ create data by rest method """
        self.rqst = RequestServer.put_method(self.rest_method,
                                             self.filter,
                                             self.attribut
                                            )
        #if self.rqst.status_code == 404:
        #    print "%s : information non trouvé" % (self.rest_method)
        #    sys.exit(1)

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
        mapper = inspect(self.database)
        orm_data = {}
        for column in mapper.attrs:
            if isinstance(column, ColumnProperty) and not column.columns[0].primary_key:
                if not column.columns[0].nullable:
                    orm_data[column.key] = column.columns[0].type
        if self.attribut:
            for column,value in orm_data.iteritems():
                if self.attribut.has_key(column):
                    if self.check_type_data(value,self.attribut[column]):
                        print "OK"
                elif not prompt:
                    return False
            return True
        return False
    
    def check_type_data(self, type_data, data):
        """Check datatype to see if is correct before to send to database"""
        print type_data, data, type(type_data)
        if isinstance(type_data, DBString):
            print dir(type_data), type_data.length
            if len(data) <= type_data.length:
                return True
        return False
        #Do for integer
        #Do for date
        #Do for boolean

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



