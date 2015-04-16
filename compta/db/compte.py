from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

from base import Base

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
    __tablename__ = 'compte'
    id = Column(Integer, primary_key=True)
    nom = Column(String(50), nullable=False)
    numero = Column(String(12), nullable=False)
    cle = Column(String(3), nullable=False)
    type = Column(String(3), nullable=False)
    archive = Column(Boolean, default=False)
    banque_id = Column(Integer, ForeignKey('banque.id'), nullable=False)
