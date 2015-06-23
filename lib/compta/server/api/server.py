#!/usr/bin/python
# -*- coding: utf8 -*-
""" Application to create server for compta """

import re
import locale
import sys
import os
import ConfigParser

from bottle import Bottle
from bottle import response, request, abort
from json import dumps, loads
from datetime import datetime
#from decimal import Decimal

from bottle.ext import sqlalchemy
#from sqlalchemy import create_engine, Column, Integer, Sequence, String
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import desc
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func

from compta.db.base import Base
from compta.db.banque import Banque
from compta.db.compte import Compte
from compta.db.ecriture import Ecriture, EcritureCategorie, Tag
from compta.db.categorie import Categorie

class App(object):
    """ Singleton to create App instance """

    class __OnlyApp(object):
        """ Class method to create database """

        def __init__(self, debug):
            """Initialize default connection to a database"""

            dict_config = Config.get_config()
            self.__engine = create_engine("sqlite:///%s/%s" % (dict_config["database_path"],
                                                               dict_config["database_name"]
                                                              ),
                                          echo=debug
                                         )
            Base.metadata.bind = self.__engine
            Base.metadata.create_all(self.__engine)
            plugin = sqlalchemy.Plugin(self.__engine, Base.metadata, create=False)

            self._app = Bottle()
            self._app.install(plugin)

        @property
        def server(self):
            """Get session"""
            return self._app

    instance = None

    #@classmethod
    def __new__(cls, debug=False):
        """ class method to get instance class """
        if not App.instance:
            App.instance = App.__OnlyApp(debug)
        return App.instance

class Config(object):
    """ Read config """

    @classmethod
    def get_config(cls):
        """ Get data on file """
        path = os.path.dirname(__file__)
        config = ConfigParser.RawConfigParser()
        if os.path.exists("%s/../server.cfg" % path):
            dict_config = {}
            try:
                config.read("%s/../server.cfg" % path)
            except ConfigPArser.ParsingError as error:
                print error
                sys.exit(1)
            try:
                dict_config["database_path"] = config.get("Database", "path")
                dict_config["database_name"] = config.get("Database", "name")
            except ConfigParser.NoSectionError as error:
                print error
                sys.exit(1)
            except ConfigParser.NoOptionError as error:
                print error
                sys.exit(1)
            return dict_config
        else:
            print "No config files found"
            sys.exit(1)

