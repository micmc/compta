#!/usr/bin/python
# -*- coding: utf8 -*-
""" Module to manage montant """

from compta.db.ecriture import Montant as DBMontant

from compta.cli.argparser import ParseArgs
from compta.cli.http_server import RequestServer
from compta.cli.server import Server

class Montant(Server):
    """ List montant """

    def __init__(self, parser=None):
        """ Init class to manage parse argument """

        Server.__init__(self, parser)
        self.rest_method = "montant"
        self.database = (DBMontant,)

    def list(self):
        """ Redefine list to print """
        Server.list(self)
        try:
            for montant in self.rqst:
                print "%s, %s, %s, %s, %s, %s" % (montant["id"],
                                                  montant["montant"],
                                                  montant["description"],
                                                  montant["categorie_nom"],
                                                  montant["categorie_id"],
                                                  montant["ecriture_id"],
                                                 )
        except Exception as ex:
            print ex

def main():
    """ Main function """
    parse_args = ParseArgs.get_method("montant")
    montant = Montant(parse_args)
    montant.launch_cmd()

if __name__ == '__main__':
    main()
