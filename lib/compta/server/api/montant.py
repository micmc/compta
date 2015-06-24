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
    """ List categorie """
    montants = db.query(Montant.id,
                        Montant.montant,
                        Montant.description,
                        Montant.categorie_id,
                        Montant.ecriture_id,
                        Categorie.nom.label("categorie_nom")
                       ).\
                    join(Categorie).\
                    group_by(Montant.id)
    if id:
        montants = montants.filter(Montant.id == id)
    if ecriture_id:
        montants = montants.filter(Montant.ecriture_id == ecriture_id)

    try:
        montants = montants.all()
    except NoResultFound:
        abort(404, "ID not found")
    if not montants:
        abort(404, "ID not found")
    list_montants = []
    for montant in montants:
        print montant
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
    """ Insert a new montant """
    data = request.body.readline()
    if not data:
        abort(204, 'No data received')
    entity = loads(data)
    print entity
    if not entity.has_key('montant'):
        abort(404, 'Nom : non spécifié')
    if not entity.has_key('categorie_id'):
        abort(404, 'Categorie (id) : non spécifié')
    if not entity.has_key('ecriture_id'):
        abort(404, 'Ecriture (id) : non spécifié')
    montant = Montant(montant=(locale.atof(entity['montant'])*100),
                      categorie_id=entity['categorie_id'],
                      ecriture_id=entity['ecriture_id']
                     )
    if entity.has_key('description'):
        montant['description'] = entity['description']
    db.add(montant)
    try:
        db.commit()
    except IntegrityError:
        abort(404, 'Integrity Error')
    response.status = 201
    response.headers["Montant"] = "/montant/%s" % (montant.id,)


