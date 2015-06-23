#!/usr/bin/python
# -*- coding: utf8 -*-
""" Manage Database """

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from compta.db.base import Base

#CREATE TABLE "banque" (
#    "id" integer NOT NULL PRIMARY KEY,
#    "nom" varchar(50) NOT NULL,
#    "adresse" varchar(200) NOT NULL,
#    "ville" varchar(50) NOT NULL,
#    "cp" varchar(5) NOT NULL,
#    "pays" varchar(2) NOT NULL,
#    "cle_controle" varchar(2) NOT NULL,
#    "code_banque" varchar(5),
#    "code_guichet" varchar(5)
#);

class Banque(Base):
    """ Class to manage banque table """
    __tablename__ = 'banque'
    id = Column(Integer, primary_key=True)
    nom = Column(String(50), nullable=False)
    adresse = Column(String(200), nullable=False)
    ville = Column(String(50), nullable=False)
    cp = Column(String(5), nullable=False)
    pays = Column(String(2), default="FR")
    cle_controle = Column(String(2), default="76")
    code_banque = Column(String(5), nullable=True)
    code_guichet = Column(String(5), nullable=True)
    comptes = relationship('Compte', backref='banque')
