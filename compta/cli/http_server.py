#!/usr/bin/python
# -*- coding: utf8 -*-
""" module to manage request on server """

import sys
import requests
from json import dumps, loads

class RequestServer(object):
    """ Default class to manage parse argument """

    def __init__(self, address='localhost', port='8080'):
        """Initialize default initialisation parser"""
        self.__session = requests.Session()
        self.__address = address
        self.__port = port
        #self.__request = requests.request()
        self._url_data = 'http://%s:%s/' % (self.__address,
                                            self.__port)

    def get(self, url=None, filter=None):
        """Get url data"""
        url_data = self._url_data
        if url is not None:
            url_data += url 
        if filter is not None:
            url_data += filter
        self.__request = self.__session.get(url_data)
        return self.__request

    def post(self, data):
        """Put url data"""
        url_data = self._url_data
        self.__request = self.__session.post(url_data, data)
        return self.__request

    @staticmethod
    def get_method(method, banque=None, compte=None, ecriture=None, categorie=None, sort=None):
        """Static fabric method"""
      
        filter = ""
        if method == "banque":
            rqst =  RequestServerBanque()
            if banque:
                filter="/%s" % (banque,)
            return rqst.get(filter=filter)
        elif method == "compte":
            rqst =  RequestServerCompte()
            if banque:
                rqst =  RequestServerBanque()
                filter = "/%s/compte" % (banque,)
            elif compte:
                filter += "/%s" % (compte,)
            return rqst.get(filter=filter)
        elif method == "ecriture":
            rqst = RequestServerEcriture()
            if compte:
                rqst = RequestServerCompte()
                filter = "/%s/ecriture" % (compte,)
            if ecriture:
                filter += "/%s" % (ecriture,)
            return rqst.get(filter=filter)
        elif method == "categorie":
            rqst = RequestServerCategorie()
            if categorie:
                filter += "/%s" % (categorie,)
            if sort:
                filter += sort 
            return rqst.get(filter=filter)


    @classmethod
    def post_method(cls, method, data):
        if method == "ecriture":
            rqst = RequestServerEcriture()
            return rqst.post(data)

class RequestServerBanque(RequestServer):
    """ Class for create banque object """

    def __init__(self, address='localhost', port='8080'):
        """ Initialize default class """

        RequestServer.__init__(self, address, port)
        self._url_data = self._url_data + "banque"

class RequestServerCompte(RequestServer):
    """ Class for create compte object """

    def __init__(self, address='localhost', port='8080'):
        """ Initialize default class """

        RequestServer.__init__(self, address, port)
        self._url_data = self._url_data + "compte"


class RequestServerEcriture(RequestServer):
    """ Class for create ecriture object """

    def __init__(self, address='localhost', port='8080'):
        """ Initialize default class """

        RequestServer.__init__(self, address, port)
        self._url_data = self._url_data + "ecriture"

class RequestServerCategorie(RequestServer):
    """ Class for create categorie object """

    def __init__(self, address='localhost', port='8080'):
        """ Initialize default class """

        RequestServer.__init__(self, address, port)
        self._url_data = self._url_data + "categorie"


