#!/usr/bin/python
# -*- coding: utf8 -*-
""" Module to manage ecriture """

#from simplejson.scanner import JSONDecodeError
import re
import sys

from compta.db.ecriture import Ecriture as DBEcriture
from compta.db.ecriture import Montant as DBMontant

from compta.cli.argparser import ParseArgs
from compta.cli.http_server import RequestServer
from compta.cli.server import Server
from compta.cli.server import LinkParser

class Ecriture(Server):
    """ List ecriture """

    def __init__(self, parser=None):
        """ Init class to manage parse argument """

        Server.__init__(self, parser)
        self.rest_method = "ecriture"
        self.database = (DBEcriture,)

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

        #Add information for table montant
        if self.options.prompt:
            attribut_montant = {}
            new_ecriture = re.match(r"^\/ecriture\/(?P<ecriture_id>.*)\/$",
                                    self.rqst.headers['Location']
                                   )
            attribut_montant['ecriture_id'] = new_ecriture.group('ecriture_id')
            list_categorie = RequestServer.get_method("categorie",
                                                {'odata': 'count lt 20'},
                                                ['nom',],
                                                []
                                               )
            for i in range(1, 10):
                tmp_str = ""
                for categorie in list_categorie[(i-1)*5:i*5]:
                    tmp_str += "%2d - %16s | " % (categorie['id'], categorie['nom'].strip())
                print tmp_str[:-3]
            while True:
                data = unicode(raw_input("categorie : "))
                if re.match(r"^\d{1,2}$", data):
                    attribut_montant['categorie_id'] = data
                    break
            while True: 
                data = unicode(raw_input("Montant : "))
                if re.match(r"^\d+[,\.]?\d*$", data):
                    attribut_montant['montant'] = data
                    break
            montant_rqst = RequestServer.post_method('montant',
                                                     attribut_montant,
                                                    )
            print montant_rqst.headers

    def import_data(self):
        """Import ofx file to database, by account"""
        if not self.options.importfile:
            sys.exit(1)
        ofx_file = open(self.options.importfile)
        ofx_buf = ofx_file.read()
        print "openfile OK"
        p = LinkParser()
        p.feed(ofx_buf)
        p.close()
        ofx_file.close()
        print p.compte
        print p.ecriture


def main():
    """ Main function """
    parse_args = ParseArgs.get_method("ecriture")
    ecriture = Ecriture(parse_args)
    ecriture.launch_cmd()

if __name__ == '__main__':
    main()



