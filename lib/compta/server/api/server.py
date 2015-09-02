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
            if isinstance(column, ColumnProperty) and \
               not column.columns[0].nullable and \
               not column.columns[0].foreign_keys and \
               not column.columns[0].primary_key:
                orm_data[column.key] = column.columns[0].nullable
            else:
                pass
        for field in orm_data.iterkeys():
            if entity.has_key(field):
                #del(orm_data[column])
                pass
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
    def get_filter(cls, filter, odata=False):
        """ Get filter in dict

            return  dict of filter if odata=False
            if odata=True return a list
            else False
        """

        if filter:
            #www.odata.org/libraries
            if odata:
                lst_filter = []
                if 'and' in filter:
                    tmp_filters = filter.split('and')
                else:
                    tmp_filters = [filter, ]
                for tmp_filter in tmp_filters:
                    if 'eq' in tmp_filter:
                        tmp_filter = tmp_filter.replace('eq', '=')
                    elif 'gt' in tmp_filter:
                        tmp_filter = tmp_filter.raplace('gt', '>')
                    elif 'lt' in tmp_filter:
                        tmp_filter = tmp_filter.replace('lt', '>')
                    lst_filter.append(tmp_filter.split())
                return lst_filter
            else:
                dict_filter = {}
                for lst_attribut in filter.split(','):
                    attribut = lst_attribut.split(':')
                    if "/" in attribut[1]:
                        dict_filter[attribut[0]] =  attribut[1].split('/')
                    else:
                        if attribut[1] == 'false':
                            dict_filter[attribut[0]] = False
                        elif attribut[1] == 'true':
                            dict_filter[attribut[0]] = True
                        else:
                            dict_filter[attribut[0]] = attribut[1]
                return dict_filter
        return False

    @classmethod
    def convert_value(cls, value):
        if value == 'false':
            return False
        elif value == 'true':
            return True
        elif value == 'null':
            return None
        else:
            return value

    @classmethod
    def get_sort(cls, sort):
        """ Get sort in list

            return list of filter
            else false
        """

        if sort:
            lst_sort = ["%s" % value for value in sort.split(',')]
            return lst_sort
        return False

    @classmethod
    def get_attribut(cls, attribut):
        """ Get attribut in list

            return list of filter
            else false
        """

        if attribut:
            lst_attribut = ["%s" % value for value in attribut.split(',')]
            return lst_attribut
        return False


class Config(object):
    """ Read config
        Default file :
        1/ /etc/compta/server.cfg
        2/ ~/.compta/server.cfg
        3/ python_path/compta/server/server.cfg
    """

    DEFAULT_CONFIGURATION_FILE = "/etc/compta/server.cfg"

    @classmethod
    def get_config(cls):
        """ Get data on file """
        path_home = os.path.expanduser('~')
        path_app = os.path.dirname(__file__)
        config = ConfigParser.RawConfigParser()
        paths = [Config.DEFAULT_CONFIGURATION_FILE,
                 "%s/.compta/server.cfg" % path_home,
                 "%s/../server.cfg" % path_app
                ]
        get_file = False
        for path in paths:
            if os.path.exists(path):
                try:
                    config.read(path)
                    get_file = True
                except ConfigPArser.ParsingError as error:
                    print error
                    sys.exit(1)
                break
        if not get_file:
            print "No config files found"
            sys.exit(1)

        dict_config = {}
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


