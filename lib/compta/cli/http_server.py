#!/usr/bin/python
# -*- coding: utf8 -*-
""" module to manage request on server """

#import sys
import requests
from json import loads, dumps

class RequestServer(object):
    """ Default class to manage parse argument """

    def __init__(self, address='localhost', port='8080'):
        """Initialize default initialisation parser"""
        self.__session = requests.Session()
        self.__address = address
        self.__port = port
        self.__request = None
        self._url_data = 'http://%s:%s/' % (self.__address,
                                            self.__port)

    def get(self, url=None, filter=None):
        """Get url data"""
        url_data = self._url_data
        if url is not None:
            url_data += url
        if filter:
            url_data += "?" + ",".join(["%s" % values for values in filter])
        self.__request = self.__session.get(url_data)
        if self.__request.status_code != 200:
            return False
        else:
            return self.__request.json()

    def post(self, data):
        """Post url data"""
        url_data = self._url_data
        self.__request = self.__session.post(url_data, data)
        return self.__request

    def put(self, url, data):
        """Put url data"""

        url_data = self._url_data + url
        self.__request = self.__session.put(url_data, data)
        return self.__request

    @classmethod
    def get_method(cls,
                   method,
                   filter,
                   sort,
                   attribut
                  ):
        """ Static fabric method """

        str_url = ""
        lst_filter = []
        #Create URL
        if method == "banque":
            rqst = RequestServerBanque()
            if filter.has_key('id'):
                str_url = "/%s" % (filter['id'],)
                del(filter['id'])
        elif method == "compte":
            rqst = RequestServerCompte()
            if filter.has_key('banque_id'):
                rqst = RequestServerBanque()
                str_url = "/%s/compte" % (filter['banque_id'],)
                del(filter['banque_id'])
            if filter.has_key('id'):
                str_url += "/%s" % (filter['id'],)
                del(filter['id'])
        elif method == "ecriture":
            rqst = RequestServerEcriture()
            if filter.has_key('compte_id'):
                rqst = RequestServerCompte()
                str_url = "/%s/ecriture" % (filter['compte_id'],)
                del(filter['compte_id'])
            if filter.has_key('id'):
                str_url += "/%s" % (filter['id'],)
                del(filter['id'])
        elif method == "categorie":
            rqst = RequestServerCategorie()
            if filter.has_key('id'):
                str_url = "/%s" % (filter['id'],)
                del(filter['id'])
        #Create filter
        if filter:
            lst_filter.append('filter=' + ','.join(["%s:%s" % (keys, values) for keys, values in filter.iteritems()]))
        if sort:
            lst_filter.append('sort=' + ','.join(["%s" % values for values in sort]))
        if attribut:
            lst_filter.append('attribut=' + ','.join(["%s" % values for values in attribut]))
        return rqst.get(url=str_url, filter=lst_filter)


    @classmethod
    def post_method(cls,
                    method,
                    data
                   ):
        """ Static fabric method """

        if method == "banque":
            rqst = RequestServerBanque()
        elif method == "compte":
            rqst = RequestServerCompte()
        elif method == "categorie":
            rqst = RequestServerCategorie()
        elif method == "Ecriture":
            rqst = RequestServerEcriture()
        else:
            return False
        return rqst.post(dumps(data))

    @classmethod
    def put_method(cls,
                   method,
                   filter,
                   data
                  ):
        """ Static fabric method """

        #entity = loads(data)
        print method, filter, data
        if not filter.has_key("id"):
            return False
        if method == "banque":
            rqst = RequestServerBanque()
        elif method == "compte":
            rqst = RequestServerCompte()
        elif method == "categorie":
            rqst = RequestServerCategorie()
        elif method == "Ecriture":
            rqst = RequestServerEcriture()
        else:
            return False
        str_url = "/%s" % (filter["id"])
        return rqst.put(url=str_url, data=dumps(data))
        #if method == "split":
        #    rqst = RequestServerEcriture()
        #    str_url = "/%s/ec/%s" % (entity['id'],entity['ecriture_categorie_id'])
        #    return rqst.put(url=str_url, data=data)

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


