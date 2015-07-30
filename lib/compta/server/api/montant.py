#!/usr/bin/python
# -*- coding: utf8 -*-
""" Application to create api to manage montant """

#import re
import locale

from json import dumps, loads
#from datetime import datetime

#from sqlalchemy import desc
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
#from sqlalchemy.sql import func

from compta.server.api.bottle import response, request, abort

from compta.db.categorie import Categorie
from compta.db.ecriture import Montant

from compta.server.api.server import App

app = App().server

@app.get('/montant')
@app.get(r'/montant/<id:int>')
@app.get(r'/ecriture/<ecriture_id:int>/montant')
@app.get(r'/ecriture/<ecriture_id:int>/montant/<id:int>')
def list_montant(db, id=None, ecriture_id=None):
    """ List montant """
    filter = {}
    if id:
        filter['id'] = id
    elif ecriture_id:
        filter['ecriture_id'] = ecriture_id
    else:
        filter = App.get_filter(request.query.filter)

    sort = App.get_sort(request.query.sort)

    montants = db.query(Montant.id,
                        Montant.montant,
                        Montant.description,
                        Montant.categorie_id,
                        Montant.ecriture_id,
                        Categorie.nom.label("categorie_nom")
                       ).\
                    join(Categorie)
    if filter:
        for column, value in filter.iteritems():
            montants = montants.filter(getattr(Montant, column) == value)
    if sort:
        for column in sort:
            montants = montants.order_by(getattr(Montant, column))
    else:
        montants = montants.order_by(Montant.montant)
 
    try:
        montants = montants.all()
    except NoResultFound:
        abort(404, "ID not found")
    if not montants:
        abort(404, "ID not found")
    list_montants = []
    for montant in montants:
        list_montants.append({'id': montant.id,
                              'montant': "%0.2f" % (montant.montant/100.0,),
                              'description': montant.description,
                              'categorie_id': montant.categorie_id,
                              'categorie_nom': montant.categorie_nom,
                              'ecriture_id': montant.ecriture_id,
                             })
    return dumps(list_montants)

@app.post('/montant')
def insert_montant(db):
    """ Create a montant """
    entity = App.check_data(Montant, request.body.readline())
    if entity:
        montant = Montant()
        for column, value in entity.iteritems():
            if column == 'montant':
               montant.montant = int(locale.atof(entity["montant"])*100)
            else:
                setattr(montant, column, value)
        db.add(montant)
        try:
            db.commit()
        except IntegrityError as ex:
            abort(404, ex.args)
        response.status = 201
        response.headers["Location"] = "/montant/%s" % (montant.id,)

@app.put(r'/montant/<id:int>')
def update_montant(db, id):
    """ Update information for a montant """
    entity = App.check_data(Montant, request.body.readline())
    if entity:
        try:
            montant = db.query(Montant).\
                           filter(Montant.id == id).\
                           one()
        except NoResultFound:
            abort(404, "ID not found")
    for column, value in entity.iteritems():
        if column == 'montant':
           montant.montant = int(locale.atof(entity["montant"])*100)
        else:
            setattr(montant, column, value)
    try:
        db.commit()
    except IntegrityError as ex:
        abort(404, ex.args)

@app.delete(r'/montant/<id:int>')
def delete_tag(db, id=None):
    """ Delete a montant """
    try:
        montant = db.query(Montant).\
                    filter(Montant.id == id).\
                    one()
    except NoResultFound:
        abort(404, "ID not found")
    db.delete(montant)
    db.commit()


