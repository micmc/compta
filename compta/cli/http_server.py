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

    @staticmethod
    def get_method(method):
        """Static fabric method"""
        if method == "banque":
            return RequestServerBanque()
            

class RequestServerBanque(RequestServer):
    """ Class for create banque object """

    def __init__(self, address='localhost', port='8080'):
        """ Initialize default class """

        RequestServer.__init__(self, address, port)
        self._url_data = self._url_data + "banque"

class RequestServerEcriture(RequestServer):
    """ Class for create ecriture object """

    def __init__(self, address='localhost', port='8080'):
        """ Initialize default class """

        RequestServer.__init__(self, address, port)
        self._url_data = self._url_data + "ecriture"


