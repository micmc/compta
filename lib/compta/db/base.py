#!/usr/bin/python
# -*- coding: utf8 -*-
""" Manage Database """

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlite3 import Connection as SQLite3Connection

Base = declarative_base()

class Table(Base):
    """ generic table to add all other table

    :param Base: Inherit from Base
    """

    __abstract__ = True


    @staticmethod
    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        """ Decorator to add pragma Foreign_keys options

        :param dbapi_connection: database to use
        :param connection_record: record that database is connected
        """
        #if not Table.foreign_keys:
        if isinstance(dbapi_connection, SQLite3Connection):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

