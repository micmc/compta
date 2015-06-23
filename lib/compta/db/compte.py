#!/usr/bin/python
# -*- coding: utf8 -*-
""" Manage Database """

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Enum
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

from compta.db.base import Base

#CREATE TABLE "compte" (
#    "id" integer NOT NULL PRIMARY KEY,
#    "nom" varchar(50) NOT NULL,
#    "numero" varchar(12) NOT NULL,
#    "cle" varchar(3) NOT NULL,
#    "type" varchar(3) NOT NULL,
#    "archive" bool NOT NULL,
#    "banque_id" integer NOT NULL REFERENCES "banque_banque" ("id")
#);
#CREATE INDEX "banque_compte_decbfcd4" ON "compte" ("banque_id");

class Compte(Base):
    """ Class to manage compte

        Two constraints is used in sqlite :
        ALTER TABLE compte  ADD compte_type_enum  CHECK (type IN ('dif', 'div', 'prs', 'prv', 'vir'));
        ALTER TABLE compte  ADD compte_archive CHECK (archive IN (0, 1)),
    """
    __tablename__ = 'compte'
    id = Column(Integer, primary_key=True)
    nom = Column(String(50), nullable=False)
    numero = Column(String(12), nullable=True)
    cle = Column(String(3), nullable=True)
    type = Column(Enum('dif', 'div', 'prs', 'prv', 'vir',
                       name="compte_type_enum"
                      ),
                  nullable=False
                 )
    archive = Column(Boolean, default=False)
    banque_id = Column(Integer, ForeignKey('banque.id'), nullable=False)
    ecritures = relationship('Ecriture',
                             foreign_keys='Ecriture.compte_id',
                             backref='compte'
                            )

