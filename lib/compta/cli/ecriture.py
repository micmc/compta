#!/usr/bin/python
# -*- coding: utf8 -*-
""" Class to manage ecriture table by cli command """

import re
import locale

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
            sort["sort"] = self.options.sort
        #rqst = RequestServer('localhost', '8080')
        #print rqst.get('ecriture')
        if not filter:
            filter = None
        response = RequestServer.get_method("ecriture",
                                            ecriture=id,
                                            compte=compte,
                                            filter=filter
                                           )
        if response.status_code == 404:
            return 1
        tmp_response = response.json()
        if isinstance(tmp_response, list):
            for response in tmp_response:
                print response
        elif isinstance(tmp_response, dict):
            for k, v in tmp_response.iteritems():
                print "%s -> %s" % (k, v)
        else:
            print tmp_response

    def insert_ecriture(self):
        """ Insert an ecriture """

        data = {}
        data['compte_id'] = self.options.compte
        if not self.options.type in ["Pr", "Vr"]:
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
            data['type'] = unicode(raw_input("Typr [Pr, Vr, Cb, Re, Ch, Li] : "))
            if not re.match(r"^(Pr|Vr|Cb|Re|Ch|Li)$", data['type']):
                raise Exception("Erreur dans le type")
        else:
            data['type'] = self.options.type

        if data['type'] == 'Pr':
            return_prv = RequestServer.get_method("compte",
                                                  filter="prv"
                                                 )
            i = 1
            list_prv = []
            for prs in return_prv.json():
                print "%d - %s" % (i, prs['nom'])
                list_prv.append(prs['nom'])
                i += 1
            input_type = raw_input("Prélèvement :")
            data['nom'] = list_prv[int(input_type)-1]
        if data['type'] == 'Vr':
            return_vir = RequestServer.get_method("compte",
                                                  filter="vir"
                                                 )
            i = 1
            list_vir = []
            for vir in return_vir.json():
                print "%d - %s" % (i, vir['nom'])
                list_vir.append(vir['nom'])
                i += 1
            input_type = raw_input("Virement :")
            data['nom'] = list_vir[int(input_type)-1]
        data['date'] = unicode(raw_input("date [YYYY/]DD/MM] :"))
        if not re.match(r"^(201[0-9]\/)?\d{1,2}\/\d{1,2}$", data['date']):
            raise Exception("Erreur dans la date")
        if re.match(r"^\d{2}\/\d{2}$", data['date']):
            data['date'] = str(date.today().year) + "/" + data['date']
        response = RequestServer.get_method("categorie", filter={"sort": "count"})
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
    """ Main function """
    locale.setlocale(locale.LC_ALL, '')
    # print local configuration
    #locale.getlocale()
    ecriture = Ecriture()
    if ecriture.options.cmd == 'list':
        ecriture.list_ecriture()
    if ecriture.options.cmd == 'insert':
        ecriture.insert_ecriture()

if __name__ == '__main__':
    main()


