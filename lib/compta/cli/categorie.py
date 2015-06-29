#!/usr/bin/python
# -*- coding: utf8 -*-
""" Module to manage banque """

from compta.cli.argparser import ParseArgs
from compta.cli.http_server import RequestServer
from compta.cli.server import Server

class Categorie(Server):
    """ List compte account """

    def __init__(self, parser=None):
        """ Init class to manage parse argument """

        Server.__init__(self, parser)
        self.rest_method = "categorie"

    def list(self):
        """ Redefine list to print """
        Server.list(self)
        try:
            for categorie in self.rqst:
                print "%s, %s, %s" % (categorie["id"],
                                      categorie["nom"],
                                      categorie["count"]
                                     )
        except Exception as ex:
            print ex

def main():
    """ Main function """
    parse_args = ParseArgs.get_method("categorie")
    categorie = Categorie(parse_args)
    categorie.launch_cmd()

if __name__ == '__main__':
    main()
