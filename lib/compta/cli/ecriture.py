#!/usr/bin/python
# -*- coding: utf8 -*-
""" Module to manage ecriture """

#from simplejson.scanner import JSONDecodeError
import re
import sys
from datetime import datetime

from compta.db.ecriture import Ecriture as DBEcriture
from compta.db.ecriture import Montant as DBMontant

from compta.cli.argparser import ParseArgs
from compta.cli.http_server import RequestServer
from compta.cli.server import Server
from compta.cli.sgml_parser import LinkParser
from compta.cli.compte import Compte
from compta.cli.tag import Tag

class Ecriture(Server):
    """ List ecriture """

    def __init__(self, parser=None):
        """ Init class to manage parse argument """

        Server.__init__(self, parser)
        self.rest_method = "ecriture"
        self.database = (DBEcriture,)
        self.tag = None
        self.tag_id = None
        if self.attribut.has_key('tag'):
            self.tag = self.attribut['tag']
            del self.attribut['tag']
        if self.options.cmd == 'list' and \
                not self.filter.has_key('compte_id'):
            print "-f compte_id=<id> is mandatory"
            sys.exit(1)
        if self.options.cmd == 'create' and \
                not self.attribut.has_key('compte_id'):
            print "-a compte_id=<id> is mandatory"
            sys.exit(1)

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
                for key, value in self.rqst.iteritems():
                    print "%s -> %s" % (key, value)
        except Exception as ex:
            print ex

    def create(self):
        """ Redefine create to add categorie """

        if not self.check_args(self.options.prompt):
            print "Erreur de saisie pour l'ajout, champ manquant ou utiliser prompt option"
            sys.exit(1)

        #Add information for table montant
        if self.options.prompt:
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
                    self.attribut['categorie_id'] = data
                    break
            while True:
                data = unicode(raw_input("Montant : "))
                if re.match(r"^[-+]?\d+[,\.]?\d*$", data):
                    self.attribut['montant'] = data
                    break
            self.rqst = RequestServer.post_method('ecriture',
                                                  self.attribut,
                                                 )
            self.set_tag()

    def import_data(self):
        """Import ofx file to database, by account"""
        if not self.options.importfile:
            sys.exit(1)
        ofx_file = open(self.options.importfile)
        ofx_buf = ofx_file.read()
        parser = LinkParser()
        parser.feed(ofx_buf)
        parser.close()
        ofx_file.close()
        comptes = Compte()
        comptes.filter = {'type': 'prs', 'archive': 'false'}
        comptes.attribut = {}
        comptes.get()
        compte_id = None
        for compte in comptes.rqst:
            if compte['numero'] == parser.compte['compte']:
                compte_id = compte['id']
                break
        if compte_id:
            for ecriture in parser.ecriture:
                self.attribut = {'date': ecriture['date'].strftime("%Y/%m/%d"),
                                 'nom': ecriture['name'],
                                 'montant': str(ecriture['montant']),
                                 'compte_id': compte_id,
                                 'categorie_id': '5'
                                }
                if ecriture.has_key('memo'):
                    self.attribut['description'] = ecriture['memo']
                if ecriture['type'] == 'DEBIT':
                    self.attribut['type'] = 'Pr'
                elif ecriture['type'] == 'CREDIT':
                    self.attribut['type'] = 'Vr'
                self.rqst = RequestServer.post_method(self.rest_method,
                                                      self.attribut,
                                                     )
                self.set_tag()
        else:
            print "compte id not found"
            sys.exit(1)

    def set_tag(self):
        """ Insert a tag if attribute exist and tag name exists """
        if self.tag:
            if not self.tag_id:
                tags = Tag()
                tags.attribut = {}
                tags.get()
                for tag in tags.rqst:
                    if tag['nom'] == self.tag:
                        self.tag_id = tag['id']
                        break
                if not self.tag_id:
                    return False
            new_ecriture = re.match(r"^\/ecriture\/(?P<ecriture_id>.*)\/$",
                                    self.rqst.headers['Location']
                                   )
            self.rqst = RequestServer.post_method("tag_ecriture",
                                                  {'ecriture_id':  new_ecriture.group('ecriture_id'),
                                                   'tag_id': self.tag_id
                                                  },
                                                 )
        return False

def main():
    """ Main function """
    parse_args = ParseArgs.get_method("ecriture")
    ecriture = Ecriture(parse_args)
    ecriture.launch_cmd()

if __name__ == '__main__':
    main()



