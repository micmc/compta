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
from compta.db.ecriture import Ecriture, Montant
from compta.db.categorie import Categorie

from compta.server.api.server import App

app = App().server

@app.get('/ecriture')
@app.get(r'/ecriture/<id:int>')
@app.get(r'/ecriture/<nom:re:[a-zA-Z\ ]+>')
@app.get(r'/compte/<id_compte:int>/ecriture')
@app.get(r'/compte/<id_compte:int>/ecriture/<id:int>')
@app.get(r'/compte/<id_compte:int>/ecriture/<nom:re:[a-zA-Z\ ]+>')
def list_ecriture(db, id=None, nom=None, id_compte=None):
    """ List compte
        Filter to use :
        filter = [1-9]+ / sum : give number or sum
        sort = field1,[field2,...] : sort by field
        field = field1,[field2,...] : field to return
        page = [1-9]+ / first / last : print by page
        valide = yes / no : print valide or not valide
    """

    filter = request.query.filter
    valide = request.query.valide
    sort = request.query.sort
    field = request.query.field
    page = request.query.page

    ecritures = db.query(Ecriture.id.label("id"),
                         func.trim(Ecriture.nom).label("nom"),
                         Ecriture.date.label("date"),
                         (Montant.montant * Ecriture.dc).label("montant"),
                         Ecriture.type.label("type"),
                         Categorie.nom.label("categorie"),
                         Montant.description.label("description"),
                         Montant.id.label("ecriture_categorie_id"),
                         Ecriture.valide.label("valide"),
                        ).\
                   join(Ecriture.montant).\
                   join(Montant.categorie)
    if id_compte:
        ecritures = ecritures.filter(Ecriture.compte_id == id_compte)
    if nom:
        ecritures = ecritures.filter(Ecriture.nom == nom)
    if id:
        ecritures = ecritures.filter(Ecriture.id == id)
    try:
        if valide == "yes":
            ecritures = ecritures.filter(Ecriture.valide == True)
        elif valide == "no":
            ecritures = ecritures.filter(Ecriture.valide == False)
        if filter == 'sum':
            ecritures = db.query(func.count(Ecriture.nom).label("nombre"),
                                 (func.sum(Ecriture.dc * Montant.montant).label("somme")/100.0).label("somme")).\
                           join(Ecriture.montant)
            if id_compte:
                ecritures = ecritures.filter(Ecriture.compte_id == id_compte)
            ecritures = ecritures.order_by(Ecriture.date).\
                                  one()
            return dumps({'somme': "%0.2f" % ecritures.somme,
                          'nombre': "%d" % ecritures.nombre,
                         })
        for lst_sort in sort.split(','):
            if lst_sort == 'nom':
                ecritures = ecritures.order_by(Ecriture.nom)
            elif lst_sort == 'type':
                ecritures = ecritures.order_by(Ecriture.type)
            elif lst_sort == 'montant':
                ecritures = ecritures.order_by(Montant.montant)
            elif lst_sort == 'categorie':
                ecritures = ecritures.order_by(Categorie.nom)
            elif lst_sort == 'ecriture_categorie':
                ecritures = ecritures.order_by(Montant.id)
        ecritures = ecritures.order_by(desc(Ecriture.date))
        ecritures = ecritures.all()

        if re.match(r"^\d+$", filter):
            ecritures = ecritures[:int(filter):]

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
                               'ecriture_categorie_id' : ecriture.ecriture_categorie_id,
                              })
    return dumps(list_ecritures)

@app.put(r'/ecriture/<id:int>')
@app.put(r'/ecriture/<id:int>/ec/<ec_id:int>')
def update_ecriture(db, id=None, ec_id=None):
    """ Update information for an ecriture """
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
        ecriture = db.query(Ecriture, Montant).\
                      join(Ecriture.montant).\
                      filter(Ecriture.id == id).\
                      one()
    except NoResultFound:
        abort(404, "ID not found")

    if id and not ec_id:
        if entity.has_key('nom'):
            ecriture.Ecriture.nom = entity["nom"]
        if entity.has_key('date'):
            ecriture.Ecriture.date = datetime.strptime(entity["date"], "%Y/%m/%d")
        if entity.has_key('dc'):
            ecriture.Ecriture.dc = entity["dc"]
        if entity.has_key('valide'):
            if entity["valide"].isnumeric():
                ecriture.Ecriture.valide = entity["valide"]
            elif entity["valide"].lower() == "true":
                ecriture.Ecriture.valide = True
            else:
                ecriture.Ecriture.valide = False
        if entity.has_key('montant'):
            ecriture.Montant.montant = (int(locale.atof(entity["montant"])*100))
        if entity.has_key('type'):
            ecriture.Ecriture.type = entity["type"]
        if entity.has_key('description'):
            ecriture.Montant.description = entity["description"]
        if entity.has_key('categorie'):
            ecriture.Montant.categorie_id = entity["categorie"]
        try:
            db.commit()
        except IntegrityError:
            abort(404, 'Integrity Error')
    elif id and ec_id:
        if not entity.has_key('montant'):
            abort(404, 'montant : non spécifié')
        if not entity.has_key('categorie'):
            abort(404, 'categorie : non spécifié')
        ecriture_categorie = db.query(Montant).\
                                filter(Montant.id == ec_id).\
                                one()
        if (int(locale.atof(entity["montant"])*100) >= ecriture_categorie.montant):
            abort(404, 'montant supérieur')
        #Create a new categorie
        new_categorie = Montant(ecriture_id=id,
                                          categorie_id=entity["categorie"],
                                          montant=int(locale.atof(entity["montant"])*100)
                                         )
        if entity.has_key('description'):
            ecriture.Montant.description = entity["description"]
        db.add(new_categorie)
        ecriture_categorie.montant = ecriture_categorie.montant - int(locale.atof(entity["montant"])*100)
        try:
            db.commit()
        except IntegrityError:
            abort(404, 'Integrity Error')

@app.post('/ecriture')
def insert_ecriture(db):
    """ Insert a new ecriture """
    data = request.body.readline()
    if not data:
        abort(204, 'No data received')
    entity = loads(data)
    if not entity.has_key('nom'):
        abort(404, 'Nom : non spécifié')
    if not entity.has_key('date'):
        abort(404, 'Date : non spécifié')
    if not entity.has_key('dc'):
        abort(404, 'dc : non spécifié')
    if not entity.has_key('montant'):
        abort(404, 'montant : non spécifié')
    if not entity.has_key('compte_id'):
        abort(404, 'compte_id : non spécifié')
    if not entity.has_key('type'):
        abort(404, 'type : non spécifié')
    ecriture = Ecriture(nom=entity["nom"],
                        date=datetime.strptime(entity["date"], "%Y/%m/%d"),
                        dc=entity["dc"],
                        compte_id=entity["compte_id"],
                        type=entity["type"],)
    if entity.has_key('valide'):
        if entity["valide"].isnumeric():
            ecriture.valide = entity["valide"]
        elif entity["valide"].lower() == "true":
            ecriture.valide = True
        else:
            ecriture.valide = False
    else:
        ecriture.valide = False
    if entity.has_key('nom_id'):
        ecriture.nom_id = entity["nom_id"]

    db.add(ecriture)
    try:
        db.commit()
    except IntegrityError:
        abort(404, 'Integrity Error')

    ecriture_categorie = Montant(montant=int(locale.atof(entity["montant"])*100),
                                           ecriture_id=ecriture.id,)
    if entity.has_key('description'):
        ecriture_categorie.description = entity["description"]
    #else:
    #    ecriture_categorie.description = "-"
    if entity.has_key('categorie'):
        ecriture_categorie.categorie_id = entity["categorie"]
    else:
        categorie = db.query(Categorie.id).\
                       filter(Categorie.nom == "Consommation").\
                       one()
        ecriture_categorie.categorie_id = categorie.id
    db.add(ecriture_categorie)

    try:
        db.commit()
    except IntegrityError:
        abort(404, 'Integrity Error')
    response.status = 201
    response.headers["Location"] = "/ecriture/%s/" % (ecriture.id,)


