#!/usr/bin/python
# -*- coding: utf8 -*-
""" Application to create server for compta """

#import re
import locale
#import sys
#import os
#import ConfigParser

#from json import dumps, loads
#from datetime import datetime
#from decimal import Decimal

#from bottle.ext import sqlalchemy
#from sqlalchemy import create_engine, Column, Integer, Sequence, String
#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy import create_engine
#from sqlalchemy import desc
#from sqlalchemy.orm.exc import NoResultFound
#from sqlalchemy.exc import IntegrityError
#from sqlalchemy.sql import func

#from compta.server.api.bottle import Bottle
from compta.server.api.bottle import response

#from compta.db.base import Base
#from compta.db.banque import Banque
#from compta.db.compte import Compte
#from compta.db.ecriture import Ecriture, EcritureCategorie, Tag

from compta.server.api.server import App
from compta.server.api.banque import app as app_banque
from compta.server.api.compte import app as app_compte
from compta.server.api.ecriture import app as app_ecriture
from compta.server.api.categorie import app as app_categorie

app = App().server

def main():
    """ Main Page """
    #Set local value for server
    if locale.getdefaultlocale()[0] != 'fr_FR':
        locale.setlocale(locale.LC_ALL, 'fr_FR.utf8')
    else:
        locale.setlocale(locale.LC_ALL, '')

    app.mount('/api/', app_banque)
    app.mount('/api/', app_compte)
    app.mount('/api/', app_ecriture)
    app.mount('/api/', app_categorie)
    app.run(host='localhost', port=8080, debug=True)

@app.hook('after_request')
def enable_cors():
    """ Header request for cors """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

@app.route('/banque/<id:int>', method=['OPTIONS'])
def default_banque(id):
    """ For firefox, ignore OPTIONS method """
    return {}

if __name__ == "__main__":
    main()

