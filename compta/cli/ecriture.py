#!/usr/bin/python
# -*- coding: utf8 -*-

import sys     
import os      
import string
import re

from json import dumps
from decimal import Decimal
from datetime import datetime

from argparser import ParseArgs
from http_server import RequestServer

class Ecriture(object):
    """ Default class to manage compte """

    def __init__(self):
        """ Init class to manage parse argument """

        self.options = ParseArgs.get_method("ecriture")

    def list_ecriture(self):
        id = None
        compte = None
        if self.options.id:
            id = self.options.id
        if self.options.compte:
            compte = self.options.compte
        #rqst = RequestServer('localhost', '8080')
        #print rqst.get('ecriture')
        response = RequestServer.get_method("ecriture", ecriture=id, compte=compte)
        print response.json()

    def insert_ecriture(self):
        data={}
        data['compte_id']=self.options.compte
        data['nom'] = unicode(raw_input("nom :"))
        data['montant'] = unicode(raw_input("montant :"))
        if not re.match("^\d+(\.\d{1,2})?$",data['montant']):
            raise Exception("Erreur dans le montant")
        data['dc'] = unicode(raw_input("Débit d / Crédit c : "))
        if data['dc'] == "d":
            data['dc'] = -1
        elif data['dc'] == "c":
            data['dc'] = 1
        else:
            raise Exception("Erreur dans Débit/Crédit")
        data['type'] = unicode(raw_input("Typr [Pr, Vr, Cb, Re, Ch, Li] : "))
        if not re.match("^(Pr|Vr|Cb|Re|Ch|Li)$",data['type']):
            raise Exception("Erreur dans le type")
        data['date'] = unicode(raw_input("date [YYYY/DD/MM] :"))
        if not re.match("^\d{4}\/\d{2}\/\d{2}$",data['date']):
            raise Exception("Erreur dans la date")
        data['categorie'] = unicode(raw_input("categorie [consommation : 5] :"))
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


