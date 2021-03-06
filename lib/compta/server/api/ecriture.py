#!/usr/bin/python
# -*- coding: utf8 -*-
""" Application to create api to manage banque """

import re
import locale

from json import dumps, loads
from datetime import datetime

from sqlalchemy import desc
from sqlalchemy import extract
from sqlalchemy.orm import aliased
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
@app.get(r'/compte/<compte_id:int>/ecriture/<month:re:month>')
def list_ecriture(db, id=None, nom=None, compte_id=None, sum=None, month=None):
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
                             func.sum(Montant.montant/100.0).label("somme")
                            ).\
                       join(Ecriture.montant).\
                       filter(Ecriture.compte_id == compte_id).\
                       one()
        return dumps({'somme': "%0.2f" % ecritures.somme if ecritures.somme is not None else 0,
                      'nombre': "%d" % ecritures.nombre,
                     }
                    )
    if month:
        ecriture = aliased(Ecriture, name="ecriture_full")
        debit = db.query(func.sum(Montant.montant/100.0)).\
                   select_from(Ecriture).\
                   join(Ecriture.montant).\
                   filter(Ecriture.compte_id == compte_id).\
                   filter(extract('year', Ecriture.date) == 2015).\
                   filter(extract('month', Ecriture.date) == extract('month', ecriture.date)).\
                   filter(Montant.montant < 0).\
                   label("debit")
        credit = db.query(func.sum(Montant.montant/100.0)).\
                   select_from(Ecriture).\
                   join(Ecriture.montant).\
                   filter(Ecriture.compte_id == compte_id).\
                   filter(extract('year', Ecriture.date) == 2015).\
                   filter(extract('month', Ecriture.date) == extract('month', ecriture.date)).\
                   filter(Montant.montant > 0).\
                   label("credit")
        ecritures = db.query(extract('month', ecriture.date).label("date"),
                             debit,
                             credit
                            ).\
                       join(ecriture.montant).\
                       filter(ecriture.compte_id == compte_id).\
                       filter(extract('year', ecriture.date) == 2015).\
                       group_by(extract('month', ecriture.date).label("date")).\
                       all()
        list_month_debit = [0 for number in range(12)]
        list_month_credit = [0 for number in range(12)]
        cpt = 0
        for ecriture in ecritures:
            cpt += 1
            print ecriture, cpt
            list_month_debit[ecriture.date-1] = float(ecriture.debit) if ecriture.debit != None else 0
            list_month_credit[ecriture.date-1] = float(ecriture.credit) if ecriture.credit != None else 0
        return dumps([list_month_debit,list_month_credit])
    
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
                         Montant.montant.label("montant"),
                         Ecriture.type.label("type"),
                         Categorie.nom.label("categorie"),
                         Categorie.id.label("categorie_id"),
                         Montant.description.label("description"),
                         Montant.id.label("montant_id"),
                         Ecriture.valide.label("valide"),
                         Ecriture.compte_id.label("compte_id"),
                        ).\
                   join(Ecriture.montant).\
                   join(Montant.categorie)


    if filter:
        for column, value in filter.iteritems():
            if not isinstance(value, list):
                ecritures = ecritures.filter(getattr(Ecriture, column) == value)
            else:
                ecritures = ecritures.filter(getattr(Ecriture, column).in_(value))
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
    attributs = App.get_attribut(request.query.attribut)
    if attributs:
        for ecriture in ecritures:
            dict_attributs = {}
            for attribut in attributs:
                dict_attributs[attribut] = getattr(ecriture, attribut)
            list_ecritures.append(dict_attributs)
    else:
        for ecriture in ecritures:
            list_ecritures.append({'id': ecriture.id,
                                   'nom': ecriture.nom,
                                   'date': datetime.strftime(ecriture.date, "%Y/%m/%d"),
                                   'type': ecriture.type,
                                   'valide': ecriture.valide,
                                   'categorie': ecriture.categorie,
                                   'categorie_id': ecriture.categorie_id,
                                   'montant': "%0.2f" % (ecriture.montant/100.0,),
                                   'description': ecriture.description,
                                   'montant_id': ecriture.montant_id,
                                   'compte_id': ecriture.compte_id,
                                  })
    if request.query.get('skip') and request.query.get('top'):
        return dumps({'count': len(list_ecritures),
                      'values': list_ecritures[request.query.get('skip',type=int):request.query.get('skip', type=int) + request.query.get('top', type=int)]
                     }
                    )
    else:
        return dumps(list_ecritures)

@app.post('/ecriture')
def insert_ecriture(db):
    """ Create an ecriture """
    entity = App.check_data(Ecriture, request.body.readline())
    if entity:
        ecriture = Ecriture()
        for column, value in entity.iteritems():
            if column == 'date':
                ecriture.date = datetime.strptime(value, "%Y/%m/%d")
            #else:
            #    setattr(ecriture, column, value)
            elif column == 'nom':
                ecriture.nom = value
            elif column == 'type':
                ecriture.type = value
            elif column == 'valide':
                ecriture.valide = value
            elif column == 'compte_id':
                ecriture.compte_id = value
            elif column == 'nom_id':
                ecriture.nom_id = value
        try:
            db.add(ecriture)
            db.commit()
        except IntegrityError as ex:
            print ex
            abort(404, ex.args)
        montant = Montant()
        for column, value in entity.iteritems():
            if column == 'montant':
                montant.montant = int(round(locale.atof(value)*100,2))
            elif column == 'description':
                montant.description = value
            elif column == 'categorie_id':
                montant.categorie_id = value
        try:
            ecriture.montant.append(montant)
            db.commit()
        except IntegrityError as ex:
            print ex
            abort(404, ex.args)
        response.status = 201
        response.headers["Location"] = "/ecriture/%s/" % (ecriture.id,)
        ecriture = loads(list_ecriture(db, ecriture.id))
        return ecriture[0]


@app.put(r'/ecriture/<id:int>')
@app.put(r'/ecriture/<id:int>/montant/<montant_id:int>')
def update_ecriture(db, id=None, montant_id=None):
    """ Update information for an ecriture """
    entity = App.check_data(Ecriture, request.body.readline())
    if entity:
        try:
            ecriture = db.query(Ecriture).\
                          filter(Ecriture.id == id).\
                          one()
            # if montant_id:
            #     ecriture = ecriture.filter(Montant.id == montant_id).\
            #ecriture = ecriture.one()
        except NoResultFound:
            abort(404, "ID not found")
        for column, value in entity.iteritems():
            if column == 'date':
                ecriture.date = datetime.strptime(value, "%Y/%m/%d")
            elif column == 'nom':
                ecriture.nom = value
            elif column == 'type':
                ecriture.type = value
            elif column == 'valide':
                ecriture.valide = value
            elif column == 'nom_id':
                ecriture.nom_id = value
        try:
            montant = db.query(Montant).\
                         filter(Montant.id == entity['montant_id']).\
                         one()
        except NoResultFound:
            abort(404, "ID not found")
        for column, value in entity.iteritems():
            if column == 'montant':
                montant.montant = int(round(locale.atof(value)*100,2))
            if column == 'description':
                montant.description = value
            elif column == 'categorie_id':
                montant.categorie_id = value
        try:
            db.commit()
            ecriture = loads(list_ecriture(db, id))
            return ecriture[0]
        except Exception as ex:
            abort(404, ex)

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
    return dumps({'id': id,})
    
