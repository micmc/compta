#!/usr/bin/python
# -*- coding: utf8 -*-
""" Manage Database """

from sqlalchemy import Column, Integer, String

from compta.db.base import Base

#CREATE TABLE categorie("id" integer NOT NULL PRIMARY KEY, "nom" varchar(200) NOT NULL);

class Categorie(Base):
    """ Class to manage Categorie table """
    __tablename__ = 'categorie'
    id = Column(Integer, primary_key=True)
    nom = Column(String(200), nullable=False)
