#!/usr/bin/python
# -*- coding: utf8 -*-
""" Application to create api to manage banque """

import re

from json import dumps, loads
from datetime import datetime

from sqlalchemy import desc
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func

from compta.server.bottle import response, request, abort

from compta.db.categorie import Categorie

from compta.server.api.server import App

app = App().server

@app.get('/categorie')
@app.get(r'/categorie/<id:int>')
@app.get(r'/categorie/<nom:re:[a-zA-Z\ ]+>')
def list_categorie(db, id=None, nom=None, id_compte=None):
    """ List categorie """
    sort = request.query.sort
    categories = db.query(Categorie.id, Categorie.nom, func.count(Categorie.nom).label("count")).\
                    join(EcritureCategorie).\
                    group_by(Categorie.nom)
    if nom:
        categories = categories.filter(Categorie.nom == nom)
    if id:
        categories = categories.filter(Categorie.id == id)
    for lst_sort in sort.split(','):
        if sort == "id":
            categories = categories.order_by(Categorie.id)
        elif sort == "count":
            categories = categories.order_by(desc('count'))
    categories = categories.order_by(Categorie.nom)
    try:
        categories = categories.all()
    except NoResultFound:
        abort(404, "ID not found")
    if not categories:
        abort(404, "ID not found")
    list_categories = []
    for categorie in categories:
        list_categories.append({'id': categorie.id,
                                'nom': categorie.nom,
                                'count': categorie.count,
                               })
    return dumps(list_categories)

@app.post('/categorie')
def insert_categorie(db):
    """ Insert a new categorie """
    data = request.body.readline()
    if not data:
        abort(204, 'No data received')
    entity = loads(data)
    if not entity.has_key('nom'):
        abort(404, 'Nom : non spécifié')
    categorie = Categorie(nom=entity["nom"])
    db.add(categorie)
    try:
        db.commit()
    except IntegrityError:
        abort(404, 'Integrity Error')
    response.status = 201
    response.headers["Location"] = "/categorie/%s" % (categorie.id,)

