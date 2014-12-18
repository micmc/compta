from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from base import Base

#CREATE TABLE categorie("id" integer NOT NULL PRIMARY KEY, "nom" varchar(200) NOT NULL);

class Categorie(Base):
    __tablename__ = 'categorie'
    id = Column(Integer, primary_key=True)
    nom = Column(String(200), nullable=False)
