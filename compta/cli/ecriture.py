#!/usr/bin/python
# -*- coding: utf8 -*-

import sys     
import os      
import string

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
        if self.options.id:
            pass
        #rqst = RequestServer('localhost', '8080')
        #print rqst.get('ecriture')
        rqst = RequestServer.get_method("ecriture")
        response =  rqst.get()
        print response.json()

    
def main():
    ecriture = Banque()
    if ecriture.options.cmd == 'list':
        ecriture.list_ecriture()

if __name__ == '__main__':
    main()


