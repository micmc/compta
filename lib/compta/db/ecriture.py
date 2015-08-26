#!/usr/bin/python
# -*- coding: utf8 -*-
""" Manage Database """

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Date, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

from base import Table
from compta.db.categorie import Categorie

#CREATE TABLE "ecriture" (
#    "id" integer NOT NULL PRIMARY KEY,
#    "date" date NOT NULL,
#    "dc" integer NOT NULL,
#    "type" varchar(2) NOT NULL,
#    "nom" varchar(200) NOT NULL,
#    "valide" bool NOT NULL,
#    "compte_id" integer NOT NULL REFERENCES "banque_compte" ("id")
#);
#CREATE INDEX "ecriture_ecriture_d7bcefde" ON "ecriture" ("compte_id");
#sqlite> .schema ecriture.categorie
#sqlite> .schema ecriture_categorie
#CREATE TABLE "ecriture_categorie" (
#    "id" integer NOT NULL PRIMARY KEY,
#    "categorie" varchar(200) NOT NULL,
#    "description" text,
#    "montant" decimal NOT NULL,
#    "ecriture_id" integer NOT NULL REFERENCES "ecriture_ecriture" ("id")
#, categorie_id integer  references "categorie" ("id"));
#CREATE INDEX "ecriture_categorie_507077e5" ON "ecriture_categorie" ("ecri

class Ecriture(Table):
    """ Class to manage ecriture table """
    __tablename__ = 'ecriture'
    id = Column(Integer, primary_key=True)
    date = Column('date', Date, key="[YYYY]/MM/DD/[YYYY]", nullable=False)
    type = Column('type', Enum('Vr', 'Pr', 'Cb', 'Ch', 'Re', 'Li'), key='Vr, Pr, Cb, Ch, Re, Li', nullable=False)
    nom = Column(String(200), nullable=False)
    valide = Column(Boolean, default=False)
    compte_id = Column(Integer, ForeignKey('compte.id'), nullable=False)
    nom_id = Column(Integer, ForeignKey('compte.id'), nullable=True)
    montant = relationship('Montant',
                           single_parent=True,
                           cascade="all, delete-orphan",
                           backref='ecritures'
                          )
    tags = relationship('Tag',
                        cascade="all, delete-orphan",
                        single_parent=True,
                        secondary='ecriture_tag',
                        backref='ecritures'
                       )

class Montant(Table):
    """ Class to manage montant table """
    __tablename__ = 'montant'
    id = Column(Integer, primary_key=True)
    montant = Column(Integer, nullable=False)
    description = Column(String(), nullable=True)
    ecriture_id = Column(Integer, ForeignKey('ecriture.id'), nullable=False)
    categorie_id = Column(Integer, ForeignKey('categorie.id'), nullable=True)
    categorie = relationship(Categorie)

class EcritureTag(Table):
    """ Class to manage ecriture_tag table """
    __tablename__ = 'ecriture_tag'
    id = Column(Integer, primary_key=True)
    ecriture_id = Column(Integer, ForeignKey('ecriture.id'))
    tag_id = Column(Integer, ForeignKey('tag.id'))

class Tag(Table):
    """ Class to manage tag table """
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    nom = Column(String(), nullable=False)
    valeur = Column(String(), nullable=False)

