#!/usr/bin/python
# -*- coding: utf8 -*-

from bottle import Bottle
from bottle import get, run, route, response, request, abort
from json import dumps, loads
from bottle import HTTPError
from bottle.ext import sqlalchemy
#from sqlalchemy import create_engine, Column, Integer, Sequence, String
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm.exc import NoResultFound

from compta.db.banque import Banque
from compta.db.compte import Compte
from compta.db.ecriture import Ecriture, EcritureCategorie
from compta.db.categorie import Categorie
from compta.db.base import Base

app = Bottle()

def main():
    #Base = declarative_base()
    engine = create_engine('sqlite:///./db/compta.test', echo=False)

    plugin = sqlalchemy.Plugin(engine, Base.metadata, create=False)
    app.install(plugin)
    app.run(host='localhost', port=8080, debug=True)

@app.hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token' 

@app.get('/banque')
@app.get('/banque/<id:int>')
@app.get('/banque/<nom:re:[a-zA-Z\ ]+>')
def show(db, id=None, nom=None):
    banques = db.query(Banque)
    if id:
        banques = banques.filter(Banque.id == id)
    if nom:
        banques = banques.filter(Banque.nom == nom)
    try:
        banques = banques.order_by(Banque.nom).\
                          all()
    except NoResultFound :
        abort(404, "ID not found")
    if not banques:
        abort(404, "ID not found")
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

@app.put('/banque/<id>')
def update_banque(db, id=None):
    dir(app)
    if not id:
        abort(404, 'no id received')
    data = request.body.readline()
    if not data:
        abort(204, 'No data received')
    entity = loads(data)
    if not entity.has_key('nom'):
        abort(404, 'Nom : non spécifié')
    if not entity.has_key('adresse'):
        abort(404, 'Adresse : non spécifié')
    if not entity.has_key('ville'):
        abort(404, 'Ville : non spécifié')
    if not entity.has_key('cp'):
        abort(404, 'Code Postal : non spécifié')
    if not entity.has_key('pays'):
        entity['pays'] = 'FR'
    if not entity.has_key('cle'):
        entity['cle'] = '76'
    if not entity.has_key('code_banque'):
        entity['code_banque'] = ""
    if not entity.has_key('code_guichet'):
        entity['code_guichet'] = ""
    banque = db.query(Banque).\
                filter(Banque.id == id).\
                one()
    banque.nom = entity["nom"]
    banque.adresse = entity["adresse"]
    banque.ville = entity["ville"]
    banque.cp = entity["cp"]
    banque.pays = entity["pays"]
    banque.cle_controle = entity["cle"]
    banque.code_banque = entity["code_banque"]
    banque.code_guichet = entity["code_guichet"]
    db.commit()

#@app.get('/banque/<nom>')
#def show(db, nom=None):
#    banque = db.query(Banque).\
#                filter(Banque.nom.ilike("%%%s%%" % (nom,))).\
#                first()
#    return dumps({'id': banque.id, 'nom': banque.nom})

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

