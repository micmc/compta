#!/usr/bin/python
# -*- coding: utf8 -*-

import sys     
import os      
import string

from decimal import Decimal
from datetime import datetime

from argparser import ParseArgs
from http_server import RequestServer

class Banque(object):
    """ Default class to manage compte """

    def __init__(self):
        """ Init class to manage parse argument """

        self.options = ParseArgs.get_method("banque")

    def list_banque(self):
        if self.options.id:
            pass
        #rqst = RequestServer('localhost', '8080')
        #print rqst.get('banque')
        rqst = RequestServer.get_method("banque")
        print rqst.json()

    
def main():
    banque = Banque()
    if banque.options.cmd == 'list':
        banque.list_banque()

if __name__ == '__main__':
    main()


