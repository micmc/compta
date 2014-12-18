#!/usr/bin/python
# -*- coding: utf8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from compta.db.banque import Banque
from compta.db.compte import Compte

engine = create_engine('sqlite:///compta.db')

#Base = declarative_base()
#Base.metadata.bind = engine
#Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()


banque = session.query(Banque).all()
for titi in banque:
    print titi.nom
    print titi.compte
