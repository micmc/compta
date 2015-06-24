#!/usr/bin/python
# -*- coding: utf8 -*-
""" Application to create api to manage tag """

#import re
import locale

from json import dumps, loads
#from datetime import datetime

#from sqlalchemy import desc
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
#from sqlalchemy.sql import func

from compta.server.api.bottle import response, request, abort

from compta.db.ecriture import Tag, Ecriture

from compta.server.api.server import App

app = App().server

@app.get('/tag')
@app.get(r'/tag/<id:int>')
@app.get(r'/ecriture/<ecriture_id:int>/tag')
@app.get(r'/ecriture/<ecriture_id:int>/tag/<id:int>')
def list_tag(db, id=None, ecriture_id=None):
    """ List categorie """
    tags = db.query(Tag.id,
                    Tag.nom,
                    Tag.valeur,
                   )
    if id:
        tags = tags.filter(Tag.id == id)
    if ecriture_id:
        tags = tags.join(Ecriture.tags).\
                    filter(Ecriture.id == ecriture_id)

    try:
        tags = tags.all()
    except NoResultFound:
        abort(404, "ID not found")
    if not tags:
        abort(404, "ID not found")
    list_tags = []
    for tag in tags:
        print tag
        list_tags.append({'id': tag.id,
                          'nom': tag.nom,
                          'valeur': tag.valeur,
                         }
                        )
    return dumps(list_tags)

@app.post('/tag')
def insert_tag(db):
    """ Insert a new tag """
    data = request.body.readline()
    if not data:
        abort(204, 'No data received')
    entity = loads(data)
    print entity
    if not entity.has_key('nom'):
        abort(404, 'Nom : non spécifié')
    if not entity.has_key('valeur'):
        abort(404, 'Valeur : non spécifié')
    tag = Tag(nom=entity['nom'],
              valeur=entity['valeur'],
             )
    db.add(tag)
    try:
        db.commit()
    except IntegrityError:
        abort(404, 'Integrity Error')
    response.status = 201
    response.headers["Tag"] = "/tag/%s" % (tag.id,)


