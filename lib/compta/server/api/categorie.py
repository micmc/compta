#!/usr/bin/python
# -*- coding: utf8 -*-
""" Application to create api to manage banque """

#import re

from json import dumps, loads
#from datetime import datetime

from sqlalchemy import desc
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func

from compta.server.api.bottle import response, request, abort

from compta.db.categorie import Categorie
from compta.db.ecriture import Montant

from compta.server.api.server import App

app = App().server

@app.get('/categorie')
@app.get(r'/categorie/<id:int>')
@app.get(r'/categorie/<nom:re:[a-zA-Z\ ]+>')
def list_categorie(db, id=None, nom=None):
    """ List categorie """
    filter = {}
    if id:
        filter['id']=id
    elif nom:
        filter['nim']=nom
    else:
        filter = App.get_filter(request.query.filter)

    sort = App.get_sort(request.query.sort)

    categories = db.query(Categorie.id, Categorie.nom, func.count(Categorie.nom).label("count")).\
                    outerjoin(Montant).\
                    group_by(Categorie.nom)
    if filter:
        for column, value in filter.iteritems():
            categories = categories.filter(getattr(Categorie, column) == value)
    if sort:
        for column in sort:
            categories = categories.order_by(getattr(Categorie, column))
    else:
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
    """ Create a categorie """
    entity = App.check_data(Categorie, request.body.readline())
    if entity:
        categorie = Categorie()
    for column, value in entity.iteritems():
        setattr(categorie, column, value)
    db.add(categorie)
    try:
        db.commit()
    except IntegrityError:
        abort(404, 'Integrity Error')
    response.status = 201
    response.headers["Location"] = "/categorie/%s" % (categorie.id,)

@app.put(r'/categorie/<id:int>')
def update_categorie(db, id):
    """ Update information for an ecriture """
    entity = App.check_data(Categorie, request.body.readline())
    if entity:
        try:
            categorie = db.query(Categorie).\
                           filter(Categorie.id == id).\
                           one()
        except NoResultFound:
            abort(404, "ID not found")
    print dir(categorie), type(categorie)
    for column, value in entity.iteritems():
        setattr(categorie, column, value)
    try:
        db.commit()
        print Categorie
    except IntegrityError:
        abort(404, 'Integrity Error')


