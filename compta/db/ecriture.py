from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

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
    __tablename__ = 'ecriture'
    id = Column(Integer, primary_key=True)
    date_ecriture = Column('date', Date, nullable=False)
    dc = Column(Integer, nullable=False)
    type_ecriture = Column('type', String(2), nullable=False)
    nom = Column(String(200), nullable=False)
    valide = Column(Boolean)
    compte_id = Column(Integer, ForeignKey('compte.id'), nullable=False)
    categories = relationship('EcritureCategorie')

class EcritureCategorie(Base):
    __tablename__ = 'ecriture_categorie'
    id = Column(Integer, primary_key=True)
    categorie = Column(String(200), nullable=False)
    description = Column(String(), nullable=False)
    montant = Column(Float(asdecimal=True), nullable=False)
    ecriture_id = Column(Integer, ForeignKey('ecriture.id'), nullable=False)
    categorie_id = Column(Integer, ForeignKey('categorie.id'), nullable=False)

