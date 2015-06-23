#!/usr/bin/python
# -*- coding: utf8 -*-
""" Application to create api to manage banque """

#import re

from json import dumps, loads
#from datetime import datetime

#from sqlalchemy import desc
from sqlalchemy.orm.exc import NoResultFound
#from sqlalchemy.exc import IntegrityError
#from sqlalchemy.sql import func

from compta.server.api.bottle import response, request, abort

from compta.db.banque import Banque
from compta.server.api.server import App

app = App().server

@app.get('/banque')
@app.get('/banque/<id:int>')
@app.get(r'/banque/<nom:re:[a-zA-Z\ ]+>')
def list_banque(db, id=None, nom=None):
    """ Display information for banque """
    banques = db.query(Banque)
    if id:
        banques = banques.filter(Banque.id == id)
    if nom:
        banques = banques.filter(Banque.nom == nom)
    try:
        banques = banques.order_by(Banque.nom).\
                          all()
    except NoResultFound:
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

@app.put(r'/banque/<id:int>')
def update_banque(db, id=None):
    """ Update information for a banque """
    if not id:
        abort(404, 'no id received')
    data = request.body.readline()
    if not data:
        abort(204, 'No data received')
    entity = {}
    try:
        entity = loads(data)
    except:
        print "erreur chargement json %s" % (data,)
        abort(404, 'Error on loading data')
    try:
        banque = db.query(Banque).\
                    filter(Banque.id == id).\
                    one()
    except NoResultFound:
        abort(404, "ID not found")
    if entity.has_key('nom'):
        banque.nom = entity["nom"]
    if entity.has_key('adresse'):
        banque.adresse = entity["adresse"]
    if entity.has_key('ville'):
        banque.ville = entity["ville"]
    if entity.has_key('cp'):
        banque.cp = entity["cp"]
    if entity.has_key('pays'):
        banque.pays = entity["pays"]
    if entity.has_key('cle'):
        banque.cle_controle = entity["cle"]
    if entity.has_key('code_banque'):
        banque.code_banque = entity["code_banque"]
    if entity.has_key('code_guichet'):
        banque.code_guichet = entity["code_guichet"]
    db.commit()

@app.post('/banque')
def insert_banque(db):
    """ Insert a new banque """
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
    banque = Banque(nom=entity["nom"],
                    adresse=entity["adresse"],
                    ville=entity["ville"],
                    cp=entity["cp"],
                    pays=entity["pays"],
                    cle_controle=entity["cle"],
                    code_banque=entity["code_banque"],
                    code_guichet=entity["code_guichet"])
    db.add(banque)
    db.commit()
    response.status = 201
    response.headers["Location"] = "/banque/%s" % (banque.id,)

@app.delete(r'/banque/<id:int>')
def delete_banque(db, id=None):
    """ Delete a banque """
    try:
        banque = db.query(Banque).\
                    filter(Banque.id == id).\
                    one()
    except NoResultFound:
        abort(404, "ID not found")
    db.delete(banque)
    db.commit()



