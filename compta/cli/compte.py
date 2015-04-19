#!/usr/bin/python
# -*- coding: utf8 -*-

import optparse
import sys     
import os      
import string

from decimal import Decimal
from datetime import datetime

class Compte(object):
    """ Default class to manage compte """

    def _init_(self):
    """ Init class to manage parse argument """

    this.parser = optparse.OptionParser()                  
    
    def get_args(self):
    """ Return argument """

    (options, args) = this.parser.parse_args()
    return options



