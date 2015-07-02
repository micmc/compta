#!/usr/bin/python
# -*- coding: utf8 -*-
""" Application to create api to manage banque """

import re
import locale

from json import dumps, loads
from datetime import datetime

from sqlalchemy import desc
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func

from compta.server.api.bottle import response, request, abort

from compta.db.banque import Banque
from compta.db.compte import Compte
from compta.db.ecriture import Ecriture, Montant, Tag, EcritureTag
from compta.db.categorie import Categorie

from compta.server.api.server import App

app = App().server

@app.get('/ecriture')
@app.get(r'/ecriture/<id:int>')
@app.get(r'/ecriture/<nom:re:[a-zA-Z\ ]+>')
@app.get(r'/compte/<compte_id:int>/ecriture')
@app.get(r'/compte/<compte_id:int>/ecriture/<id:int>')
@app.get(r'/compte/<compte_id:int>/ecriture/<nom:re:[a-zA-Z\ ]+>')
@app.get(r'/compte/<compte_id:int>/ecriture/<sum:re:sum>')
def list_ecriture(db, id=None, nom=None, compte_id=None, sum=None):
    """ List compte
        Filter to use :
        filter = [1-9]+ / sum : give number or sum
        sort = field1,[field2,...] : sort by field
        field = field1,[field2,...] : field to return
        page = [1-9]+ / first / last : print by page
        valide = yes / no : print valide or not valide
    """

    # return sums of account
    if sum:
        ecritures = db.query(func.count(Ecriture.nom).label("nombre"),
                             (func.sum(Ecriture.dc * Montant.montant)/100.0).label("somme")
                            ).\
                       join(Ecriture.montant).\
                       filter(Ecriture.compte_id == compte_id).\
                       one()
        return dumps({'somme': "%0.2f" % ecritures.somme,
                      'nombre': "%d" % ecritures.nombre,
                     }
                    )
    # continue
    filter = {}
    if id:
        filter['id'] = id
    elif nom:
        filter['nom'] = nom
    elif compte_id:
        filter['compte_id'] = compte_id
    else:
        filter = App.get_filter(request.query.filter)

    sort = App.get_sort(request.query.sort)

    ecritures = db.query(Ecriture.id.label("id"),
                         func.trim(Ecriture.nom).label("nom"),
                         Ecriture.date.label("date"),
                         (Montant.montant * Ecriture.dc).label("montant"),
                         Ecriture.type.label("type"),
                         Categorie.nom.label("categorie"),
                         Montant.description.label("description"),
                         Montant.id.label("montant_id"),
                         Ecriture.valide.label("valide"),
                        ).\
                   join(Ecriture.montant).\
                   join(Montant.categorie)


    if filter:
        for column, value in filter.iteritems():
            ecritures = ecritures.filter(getattr(Ecriture, column) == value)
    if sort:
        for column in sort:
            ecritures = ecritures.order_by(getattr(Ecriture, column))
    else:
        ecritures = ecritures.order_by(desc(Ecriture.date))
    try:
        ecritures = ecritures.all()
        #if re.match(r"^\d+$", filter):
        #    ecritures = ecritures[:int(filter):]
    except NoResultFound:
        abort(404, "ID not found")
    if not ecritures:
        abort(404, "ID not found")
    list_ecritures = []
    for ecriture in ecritures:
        list_ecritures.append({'id': ecriture.id,
                               'nom': ecriture.nom,
                               'date': datetime.strftime(ecriture.date, "%Y/%m/%d"),
                               #'dc': ecriture.Ecriture.dc,
                               'type': ecriture.type,
                               'valide': ecriture.valide,
                               'categorie': ecriture.categorie,
                               'montant': "%0.2f" % (ecriture.montant/100.0,),
                               'description': ecriture.description,
                               'montant_id' : ecriture.montant_id,
                              })
    return dumps(list_ecritures)

@app.post('/ecriture')
def insert_ecriture(db):
    """ Create an ecriture """
    entity = App.check_data(Ecriture, request.body.readline())
    if entity:
        ecriture = Ecriture()
    for column, value in entity.iteritems():
        setattr(ecriture, column, value)
    db.add(ecriture)
    try:
        db.commit()
    except IntegrityError as ex:
        abort(404, ex.args)
    response.status = 201
    response.headers["Location"] = "/ecriture/%s/" % (ecriture.id,)


@app.put(r'/ecriture/<id:int>')
def update_ecriture(db, id=None, ec_id=None):
    """ Update information for an ecriture """
    entity = App.check_data(Ecriture, request.body.readline())
    if entity:
        try:
            ecriture = db.query(Ecriture).\
                           filter(Ecriture.id == id).\
                           one()
        except NoResultFound:
            abort(404, "ID not found")
    for column, value in entity.iteritems():
        setattr(ecriture, column, value)
    try:
        db.commit()
    except IntegrityError as ex:
        abort(404, ex.args)

@app.delete(r'/ecriture/<id:int>')
def delete_ecriture(db, id=None):
    """ Delete an ecriture """
    try:
        ecriture = db.query(Ecriture).\
                    filter(Ecriture.id == id).\
                    one()
    except NoResultFound:
        abort(404, "ID not found")
    db.delete(ecriture)
    db.commit()
