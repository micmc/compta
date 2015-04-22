#!/usr/bin/python
# -*- coding: utf8 -*-
""" Class to manage ecriture table by cli command """

import re

from json import dumps
from datetime import date

from argparser import ParseArgs
from http_server import RequestServer

class Ecriture(object):
    """ Default class to manage compte """

    def __init__(self):
        """ Init class to manage parse argument """

        self.options = ParseArgs.get_method("ecriture")

    def list_ecriture(self):
        """ List ecriture """

        id = None
        compte = None
        if self.options.id:
            id = self.options.id
        if self.options.compte:
            compte = self.options.compte
        #rqst = RequestServer('localhost', '8080')
        #print rqst.get('ecriture')
        response = RequestServer.get_method("ecriture", ecriture=id, compte=compte)
        for response in response.json():
            print response

    def insert_ecriture(self):
        """ Insert an ecriture """

        data = {}
        data['compte_id'] = self.options.compte
        data['nom'] = unicode(raw_input("nom :"))

        data['montant'] = unicode(raw_input("montant :"))
        if not re.match(r"^\d+(\.\d{1,2})?$", data['montant']):
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
            data['dc'] = self.options.dc

        if not self.options.type:
            data['type'] = unicode(raw_input("Typr [Pr, Vr, Cb, Re, Ch, Li] : "))
            if not re.match(r"^(Pr|Vr|Cb|Re|Ch|Li)$", data['type']):
                raise Exception("Erreur dans le type")
        else:
            data['type'] = self.options.type

        data['date'] = unicode(raw_input("date [YYYY/]DD/MM] :"))
        if not re.match(r"^(201[0-9]\/)?\d{1,2}\/\d{1,2}$", data['date']):
            raise Exception("Erreur dans la date")
        if re.match(r"^\d{2}\/\d{2}$", data['date']):
            data['date'] = str(date.today().year) + "/" + data['date']
        response = RequestServer.get_method("categorie", sort="?sort=count")
        list_categorie = response.json()
        for i in range(1, 4):
            tmp_str = ""
            for categorie in list_categorie[(i-1)*5:i*5]:
                tmp_str += "%d - %12s, " % (categorie['id'], categorie['nom'])
            print tmp_str[:-2]

        data['categorie'] = unicode(raw_input("categorie [consommation : 5] :"))
        if not data['categorie'].isnumeric():
            raise Exception("Erreur de categorie")

        print data
        response = RequestServer.post_method("ecriture", dumps(data))
        print response


def main():
    ecriture = Ecriture()
    if ecriture.options.cmd == 'list':
        ecriture.list_ecriture()
    if ecriture.options.cmd == 'insert':
        ecriture.insert_ecriture()

if __name__ == '__main__':
    main()


