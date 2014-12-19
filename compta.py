#!/usr/bin/python
# -*- coding: utf8 -*-

import optparse
import sys     
import os      

from datetime import datetime

from xml.etree.ElementTree import ElementTree

from sqlalchemy import create_engine, select, func, and_, desc
from sqlalchemy.orm import sessionmaker

from compta.db.banque import Banque
from compta.db.compte import Compte
from compta.db.ecriture import Ecriture, EcritureCategorie
from compta.db.categorie import Categorie

def arg_parse():
    parser = optparse.OptionParser()                  
    
    parser.add_option("-i", "--index",                
                      help=U"Compte index to add",     
                      dest="compte_index", type="int")

    # group for display dabase information
    group_list = optparse.OptionGroup(parser, "Liste")
    group_list.add_option("--solde", action="store_true",
                     dest="solde", help=U"Solde du compte")
    group_list.add_option("--last",  action="store_true",
                     dest="last", help=U"les 5 dernières opérations")
    group_list.add_option("--banque", action="store_true",
                     dest="banque", help=U"Liste des banques")
    group_list.add_option("--compte", action="store_true",
                     dest="compte", help=U"Liste des comptes")
    parser.add_option_group(group_list)
    
    # group for manage ecriture
    group_ecriture = optparse.OptionGroup(parser, "Ecriture")
    group_ecriture.add_option("--add", action="store_true",
                              dest="add_ecriture", help=U"Ajout d'une ecriture")
    group_ecriture.add_option("-m", 
                              dest="montant", help=U"Montant")
    group_ecriture.add_option("-D",
                              dest="date_ecriture", help=U"Date [YYYY/MM/DD]")
    group_ecriture.add_option("-c",
                              dest="categorie", help=U"Categorie")
    group_ecriture.add_option("-n",
                              dest="nom", help=U"Nom")
    group_ecriture.add_option("-d",
                              dest="description", help=U"Description")
    parser.add_option_group(group_ecriture)

    (options, args) = parser.parse_args()

    #if options.compte_index is None and not options.compte:  
    #    print "options -i is missing" 
    #    sys.exit(1)                   

    return options

def liste_compte(session):
    comptes = session.query(Compte).all()
    for compte in comptes:
        print U"%d : %s, %s - %s" % (compte.id, compte.type, compte.banque.nom, compte.nom)

def liste_banque(session):
    banques = session.query(Banque).all()
    for banque in banques:
        print U"%d : %s" % (banque.id, banque.nom)

def liste_solde(session, compte_id):
    total_solde = select([func.sum(Ecriture.dc*EcritureCategorie.montant).label('solde')]).where(
                         and_(Ecriture.compte_id==compte_id,
                              Ecriture.id==EcritureCategorie.ecriture_id))
    print U"Solde : %2.2f €" % (session.query(total_solde).one())

def liste_last(session, compte_id, latest=10):
    ecritures = session.query(Ecriture).filter_by(compte_id = compte_id).order_by(desc(Ecriture.date_ecriture)).limit(latest)
    for ecriture in ecritures:
        print U"%s : %s - %2.2f €, %s" % (ecriture.date_ecriture,
                                ecriture.type_ecriture,
                                ecriture.categories[0].montant,
                                ecriture.nom)

#./compta.py --add -i 1 -m 45 -n test -D 2014-12-01
def ecriture(session, compte_id, nom, montant, date_ecriture, categorie="", description="", type_ecriture=""):
    if not categorie:
        list_categorie = select([func.count(EcritureCategorie.categorie_id).label('categorie_count'),Categorie.nom]).where(
                                and_(EcritureCategorie.categorie_id==Categorie.id)).group_by(Categorie.nom).order_by(desc('categorie_count'))
        categories = session.query(list_categorie).limit(10)
        i = 1
        for categorie in categories:
            
            print U"%d : %s " % (i,categorie.nom)
            i += 1
        input = raw_input("Choisissez la categorie")
        categorie = session.query(Categorie).filter_by(nom = categories[int(input)-1].nom).one()

    if not type_ecriture:
        type_ecriture='CB'

    if montant < 0:
        dc = -1
    else:
        dc = 1
    date_ecriture = datetime.strptime(date_ecriture,"%Y-%m-%d")
    ecriture = Ecriture(nom=nom, date_ecriture=date_ecriture, dc=dc, compte_id=compte_id, type_ecriture=type_ecriture,valide=True)
    session.add(ecriture)
    ecriture_categorie = EcritureCategorie(montant=montant, description=description, categorie_id=categorie.id,categorie='test')
    ecriture.ecriture_categories.append(ecriture_categorie)
    session.commit()

def main():
    options = arg_parse()

    engine = create_engine('sqlite:///db/compta.test')
    
    #Base = declarative_base()
    #Base.metadata.bind = engine
    #Base.metadata.create_all(engine)
    #banque = session.query(Banque).all()
    #for titi in banque:
    #    print tite.nom
    #    print titi.compte
    
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
                                                  
    if options.compte:
        liste_compte(session)
    if options.banque:
        liste_banque(session)
    if options.solde:
        liste_solde(session,options.compte_index)
    if options.last:
        liste_last(session,options.compte_index)
    if options.add_ecriture:
        ecriture(session,options.compte_index,
                 options.nom,
                 options.montant,
                 options.date_ecriture)

if __name__ == "__main__":
    main()
