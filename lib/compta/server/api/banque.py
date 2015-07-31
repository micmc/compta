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
            if not isinstance(value, list):
                banques = banques.filter(getattr(Banque, column) == value)
            else:
                banques = banques.filter(getattr(Banque, column).in_(value))
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
    list_banques = []
    attributs = App.get_attribut(request.query.attribut)
    if attributs:
        for banque in banques:
            dict_attributs = {}
            for attribut in attributs:
                dict_attributs[attribut] = getattr(banque, attribut)
            list_banques.append(dict_attributs)
    else:
        for banque in banques:
            list_banques.append({'id': banque.id,
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
    return dumps(list_banques)

@app.post('/jtable/ListBanque')
def list_banque_jtable(db):
    json_list = list_banque(db)
    data_list = loads(json_list)
    data = {
            "Result": "OK",
            "Records": data_list
           }
    return dumps(data)

@app.post('/jtable/GetBanqueName')
def list_banque_jtable(db):
    json_list = list_banque(db)
    data_list = loads(json_list)
    data_new = []
    for data in data_list:
        data_dict = {'DisplayText': data['nom'],
                     'Value': data['id']
                    }
        data_new.append(data_dict)
    data = {
            "Result": "OK",
            "Options": data_new
           }
    return dumps(data)


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

@app.post('/jtable/CreateBanque')
def insert_banque_jtable(db):
    """ Create a banque with jtable"""
    entity = App.check_forms(Banque, request.forms)
    if entity:
        banque = Banque()
        for column, value in entity.iteritems():
            setattr(banque, column, value)
        db.add(banque)
        try:
            db.commit()
        except IntegrityError as ex:
            data = {
                    "Result": "ERROR",
                    "Message": "Erreur d'intégrité"
                   }
            return dumps(data)
        data_list = {
                     'id': banque.id,
                     'nom': banque.nom,
                     'adresse': banque.adresse,
                     'ville': banque.ville,
                     'cp': banque.cp,
                     #'pays': banque.pays,
                     #'cle': banque.cle_controle,
                     'code_banque': banque.code_banque,
                     'code_guichet': banque.code_guichet
                    }

        data = {
                "Result": "OK",
                "Record" : data_list
               }
        return dumps(data)

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

@app.post('/jtable/UpdateBanque')
def update_banque_jtable(db):
    """ Update information for a banque with jtable"""
    entity = App.check_forms(Banque, request.forms)
    if entity:
        try:
            banque = db.query(Banque).\
                           filter(Banque.id == entity['id']).\
                           one()
        except NoResultFound:
            data = {
                    "Result": "ERROR",
                    "Message": "Pes de resultat"
                   }
            return dumps(data)
    for column, value in entity.iteritems():
        setattr(banque, column, value)
    try:
        db.commit()
    except IntegrityError as ex:
        data = {
                "Result": "ERROR",
                "Message": "Erreur d'intégrité"
               }
        return dumps(data)
    data = {
            "Result": "OK",
           }
    return dumps(data)



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

@app.post('/jtable/DeleteBanque')
def delete_banque_jtable(db):
    """ Delete a banque with jtable"""
    entity = App.check_forms(Banque, request.forms)
    try:
        banque = db.query(Banque).\
                    filter(Banque.id == entity['id']).\
                    one()
    except NoResultFound:
        data = {
                "Result": "ERROR",
                "Message": "Pes de resultat"
               }
        return dumps(data)
    db.delete(banque)
    db.commit()
    data = {
            "Result": "OK",
           }
    return dumps(data)



