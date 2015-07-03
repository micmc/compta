#!/usr/bin/python
# -*- coding: utf8 -*-
""" Application to create api to manage banque """

#import re

from json import dumps, loads
#from datetime import datetime

#from sqlalchemy import desc
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
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
    filter = {}
    if id:
        filter['id'] = id
    elif nom:
        filter['nom'] = nom
    else:
        filter = App.get_filter(request.query.filter)

    sort = App.get_sort(request.query.sort)

    banques = db.query(Banque)
    
    if filter:
        for column, value in filter.iteritems():
            banques = banques.filter(getattr(Banque, column) == value)
    if sort:
        for column in sort:
            banques = banques.order_by(getattr(Banque, column))
    else:
        banques = banques.order_by(Banque.nom)
    try:
        banques = banques.all()
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
                            'code_guichet': banque.code_guichet
                           }
                          )
    return dumps(list_banque)

@app.post('/banque')
def insert_banque(db):
    """ Create a banque """
    entity = App.check_data(Banque, request.body.readline())
    if entity:
        banque = Banque()
        for column, value in entity.iteritems():
            setattr(banque, column, value)
        db.add(banque)
        try:
            db.commit()
        except IntegrityError as ex:
            abort(404, ex.args)
        response.status = 201
        response.headers["Location"] = "/banque/%s" % (banque.id,)

@app.put(r'/banque/<id:int>')
def update_banque(db, id=None):
    """ Update information for a banque """
    entity = App.check_data(Banque, request.body.readline())
    if entity:
        try:
            banque = db.query(Banque).\
                           filter(Banque.id == id).\
                           one()
        except NoResultFound:
            abort(404, "ID not found")
    for column, value in entity.iteritems():
        setattr(banque, column, value)
    try:
        db.commit()
    except IntegrityError as ex:
        abort(404, ex.args)

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



