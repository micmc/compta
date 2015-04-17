#!/usr/bin/python
# -*- coding: utf8 -*-
""" Application to create server for compta """

from bottle import Bottle
from bottle import response, request, abort
from json import dumps, loads
from datetime import datetime

from bottle.ext import sqlalchemy
#from sqlalchemy import create_engine, Column, Integer, Sequence, String
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func

from compta.db.base import Base
from compta.db.banque import Banque
from compta.db.compte import Compte
from compta.db.ecriture import Ecriture, EcritureCategorie
from compta.db.categorie import Categorie

app = Bottle()

def main():
    """ Main Page """
    engine = create_engine('sqlite:///./db/compta.test', echo=True)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    plugin = sqlalchemy.Plugin(engine, Base.metadata, create=False)
    app.install(plugin)
    app.run(host='localhost', port=8080, debug=True)

@app.hook('after_request')
def enable_cors():
    """ Header request for cors """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

@app.route('/banque/<id:int>', method=['OPTIONS'])
def default_banque(id):
    """ For firefox, ignore OPTIONS method """
    return {}

@app.get('/banque')
@app.get('/banque/<id:int>')
@app.get('/banque/<nom:re:[a-zA-Z\ ]+>')
def list_banque(db, id=None, nom=None):
    """ Display information for banque """
    banques = db.query(Banque)
    if id:
        banques = banques.filter(Banque.id == id)
    if nom:
        banques = banques.filter(Banque.nom == nom)
    try:
        banques = banques.order_by(Banque.nom).\
                          all()
    except NoResultFound:
        abort(404, "ID not found")
    if not banques:
        abort(404, "ID not found")
    list_banque = []
    for banque in banques:
        list_banque.append({'id': banque.id,
                            'nom': banque.nom,
                            'adresse': banque.adresse,
                            'ville': banque.ville,
                            'cp': banque.cp,
                            'pays': banque.pays,
                            'cle': banque.cle_controle,
                            'code_banque': banque.code_banque,
                            'code_guichet': banque.code_guichet})
    return dumps(list_banque)

@app.put('/banque/<id:int>')
def update_banque(db, id=None):
    """ Update information for a banque """
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
        banque = db.query(Banque).\
                    filter(Banque.id == id).\
                    one()
    except NoResultFound:
        abort(404, "ID not found")
    if entity.has_key('nom'):
        banque.nom = entity["nom"]
    if entity.has_key('adresse'):
        banque.adresse = entity["adresse"]
    if entity.has_key('ville'):
        banque.ville = entity["ville"]
    if entity.has_key('cp'):
        banque.cp = entity["cp"]
    if entity.has_key('pays'):
        banque.pays = entity["pays"]
    if entity.has_key('cle'):
        banque.cle_controle = entity["cle"]
    if entity.has_key('code_banque'):
        banque.code_banque = entity["code_banque"]
    if entity.has_key('code_guichet'):
        banque.code_guichet = entity["code_guichet"]
    db.commit()

@app.post('/banque')
def insert_banque(db):
    """ Insert a new banque """
    data = request.body.readline()
    if not data:
        abort(204, 'No data received')
    entity = loads(data)
    if not entity.has_key('nom'):
        abort(404, 'Nom : non spécifié')
    if not entity.has_key('adresse'):
        abort(404, 'Adresse : non spécifié')
    if not entity.has_key('ville'):
        abort(404, 'Ville : non spécifié')
    if not entity.has_key('cp'):
        abort(404, 'Code Postal : non spécifié')
    if not entity.has_key('pays'):
        entity['pays'] = 'FR'
    if not entity.has_key('cle'):
        entity['cle'] = '76'
    if not entity.has_key('code_banque'):
        entity['code_banque'] = ""
    if not entity.has_key('code_guichet'):
        entity['code_guichet'] = ""
    banque = Banque(nom=entity["nom"],
                    adresse=entity["adresse"],
                    ville=entity["ville"],
                    cp=entity["cp"],
                    pays=entity["pays"],
                    cle_controle=entity["cle"],
                    code_banque=entity["code_banque"],
                    code_guichet=entity["code_guichet"])
    db.add(banque)
    db.commit()
    response.status = 201
    response.headers["Location"] = "/banque/%s" % (banque.id,)

@app.delete('/banque/<id:int>')
def delete_banque(db, id=None):
    """ Delete a banque """
    try:
        banque = db.query(Banque).\
                    filter(Banque.id == id).\
                    one()
    except NoResultFound:
        abort(404, "ID not found")
    db.delete(banque)
    db.commit()


@app.get('/compte')
@app.get('/compte/<id_compte:int>')
@app.get('/compte/<nom:re:[a-zA-Z\ ]+>')
@app.get('/banque/<id:int>/compte')
@app.get('/banque/<id:int>/compte/<id_compte:int>')
@app.get('/banque/<id:int>/compte/<nom:re:[a-zA-Z\ ]+>')
def list_compte(db, id=None, nom=None, id_compte=None):
    """ List compte """
    comptes = db.query(Compte)
    if id:
        comptes = comptes.join(Compte.banque).\
                          filter(Banque.id == id)
    if nom:
        comptes = comptes.filter(Compte.nom == nom)
    if id_compte:
        comptes = comptes.filter(Compte.id == id_compte)
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

@app.put('/compte/<id:int>')
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

@app.delete('/compte/<id:int>')
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

@app.get('/ecriture')
@app.get('/ecriture/<id:int>')
@app.get('/ecriture/<nom:re:[a-zA-Z\ ]+>')
@app.get('/compte/<id_compte:int>/ecriture')
@app.get('/compte/<id_compte:int>/ecriture/<id:int>')
@app.get('/compte/<id_compte:int>/ecriture/<nom:re:[a-zA-Z\ ]+>')
def list_ecriture(db, id=None, nom=None, id_compte=None):
    """ List compte """
    ecritures = db.query(Ecriture, EcritureCategorie, Categorie).\
                   join(Ecriture.categories).\
                   join(EcritureCategorie.categorie)
    if id_compte:
        ecritures = ecritures.filter(Ecriture.compte_id == id_compte)
    if nom:
        ecritures = ecritures.filter(Ecriture.nom == nom)
    if id:
        ecritures = ecritures.filter(Ecriture.id == id)
    try:
        filters = request.query.filters
        valide = request.query.valide
        somme = request.query.somme

        if valide == "yes":
            ecritures = ecritures.filter(Ecriture.valide == True)
        elif valide == "no":
            ecritures = ecritures.filter(Ecriture.valide == False)
        if somme == 'yes':
            ecritures = db.query(func.count(Ecriture.nom).label("nombre"),
                                 (func.sum(Ecriture.dc * EcritureCategorie.montant).label("somme")/100).label("somme")).\
                           join(Ecriture.categories)
            if id_compte:
                ecritures = ecritures.filter(Ecriture.compte_id == id_compte)
            ecritures = ecritures.order_by(Ecriture.date).\
                                  one()
            return dumps({'somme': "%0.2f" % (ecritures.somme,),
                          'nombre': str(ecritures.nombre),
                         })

        ecritures = ecritures.order_by(Ecriture.date).\
                              all()
        
        if filters == 'last_10':
            ecritures = ecritures[-10:]
        if filters == 'last_5':
            ecritures = ecritures[-5:]

    except NoResultFound:
        abort(404, "ID not found")
    if not ecritures:
        abort(404, "ID not found")
    list_ecritures = []
    for ecriture in ecritures:
        list_ecritures.append({'id': ecriture.Ecriture.id,
                               'nom': ecriture.Ecriture.nom,
                               'date': datetime.strftime(ecriture.Ecriture.date,"%Y/%m/%d"),
                               'dc': ecriture.Ecriture.dc,
                               'type': ecriture.Ecriture.type,
                               'valide': ecriture.Ecriture.valide,
                               'compte_id': ecriture.Ecriture.compte_id,
                               'categorie': ecriture.Categorie.nom,
                               'montant': "%0.2f" %(ecriture.EcritureCategorie.montant/100,),
                               'description': ecriture.EcritureCategorie.description,
                              })
    return dumps(list_ecritures)

@app.put('/ecriture/<id:int>')
def update_ecriture(db, id=None):
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
        ecriture = db.query(Ecriture, EcritureCategorie).\
                      join(Ecriture.categories).\
                      filter(Ecriture.id == id).\
                      one()
    except NoResultFound:
        abort(404, "ID not found")
    
    if entity.has_key('nom'):
        ecriture.Ecriture.nom = entity["nom"]
    if entity.has_key('date'):
        ecriture.Ecriture.date = datetime.strptime(entity["date"],"%Y/%m/%d")
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
        ecriture.EcritureCategorie.montant = int(entity["montant"])*100
    if entity.has_key('type'):
        ecriture.EcritureCategorie.type = entity["type"]
    if entity.has_key('description'):
        ecriture.EcritureCategorie.description = entity["description"]
    if entity.has_key('categorie'):
        ecriture.Ecriture.categorie_id = entity["categorie"]
    try:
        db.commit()
    except IntegrityError:
        abort(404, 'Integrity Error')

@app.get('/categorie')
@app.get('/categorie/<id:int>')
@app.get('/categorie/<nom:re:[a-zA-Z\ ]+>')
def list_categorie(db, id=None, nom=None, id_compte=None):
    """ List categorie """
    categories = db.query(Categorie)
    if nom:
        categories = categories.filter(Categorie.nom == nom)
    if id:
        categories = categories.filter(Categorie.id == id)
    try:
        categories = categories.order_by(Categorie.nom).\
                                all()
    except NoResultFound:
        abort(404, "ID not found")
    if not categories:
        abort(404, "ID not found")
    list_categories = []
    for categorie in categories:
        list_categories.append({'id': categorie.id,
                               'nom': categorie.nom,
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


if __name__ == "__main__":
    main()

