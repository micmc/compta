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

from compta.db.ecriture import Tag, Ecriture, EcritureTag

from compta.server.api.server import App

app = App().server

@app.get('/tag')
@app.get(r'/tag/<id:int>')
@app.get(r'/tag/<nom:re:[a-zA-Z\ ]+>')
def list_tag(db, id=None, nom=None):
    """ List tag """
    filter = {}
    if id:
        filter['id'] = id
    elif nom:
        filter['nom'] = nom
    else:
        filter = App.get_filter(request.query.filter)

    sort = App.get_sort(request.query.sort)

    tags = db.query(Tag.id,
                    Tag.nom,
                    Tag.valeur,
                   )
    if filter:
        for column, value in filter.iteritems():
            if not isinstance(value, list):
                tags = tags.filter(getattr(Tag, column) == value)
            else:
                tags = tags.filter(getattr(Tag, column).in_(value))
    if sort:
        for column in sort:
            tags = tags.order_by(getattr(Tag, column))
    else:
        tags = tags.order_by(Tag.nom)
    try:
        tags = tags.all()
    except NoResultFound:
        abort(404, "ID not found")
    if not tags:
        abort(404, "ID not found")

    list_tags = []
    attributs = App.get_attribut(request.query.attribut)
    if attributs:
        for tag in tags:
            dict_attributs = {}
            for attribut in attributs:
                dict_attributs[attribut] = getattr(tag, attribut)
            list_tags.append(dict_attributs)
    else:
        for tag in tags:
            list_tags.append({'id': tag.id,
                              'nom': tag.nom,
                              'valeur': tag.valeur,
                             }
                            )
    return dumps(list_tags)

@app.get(r'/ecriture/<ecriture_id:int>/tag')
def list_ecriture_tag(db, ecriture_id=None):
    """ List ecriture for tag """
    filter = {}
    filter = App.get_filter(request.query.filter)

    sort = App.get_sort(request.query.sort)

    tags = db.query(EcritureTag.id,
                    Tag.nom,
                    Tag.valeur,
                    EcritureTag.ecriture_id,
                    EcritureTag.tag_id
                   ).\
              select_from(Tag).\
              join(EcritureTag).\
              filter(EcritureTag.ecriture_id == ecriture_id)

    if filter:
        for column, value in filter.iteritems():
            if not isinstance(value, list):
                tags = tags.filter(getattr(Tag, column) == value)
            else:
                tags = tags.filter(getattr(Tag, column).in_(value))
    if sort:
        for column in sort:
            tags = tags.order_by(getattr(Tag, column))
    else:
        tags = tags.order_by(Tag.nom)
    try:
        tags = tags.all()
    except NoResultFound:
        abort(404, "ID not found")
    if not tags:
        response.status = 204
        return "ID not found"

    list_tags = []
    attributs = App.get_attribut(request.query.attribut)
    if attributs:
        for tag in tags:
            dict_attributs = {}
            for attribut in attributs:
                dict_attributs[attribut] = getattr(tag, attribut)
            list_tags.append(dict_attributs)
    else:
        for tag in tags:
            list_tags.append({'id': tag.tag_id,
                              'tag_id': tag.id,
                              'ecriture_id' : tag.ecriture_id,
                              'nom': tag.nom,
                              'valeur': tag.valeur,
                             }
                            )
    return dumps(list_tags)


@app.post('/tag')
def insert_tag(db):
    """ Insert a new tag """
    entity = App.check_data(Tag, request.body.readline())
    if entity:
        tag = Tag()
        for column, value in entity.iteritems():
            setattr(tag, column, value)
        db.add(tag)
        try:
            db.commit()
        except IntegrityError as ex:
            abort(404, ex.args)
        response.status = 201
        response.headers["Tag"] = "/tag/%s" % (tag.id,)
        tag = loads(list_tag(db, tag.id))
        return tag[0]

@app.post(r'/ecriture/<ecriture_id:int>/tag')
def insert_ecriture_tag(db, ecriture_id):
    """ Insert a new ecriture_tag for an existing ecriture """
    entity = App.check_data(EcritureTag, request.body.readline())
    if entity:
        ecriture_tag = EcritureTag(ecriture_id=ecriture_id, tag_id=entity['tag_id'])
        db.add(ecriture_tag)
        try:
            db.commit()
        except IntegrityError as ex:
            abort(404, ex.args)
        response.status = 201
        response.headers["Tag"] = "/tag/%s" % (ecriture_tag.id,)
        ecriture_tag = {'id': ecriture_tag.id,
                        'tag_id': ecriture_tag.tag_id,
                        'ecriture_id': ecriture_tag.ecriture_id
                       }
        return ecriture_tag

@app.put(r'/tag/<id:int>')
def update_tag(db, id):
    """ Update information for a tag """
    entity = App.check_data(Tag, request.body.readline())
    if entity:
        try:
            tag = db.query(Tag).\
                           filter(Tag.id == id).\
                           one()
        except NoResultFound:
            abort(404, "ID not found")
    for column, value in entity.iteritems():
        setattr(tag, column, value)
    try:
        db.commit()
        tag = loads(list_tag(db, tag.id))
        return tag[0]
    except IntegrityError as ex:
        abort(404, ex.args)

@app.delete(r'/tag/<id:int>')
def delete_tag(db, id=None):
    """ Delete a ecriture_tag for an ecriture"""
    try:
        tag = db.query(Tag).\
                    filter(Tag.id == id).\
                    one()
    except NoResultFound:
        abort(404, "ID not found")
    db.delete(tag)
    db.commit()
    return dumps({'id': id})

@app.delete(r'/ecriture/<ecriture_id:int>/tag/<id:int>')
def delete_tag(db, id=None, ecriture_id=None):
    """ Delete a tag """
    try:
        ecriture_tag = db.query(EcritureTag).\
                          filter(EcritureTag.id == id).\
                          one()
    except NoResultFound:
        abort(404, "ID not found")
    db.delete(ecriture_tag)
    db.commit()
    return dumps({'id': id,})


