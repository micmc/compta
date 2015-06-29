#!/usr/bin/python
# -*- coding: utf8 -*-
""" Module to manage compte """

import sys

from simplejson.scanner import JSONDecodeError

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
        if self.options.cmd == 'list':
            self.filter = {}
            if self.options.filter:
                for filter in self.options.filter:
                    tmp_filter = filter.split('=')
                    if len(tmp_filter) == 1:
                        self.filter['filter'] = tmp_filter[0]
                    else:
                        self.filter[tmp_filter[0]]=tmp_filter[1]
            if self.options.sort:
                self.sort = self.options.sort
        if self.options.cmd != 'list':
            self.attribut = {}
            for attribut in self.options.attribut:
                tmp_attr = attribut.split('=')
                self.attribut[tmp_attr[0]]=tmp_attr[1]

    def list(self):
        """ get data by rest method """
        self.rqst = RequestServer.get_method(self.rest_method,
                                             self.filter,
                                             self.sort,
                                             self.attribut
                                            )
        if self.rqst.status_code == 404:
            print "%s : information non trouvé" % (self.rest_method)
            sys.exit(1)

    def create(self, data):
        """ create data by rest method """
        json_data = dumps(data)
        self.rqst = RequestServer.post_method(self.rest_method,
                                              json_data,
                                             )
        if self.rqst.status_code == 404:
            print "%s : information non trouvé" % (self.rest_method)
            sys.exit(1)

    def update(self, data):
        """ create data by rest method """
        json_data = dumps(data)
        self.rqst = RequestServer.put_method(self.rest_method,
                                             json_data,
                                            )
        if self.rqst.status_code == 404:
            print "%s : information non trouvé" % (self.rest_method)
            sys.exit(1)

    def launch_cmd(self, cmd=None):
        """ launch command to execute """
        if not cmd:
            cmd = self.options.cmd
        if self.options.cmd == "list":
            self.list()
        elif self.options.cmd == "create":
            self.create(self.attribut)
        elif self.options.cmd == "update":
            self.update(self.attribut)
                                        
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
    if parse_args.database == 'categorie':        
        from compta.cli.categorie import Categorie
        categorie = Categorie(parse_args)
        categorie.launch_cmd()

if __name__ == '__main__':
    main()



