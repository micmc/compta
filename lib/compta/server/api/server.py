#!/usr/bin/python
# -*- coding: utf8 -*-
""" Application to create server for compta """

#import re
#import locale
import sys
import os
import ConfigParser

from json import loads
#from datetime import datetime
#from decimal import Decimal

#from sqlalchemy import create_engine, Column, Integer, Sequence, String
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
#from sqlalchemy import desc
#from sqlalchemy.orm.exc import NoResultFound
#from sqlalchemy.exc import IntegrityError
#from sqlalchemy.sql import func
from sqlalchemy import inspect
from sqlalchemy.orm.properties import ColumnProperty

from compta.server.api.bottle import Bottle

# Equivalent of this form
#from compta.server.api.bottle.ext import sqlalchemy
import compta.server.api.bottle_sqlalchemy as sqlalchemy

from compta.server.api.bottle import abort

from compta.db.base import Base
from compta.db.banque import Banque
from compta.db.compte import Compte
from compta.db.ecriture import Ecriture, Montant, EcritureTag, Tag
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
            plugin = sqlalchemy.Plugin(self.__engine, Base.metadata, create=True)

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

    @classmethod
    def check_data(cls, database, data):
        """ Check data if valid

            return data in dict
            else False
        """
        if not data:
            abort(204, 'No data received')
        entity = {}
        try:
            entity = loads(data)
        except:
            print "erreur chargement json %s" % (data,)
            abort(404, 'Error on loading data')
        mapper = inspect(database)
        orm_data = {}
        for column in mapper.attrs:
            if isinstance(column, ColumnProperty):
                orm_data[column.key] = column.columns[0].nullable
        for column in entity.iterkeys():
            if orm_data.has_key(column):
                del(orm_data[column])
            else:
                return False
        return entity

    @classmethod
    def check_forms(cls, database, data):
        """ Check data from formif valid

            return data in dict
            else False
        """
        if not data:
            abort(204, 'No data received')
        mapper = inspect(database)
        orm_data = {}
        entity = {}
        for column in mapper.attrs:
            if isinstance(column, ColumnProperty):
                orm_data[column.key] = column.columns[0].nullable
        for column in data.iterkeys():
            if orm_data.has_key(column):
                del(orm_data[column])
            else:
                return False
        for key, value in data.iteritems():
            entity[key] = value
        return entity


    @classmethod
    def get_filter(cls, filter):
        """ Get filter in dict

            return  dict of filter
            else false
        """

        if filter:
            dict_filter = {}
            for lst_attribut in filter.split(','):
                attribut = lst_attribut.split(':')
                dict_filter[attribut[0]] = attribut[1]
            return dict_filter
        return False

    @classmethod
    def get_sort(cls, sort):
        """ Get sort in list

            return  dict of filter
            else false
        """

        if sort:
            lst_sort = ["%s" % value for value in sort.split(',')]
            return lst_sort
        return False


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


