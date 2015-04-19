#!/usr/bin/python
# -*- coding: utf8 -*-

import sys     
import os      
import string

from decimal import Decimal
from datetime import datetime

from argparser import ParseArgs

class Banque(object):
    """ Default class to manage compte """

    def __init__(self):
        """ Init class to manage parse argument """

        self.parser = ParseArgs()                  
        self.parser.get_banque()
        self.options = self.parser.get_args()
        print self.options

    def list_banque(self):
        if self.options.id:

    
def main():
    banque = Banque()
    if banque.options.cmd == 'list':
        banque.list_banque

if __name__ == '__main__':
    main()


