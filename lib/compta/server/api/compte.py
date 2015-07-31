#!/usr/bin/python
# -*- coding: utf8 -*-
""" Application to create server for compta """

from compta.server.api.bottle import response, request, abort
from json import dumps, loads

#from sqlalchemy import desc
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
#from sqlalchemy.sql import func

#from compta.db.base import Base
from compta.db.compte import Compte
from compta.db.compte import Compte

from compta.server.api.server import App

app = App().server

@app.get('/compte')
@app.get(r'/compte/<id:int>')
@app.get(r'/compte/<nom:re:[a-zA-Z\ ]+>')
@app.get(r'/banque/<banque_id:int>/compte')
@app.get(r'/banque/<banque_id:int>/compte/<id:int>')
@app.get('/banque/<banque_id:int>/compte/<nom:re:[a-zA-Z\ ]+>')
def list_compte(db, id=None, nom=None, banque_id=None):
    """ List compte """

    filter = {}
    if id:
        filter['id'] = id
    elif nom:
        filter['nom'] = nom
    elif banque_id:
        filter['banque_id'] = banque_id
    else:
        filter = App.get_filter(request.query.filter)

    sort = App.get_sort(request.query.sort)

    comptes = db.query(Compte)

    if filter:
        for column, value in filter.iteritems():
            if not isinstance(value, list):
                comptes = comptes.filter(getattr(Compte, column) == value)
            else:
                comptes = comptes.filter(getattr(Compte, column).in_(value))
    if sort:
        for column in sort:
            comptes = comptes.order_by(getattr(Compte, column))
    else:
        comptes = comptes.order_by(Compte.nom)

    try:
        comptes = comptes.all()
    except NoResultFound:
        abort(404, "ID not found")
    if not comptes:
        abort(404, "ID not found")
    list_comptes = []
    attributs = App.get_attribut(request.query.attribut)
    if attributs:
        for compte in comptes:
            dict_attributs = {}
            for attribut in attributs:
                dict_attributs[attribut] = getattr(compte, attribut)
            list_comptes.append(dict_attributs)
    else:
        for compte in comptes:
            list_comptes.append({'id': compte.id,
                                 'nom': compte.nom,
                                 'numero': compte.numero,
                                 'cle': compte.cle,
                                 'type': compte.type,
                                 'archive': compte.archive,
                                 'banque_id': compte.banque_id,
                                })
    return dumps(list_comptes)

@app.post('/jtable/ListCompte')
def list_compte_jtable(db):
    json_list = list_compte(db)
    data_list = loads(json_list)
    data = {
            "Result": "OK",
            "Records": data_list
           }
    return dumps(data)

@app.post('/compte')
def insert_compte(db):
    """ Create a  compte """
    entity = App.check_data(Compte, request.body.readline())
    if entity:
        compte = Compte()
        for column, value in entity.iteritems():
            setattr(compte, column, value)
        db.add(compte)
        try:
            db.commit()
        except IntegrityError as ex:
            abort(404, ex.args)
        response.status = 201
        response.headers["Location"] = "/compte/%s" % (compte.id,)

@app.put(r'/compte/<id:int>')
def update_compte(db, id=None):
    """ Update information for a compte """
    entity = App.check_data(Compte, request.body.readline())
    if entity:
        try:
            compte = db.query(Compte).\
                           filter(Compte.id == id).\
                           one()
        except NoResultFound:
            abort(404, "ID not found")
    for column, value in entity.iteritems():
        setattr(compte, column, value)
    try:
        db.commit()
    except IntegrityError as ex:
        abort(404, ex.args)

@app.delete(r'/compte/<id:int>')
def delete_compte(db, id=None):
    """ Delete a compte """
    try:
        compte = db.query(Compte).\
                    filter(Compte.id == id).\
                    one()
    except NoResultFound:
        abort(404, "ID not found")
    db.delete(compte)
    db.commit()


