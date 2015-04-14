#!/usr/bin/python
# -*- coding: utf8 -*-

from bottle import Bottle
from bottle import get, run, route, response
from json import dumps
from bottle import HTTPError
from bottle.ext import sqlalchemy
#from sqlalchemy import create_engine, Column, Integer, Sequence, String
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

from compta.db.banque import Banque
from compta.db.compte import Compte
from compta.db.ecriture import Ecriture, EcritureCategorie
from compta.db.categorie import Categorie
from compta.db.base import Base

app = Bottle()

def main():
    #Base = declarative_base()
    engine = create_engine('sqlite:///./db/compta.test', echo=True)

    plugin = sqlalchemy.Plugin(engine, Base.metadata, create=False)
    app.install(plugin)
    app.run(host='localhost', port=8080, debug=True)

@app.hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token' 

@app.get('/banque')
def show(db):
    banques = db.query(Banque).\
                 order_by(Banque.nom).\
                 all()
    list_banque = []
    for banque in banques:
        list_banque.append({'id': banque.id,
                            'nom': banque.nom,
                            'adresse': banque.adresse,
                            'ville': banque.ville,
                            'cp': banque.cp,
                            'pays': banque.pays,
                            'cle': banque.cle_controle,
                            'code_banque': banque.code_banque,
                            'code_guichet': banque.code_guichet})
    return dumps(list_banque)

@app.get('/banque/<nom>')
def show(db, nom=None):
    banque = db.query(Banque).\
                filter(Banque.nom.ilike("%%%s%%" % (nom,))).\
                first()
    return dumps({'id': banque.id, 'nom': banque.nom})

@app.get('/compte/<nom>')
def show(nom, db):
    compte = db.query(Compte).\
                filter(Compte.nom.ilike("%%%s%%" % (nom,))).\
                first()
    print compte
    if compte:
        return {'id': compte.id, 'nom': compte.nom}
    return HTTPError(404, 'Entity not found.')

if __name__ == "__main__":
    main()

