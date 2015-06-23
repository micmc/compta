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
from compta.db.banque import Banque
from compta.db.compte import Compte

from compta.server.api.server import App

app = App().server

@app.get('/compte')
@app.get(r'/compte/<id_compte:int>')
@app.get(r'/compte/<nom:re:[a-zA-Z\ ]+>')
@app.get(r'/banque/<id:int>/compte')
@app.get(r'/banque/<id:int>/compte/<id_compte:int>')
@app.get('/banque/<id:int>/compte/<nom:re:[a-zA-Z\ ]+>')
def list_compte(db, id=None, nom=None, id_compte=None):
    """ List compte 
        filter to use :
        filter = ['dif', 'div', 'prs', 'prv', 'vir']
        archive = yes / no : print archive or not archive
    """
 
    filter = request.query.filter
    archive = request.query.archive

    comptes = db.query(Compte)
    if id:
        comptes = comptes.join(Compte.banque).\
                          filter(Banque.id == id)
    if nom:
        comptes = comptes.filter(Compte.nom == nom)
    if id_compte:
        comptes = comptes.filter(Compte.id == id_compte)

    if filter:
        type_compte = ['dif', 'div', 'prs', 'prv', 'vir']
        if filter in type_compte:
            comptes = comptes.filter(Compte.type == filter)
        else:
            abort(404, "filter not found")

    if archive == "yes":
        comptes = comptes.filter(Compte.archive == True)
    elif archive == "no":
        comptes = comptes.filter(Compte.archive == False)

    try:
        comptes = comptes.order_by(Compte.nom).\
                          all()
    except NoResultFound:
        abort(404, "ID not found")
    if not comptes:
        abort(404, "ID not found")
    list_comptes = []
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

@app.put(r'/compte/<id:int>')
def update_compte(db, id=None):
    """ Update information for a compte """
    if not id:
        abort(404, 'no id received')
    data = request.body.readline()
    if not data:
        abort(204, 'No data received')
    entity = {}
    try:
        entity = loads(data)
    except:
        print "erreur chargement json %s" % (data,)
        abort(404, 'Error on loading data')
    try:
        compte = db.query(Compte).\
                    filter(Compte.id == id).\
                    one()
    except NoResultFound:
        abort(404, "ID not found")
    if entity.has_key('nom'):
        compte.nom = entity["nom"]
    if entity.has_key('numero'):
        compte.numero = entity["numero"]
    if entity.has_key('cle'):
        compte.cle = entity["cle"]
    if entity.has_key('type'):
        compte.type = entity["type"]
    if entity.has_key('archive'):
        if entity["archive"].isnumeric():
            compte.archive = entity["archive"]
        elif entity["archive"].lower() == "true":
            compte.archive = True
        else:
            compte.archive = False
    try:
        db.commit()
    except IntegrityError:
        abort(404, 'Integrity Error')


@app.post('/compte')
def insert_compte(db):
    """ Insert a new compte """
    data = request.body.readline()
    if not data:
        abort(204, 'No data received')
    entity = loads(data)
    if not entity.has_key('nom'):
        abort(404, 'Nom : non spécifié')
    if not entity.has_key('numero'):
        abort(404, 'numero : non spécifié')
    if not entity.has_key('cle'):
        abort(404, 'cle : non spécifié')
    if not entity.has_key('type'):
        abort(404, 'Type : non spécifié')
    if not entity.has_key('banque_id'):
        abort(404, 'banque_id : non spécifié')
    compte = Compte(nom=entity["nom"],
                    numero=entity["numero"],
                    cle=entity["cle"],
                    type=entity["type"],
                    banque_id=entity["banque_id"])
    if entity.has_key('archive'):
        if entity["archive"].isnumeric():
            compte.archive = entity["archive"]
        elif entity["archive"].lower() == "true":
            compte.archive = True
        else:
            compte.archive = False
    db.add(compte)
    try:
        db.commit()
    except IntegrityError:
        abort(404, 'Integrity Error')
    response.status = 201
    response.headers["Location"] = "/compte/%s" % (compte.id,)

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


