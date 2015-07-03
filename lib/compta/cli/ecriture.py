#!/usr/bin/python
# -*- coding: utf8 -*-
""" Module to manage ecriture """

#from simplejson.scanner import JSONDecodeError
import re

from compta.db.ecriture import Ecriture as DBEcriture
from compta.db.ecriture import Montant as DBMontant

from compta.cli.argparser import ParseArgs
from compta.cli.http_server import RequestServer
from compta.cli.server import Server

class Ecriture(Server):
    """ List ecriture """

    def __init__(self, parser=None):
        """ Init class to manage parse argument """

        Server.__init__(self, parser)
        self.rest_method = "ecriture"
        self.database = (DBEcriture)

    def list(self):
        """ Redefine list to print """
        Server.list(self)
        try:
            if isinstance(self.rqst, list):
                for response in self.rqst:
                    print "%s - %40s | %8s | %2s | %15s / (%s/%s)" % (response["date"],
                                                                      response["nom"],
                                                                      response["montant"],
                                                                      response["type"],
                                                                      response["categorie"],
                                                                      response["id"],
                                                                      response["montant_id"],
                                                                     )
            elif isinstance(self.rqst, dict):
                for k, v in self.rqst.iteritems():
                    print "%s -> %s" % (k, v)
        except Exception as ex:
            print ex

    def create(self):
        """ Redefine create to add categorie """

        #Test data for ecriture
        if self.check_args(self.options.prompt):
            #Next test data for montant

            self.rqst = RequestServer.post_method(self.rest_method,
                                                  self.attribut,
                                                 )
        else:
            print "Erreur de saisie pour l'ajout"
            sys.exit(1)

        list_categorie = RequestServer.get_method("categorie",
                                            {},
                                            ['nom',],
                                            []
                                           )
        for i in range(1, 10):
            tmp_str = ""
            for categorie in list_categorie[(i-1)*5:i*5]:
                tmp_str += "%2d - %16s | " % (categorie['id'], categorie['nom'].strip())
            print tmp_str[:-3]
        data = unicode(raw_input("categorie :"))
        if re.match(r"^\d+([\.,]\d{1,2})?$", data):
            self.attribut['categorie_id'] = data
            Server.create(self)
        else:
            print "Categorie erroné"
            sys.exit(1)

def main():
    """ Main function """
    parse_args = ParseArgs.get_method("ecriture")
    ecriture = Ecriture(parse_args)
    ecriture.launch_cmd()

if __name__ == '__main__':
    main()



