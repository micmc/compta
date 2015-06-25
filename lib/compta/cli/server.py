#!/usr/bin/python
# -*- coding: utf8 -*-
""" Module to manage compte """

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
        self.parse_args()
        self.filter = None
        self.sort = None
        self.attribut = None
        self.rest_method = None

    def parse_args(self):
        """ parse data """
        if self.options.cmd == 'list':
            if self.options.filter:
                if len(self.options.filter) == 1:
                    self.filter = self.options.filter
                else:
                    self.filter = {}
                    for filter in self.options.filter:
                        tmp_filter = filter.split('=')
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
                                            )

    def launch_cmd(self):
        """ launch command to execute """
        if self.options.cmd == "list":
            self.list()
                                        
class Compte(Server):
    """ List compte account """

    def __init__(self, parser=None):
        """ Init class to manage parse argument """

        Server.__init__(self, parser)
        self.rest_method = "compte"

    def list(self):
        """ Redefine list to print """
        Server.list(self)
        for compte in self.rqst.json():
            print "(%2d) - %s / %s, %s -  %s" % (compte["id"],
                                                 compte["nom"],
                                                 compte["type"],
                                                 compte["numero"],
                                                 compte["cle"]
                                                )

def main():
    """ Main function """
    parse_args = ParseArgs.get_method("all")
    if parse_args.database == 'compte':        
        compte = Compte(parse_args)
        compte.launch_cmd()

if __name__ == '__main__':
    main()



