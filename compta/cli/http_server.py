#!/usr/bin/python
# -*- coding: utf8 -*-
""" module to manage request on server """

import sys
import requests
from json import dumps, loads

class RequestServer(object):
    """ Default class to manage parse argument """

    def __init__(self, address, port):
        """Initialize default initialisation parser"""
        self.__session = requests.Session()
        self.__address = address
        self.__port = port
        #self.__request = requests.request()

    def get(self, url):
        """Get url data"""
        url_data = 'http://%s:%s/%s' % (self.__address,
                                        self.__port,
                                        url)
        self.__request = self.__session.get(url_data)
        for data in self.__request.json():
            print data
        print self.__request.headers
        return self.__request.status_code

    @staticmethod
    def get_method(method):
        """Static fabric method"""
        if method == "get":
            pass

class RequestServerBanque(RequestServer):
    """ Class for create banque object """

    def __init__(self, adresse, port):
        """ Initialize default class """

        RequestServer.__init__(self, adresse, port)

