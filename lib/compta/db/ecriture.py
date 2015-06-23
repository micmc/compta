#!/usr/bin/python
# -*- coding: utf8 -*-
""" Manage Database """

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Date, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

from base import Base

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

class Ecriture(Base):
    """ Class to manage ecriture table """
    __tablename__ = 'ecriture'
    id = Column(Integer, primary_key=True)
    date = Column('date', Date, nullable=False)
    dc = Column(Integer, nullable=False)
    type = Column('type', Enum('Vr', 'Pr', 'Cb', 'Ch', 'Re', 'Li'), nullable=False)
    nom = Column(String(200), nullable=False)
    valide = Column(Boolean, default=False)
    compte_id = Column(Integer, ForeignKey('compte.id'), nullable=False)
    nom_id = Column(Integer, ForeignKey('compte.id'), nullable=True)
    montant = relationship('Montant',
                           backref='ecritures'
                          )
    tags = relationship('Tag',
                        secondary='ecriture_tag',
                        backref='ecritures'
                       )

class Montant(Base):
    """ Class to manage montant table """
    __tablename__ = 'ecriture_categorie'
    id = Column(Integer, primary_key=True)
    montant = Column(Integer, nullable=False)
    description = Column(String(), nullable=True)
    ecriture_id = Column(Integer, ForeignKey('ecriture.id'), nullable=False)
    categorie_id = Column(Integer, ForeignKey('categorie.id'), nullable=True)
    categorie = relationship('Categorie')

class EcritureTag(Base):
    """ Class to manage ecriture_tag table """
    __tablename__ = 'ecriture_tag'
    ecriture_id = Column(Integer, ForeignKey('ecriture.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tag.id'), primary_key=True)

class Tag(Base):
    """ Class to manage tag table """
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    nom = Column(String(), nullable=False)
    valeur = Column(String(), nullable=False)

