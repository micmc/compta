#!/usr/bin/python
# -*- coding: utf8 -*-
""" Module to manage ecriture """

#from simplejson.scanner import JSONDecodeError
import re
import sys
import csv
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
        self.cache_categorie = None
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
        """ Redefine create to add an ecriture """

        if not self.check_args(self.options.prompt):
            print "Erreur de saisie pour l'ajout, champ manquant ou utiliser prompt option"
            sys.exit(1)

        #Add information for table montant
        if self.options.prompt:
            self.prompt_categorie()
            while True:
                data = unicode(raw_input("Montant : "))
                if re.match(r"^[-+]?\d+[,\.]?\d*$", data):
                    self.attribut['montant'] = data
                    break
            self.rqst = RequestServer.post_method('ecriture',
                                                  self.attribut,
                                                 )
            ecriture_id = re.match(r"^\/ecriture\/(?P<ecriture_id>.*)\/$",
                                   self.rqst.headers['Location']
                                  ).group('ecriture_id')
            self.set_tag(ecriture_id, False)

    def prompt_categorie(self):
        """ print prompt to choose your categorie """
        if self.cache_categorie is None:
            self.cache_categorie = RequestServer.get_method("categorie",
                                                            {'odata': 'count lt 20'},
                                                            ['nom',],
                                                            []
                                                           )

        for i in range(1, 10):
            tmp_str = ""
            for categorie in self.cache_categorie[(i-1)*5:i*5]:
                tmp_str += "%2d - %10s | " % (categorie['id'], categorie['nom'].strip()[0:10])
            print tmp_str[:-3]
        while True:
            data = unicode(raw_input("categorie (defaut: 5): "))
            if data == "":
                self.attribut['categorie_id'] = 5
                break
            if re.match(r"^\d{1,2}$", data):
                self.attribut['categorie_id'] = data
                break

    def import_data(self, extension='csv'):
        """Import ofx file to database, by account
           Import data from a file
           For csv file, there must hae a header like it :
           date;nom;montant
           In attribute, we muste define these parameter :
           compte_id
           By default, all import has default categorie (5)
           A Tag is created with default date for the import
        """
        if not self.options.importfile:
            sys.exit(1)
        if extension == 'ofx':
            ofx_file = open(self.options.importfile)
            ofx_buf = ofx_file.read()
            parser = LinkParser()
            parser.feed(ofx_buf)
            parser.close()
            ofx_file.close()
        elif extension == 'csv':
            with open(self.options.importfile, 'rb') as csvfile:
                csvreader = csv.DictReader(csvfile, delimiter=';', quoting=csv.QUOTE_NONE)
                for row in csvreader:
                    print "import %s - %s - %s" % (row['date'], row['montant'], row['nom'])
                    self.attribut['date'] = datetime.strptime(row['date'],
                                                              "%d/%m/%y").strftime("%Y/%m/%d")
                    self.attribut['nom'] = row['nom']
                    self.attribut['montant'] = str(row['montant'])
                    if self.options.prompt:
                        self.prompt_categorie()
                    else:
                        self.attribut['categorie_id'] = '5'
                    self.rqst = RequestServer.post_method(self.rest_method,
                                                          self.attribut,
                                                         )
                    ecriture_id = re.match(r"^\/ecriture\/(?P<ecriture_id>.*)\/$",
                                           self.rqst.headers['Location']
                                          ).group('ecriture_id')
                    self.set_tag(ecriture_id, True)

    def set_tag(self, ecriture_id, create=False):
        """ Insert a tag if attribute exist and tag name exists """
        if self.tag:
            if not self.tag_id:
                tags = Tag()
                tags.attribut = {}
                tags.filter = {'nom': self.tag}
                tags.get()
                if tags.rqst != False:
                    self.tag_id = tags.rqst[0]['id']
                elif create:
                    tags.attribut['nom'] = self.tag
                    tags.attribut['valeur'] = ""
                    tags.create()
                    self.tag_id = re.match(r"^\/tag\/(?P<tag_id>.*)\/$",
                                           tags.rqst.headers['Location']
                                          ).group('tag_id')
            self.rqst = RequestServer.post_method("tag_ecriture",
                                                  {'ecriture_id': ecriture_id,
                                                   'tag_id': self.tag_id
                                                  },
                                                 )

def main():
    """ Main function """
    parse_args = ParseArgs.get_method("ecriture")
    ecriture = Ecriture(parse_args)
    ecriture.launch_cmd()

if __name__ == '__main__':
    main()



