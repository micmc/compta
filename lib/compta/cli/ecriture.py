#!/usr/bin/python
# -*- coding: utf8 -*-
""" Class to manage ecriture table by cli command """

import re
#import locale

from json import dumps
from datetime import date, datetime

from compta.cli.argparser import ParseArgs
from compta.cli.http_server import RequestServer

class Ecriture(object):
    """ Default class to manage compte """

    def __init__(self):
        """ Init class to manage parse argument """

        self.options = ParseArgs.get_method("ecriture")

    def list_ecriture(self):
        """ List ecriture """

        id = None
        compte = None
        filter = {}
        if self.options.id:
            id = self.options.id
        if self.options.compte:
            compte = self.options.compte
        if self.options.filter:
            filter["filter"] = self.options.filter
        if self.options.valid:
            filter["valide"] = "yes"
        if self.options.unvalid:
            filter["valide"] = "no"
        if self.options.sort:
            filter["sort"] = self.options.sort
        #rqst = RequestServer('localhost', '8080')
        #print rqst.get('ecriture')
        if not filter:
            filter = None
        response = RequestServer.get_method("ecriture",
                                            ecriture=id,
                                            compte=compte,
                                            filter=filter,
                                           )
        if response.status_code == 404:
            return 1
        tmp_response = response.json()
        if isinstance(tmp_response, list):
            for response in tmp_response:
                print "%s - %40s | %8s | %2s | %15s | %d | %d" % \
                      (response["date"],
                       response["nom"],
                       response["montant"],
                       response["type"],
                       response["categorie"],
                       response["id"],
                       response["ecriture_categorie_id"],
                      )
        elif isinstance(tmp_response, dict):
            for k, v in tmp_response.iteritems():
                print "%s -> %s" % (k, v)
        else:
            print tmp_response

    def insert_ecriture(self):
        """ Insert an ecriture """

        data = {}
        data['compte_id'] = self.options.compte
        if not self.options.type in ["Pr", "Vr", "Prs"]:
            data['nom'] = raw_input("nom :")

        data['montant'] = unicode(raw_input("montant :"))
        if not re.match(r"^\d+([\.,]\d{1,2})?$", data['montant']):
            raise Exception("Erreur dans le montant")

        if not self.options.dc:
            data['dc'] = unicode(raw_input("Débit d / Crédit c : "))
            if data['dc'] == "d":
                data['dc'] = -1
            elif data['dc'] == "c":
                data['dc'] = 1
            else:
                raise Exception("Erreur dans Débit/Crédit")
        else:
            if self.options.dc == "d":
                data['dc'] = -1
            elif self.options.dc == "c":
                data['dc'] = 1

        if not self.options.type:
            data['type'] = unicode(raw_input("Typr [Pr, Vr, Cb, Re, Ch, Li]: "))
            if not re.match(r"^(Pr|Vr|Cb|Re|Ch|Li)$", data['type']):
                raise Exception("Erreur dans le type")
        elif self.options.type in ["Pr", "Vr", "Prs"]:
            if self.options.type == 'Pr':
                data['type'] = 'Pr'
                return_compte = RequestServer.get_method("compte",
                                                         filter="prv"
                                                        )
            elif self.options.type == 'Vr':
                data['type'] = 'Vr'
                return_compte = RequestServer.get_method("compte",
                                                         filter="vir"
                                                        )
            elif self.options.type == 'Prs':
                return_compte = RequestServer.get_method("compte",
                                                         filter="prs"
                                                        )
                data['type'] = 'Vr'
            i = 1
            list_compte = []
            for prs in return_compte.json():
                print "%d - %s" % (i, prs['nom'])
                list_compte.append((prs['nom'], prs['id']))
                i += 1
            input_type = raw_input("Virement :")
            data['nom'] = list_compte[int(input_type)-1][0]
            data['nom_id'] = list_compte[int(input_type)-1][1]
        else:
            data['type'] = self.options.type
        if self.options.description:
            date['description'] = self.options.description
        data['date'] = unicode(raw_input("date [YYYY/]DD/MM] :"))
        if not re.match(r"^(201[0-9]\/)?\d{1,2}\/\d{1,2}$", data['date']):
            raise Exception("Erreur dans la date")
        if re.match(r"^\d{2}\/\d{2}$", data['date']):
            data['date'] = str(date.today().year) + "/" + data['date']
        date_now = datetime.now()
        if date_now < datetime.strptime(data["date"], "%Y/%m/%d"):
            raise Exception("La date ne doit pas être dans le future")
        response = RequestServer.get_method("categorie", filter={"sort": "count"})
        list_categorie = response.json()
        for i in range(1, 5):
            tmp_str = ""
            for categorie in list_categorie[(i-1)*5:i*5]:
                tmp_str += "%2d - %16s | " % (categorie['id'], categorie['nom'].strip())
            print tmp_str[:-3]

        data['categorie'] = unicode(raw_input("categorie [consommation : 5] :"))
        if not data['categorie'].isnumeric():
            raise Exception("Erreur de categorie")

        print data
        response = RequestServer.post_method("ecriture", dumps(data))
        print response

    def update_ecriture(self):
        """ Update an ecritue"""

        data = {}
        data['compte_id'] = self.options.compte
        data['id'] = self.options.id
        if self.options.montant:
            data['montant'] = self.options.montant
        if self.options.type:
            data['type'] = self.options.type
        if self.options.dc and self.options.dc == "d":
            data['dc'] = -1
        elif self.options.dc and  self.options.dc == "c":
            data['dc'] = 1
        if self.options.nom:
            data['nom'] = self.options.nom
        if self.options.description:
            data['description'] = self.options.description
        if self.options.date:
            if not re.match(r"^201[0-9]\/\d{1,2}\/\d{1,2}$", self.options.date):
                raise Exception("format non valide de date")
            data['date'] = self.options.date
        if self.options.categorie:
            data['categorie'] = self.options.categorie

        print data
        response = RequestServer.put_method("ecriture", data['id'], dumps(data))
        print response

def main():
    """ Main function """
    #locale.setlocale(locale.LC_ALL, '')
    # print local configuration
    #locale.getlocale()
    ecriture = Ecriture()
    if ecriture.options.cmd == 'list':
        ecriture.list_ecriture()
    elif ecriture.options.cmd == 'insert':
        ecriture.insert_ecriture()
    elif ecriture.options.cmd == 'update':
        ecriture.update_ecriture()

if __name__ == '__main__':
    main()


