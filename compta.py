#!/usr/bin/python
# -*- coding: utf8 -*-

import optparse
import sys     
import os      
import string

from decimal import Decimal
from datetime import datetime

#from xml.etree.ElementTree import ElementTree

from sqlalchemy import create_engine, select, func, and_, desc
from sqlalchemy.orm import sessionmaker

from compta.db.banque import Banque
from compta.db.compte import Compte
from compta.db.ecriture import Ecriture, EcritureCategorie
from compta.db.categorie import Categorie

def arg_parse():
    parser = optparse.OptionParser()                  
    
    parser.add_option("-i",
                      "--index",
                      help=U"Compte index to add",     
                      dest="compte_index",
                      type="int")

    # group for display dabase information
    group_list = optparse.OptionGroup(parser, "Liste")
    group_list.add_option("--solde",
                          action="store_true",
                          dest="solde",
                          help=U"Solde du compte")
    group_list.add_option("--last",
                          action="store_true",
                          dest="last",
                          help=U"les 5 dernières opérations")
    group_list.add_option("--banque",
                          action="store_true",
                          dest="banque",
                          help=U"Liste des banques")
    group_list.add_option("--compte",
                          action="store_true",
                          dest="compte",
                          help=U"Liste des comptes")
    parser.add_option_group(group_list)
    
    # group for manage ecriture
    group_ecriture = optparse.OptionGroup(parser, "Ecriture")
    group_ecriture.add_option("--add_ecriture",
                              action="store_true",
                              dest="add_ecriture",
                              help=U"Ajout d'une ecriture")
    group_ecriture.add_option("-m", 
                              dest="montant",
                              help=U"Montant")
    group_ecriture.add_option("-t", 
                              dest="type_ecriture",
                              help=U"Type Ecriture [cb,pr,vr,re,ch], default = cb",
                              default="cb",
                              type="choice",
                              choices=["cb","pr","vr","re","ch"])
    group_ecriture.add_option("-D",
                              dest="date_ecriture",
                              help=U"Date [YYYY/MM/DD]")
    group_ecriture.add_option("-c",
                              dest="categorie",
                              help=U"Categorie",
                              default="")
    group_ecriture.add_option("-n",
                              dest="nom",
                              help=U"Nom")
    group_ecriture.add_option("-d",
                              dest="description",
                              help=U"Description",
                              default="")
    parser.add_option_group(group_ecriture)

    # group manage banque, compte, iban
    group_banque_compte = optparse.OptionGroup(parser, "Banque + compte")
    group_banque_compte.add_option("--add_banque",
                                   action="store_true",
                                   dest="add_banque_compte", 
                                   help=U"Ajout d'un compte bancaire iban")
    group_banque_compte.add_option("--nom_compte",
                                   dest="nom_compte",
                                   help=U"Nom du compte")
    group_banque_compte.add_option("--nom_banque",
                                   dest="nom_banque",
                                   help=U"Nom de la banque")
    group_banque_compte.add_option("--adresse",
                                   dest="adresse",
                                   help=U"Adresse")
    group_banque_compte.add_option("--ville",
                                   dest="ville",
                                   help=U"Ville")
    group_banque_compte.add_option("--cp",
                                   dest="cp",
                                   help=U"Code Postal")
    group_banque_compte.add_option("--type_compte",
                                   dest="type_compte",
                                   type="choice",
                                   choices=["prs","prv","dif","vir"],
                                   help=U"Type de Compte [prs,prv,dif,vir]")
    group_banque_compte.add_option("--iban",
                                   dest="iban",
                                   help=U"Numéro iban [FR76 1111 2222 3333 4444 5555 abc]")
    parser.add_option_group(group_banque_compte)
    
    #if options.compte_index is None and not options.compte:  
    #    print "options -i is missing" 
    #    sys.exit(1)                   
    (options, args) = parser.parse_args()

    return options

def liste_compte(session):
    comptes = session.query(Compte).all()
    for compte in comptes:
        print U"%d : %s, %s - %s" % (compte.id,
                                     compte.type,
                                     compte.banque.nom,
                                     compte.nom)

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
        print U"%s : %s - %2.2f €, %s / %s" % (ecriture.date_ecriture,
                                ecriture.type_ecriture,
                                ecriture.ecriture_categories[0].montant,
                                ecriture.nom,
                                ecriture.ecriture_categories[0].categorie.nom)

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
        input = raw_input("Choisissez la categorie : ")
        categorie = session.query(Categorie).filter_by(nom = categories[int(input)-1].nom).one()
    if not type_ecriture:
        type_ecriture='Cb'
    if float(montant) < 0:
        dc = -1
        montant = str(abs(Decimal(montant)))
    else:
        dc = 1
    date_ecriture = datetime.strptime(date_ecriture,"%Y-%m-%d")
    ecriture = Ecriture(nom=nom,
                        date_ecriture=date_ecriture,
                        dc=dc,
                        compte_id=compte_id,
                        type_ecriture=type_ecriture,valide=True)
    session.add(ecriture)
    ecriture_categorie = EcritureCategorie(montant=montant,
                                           description=description,
                                           categorie_id=categorie.id)
    ecriture.ecriture_categories.append(ecriture_categorie)
    session.commit()

def banque(session, nom, adresse, ville, cp, code_banque, code_guichet, pays='FR', cle_controle='76'):
    banque = Banque(nom = nom,
                    adresse = adresse,
                    ville = ville,
                    cp = cp,
                    code_banque = code_banque,
                    code_guichet = code_guichet,
                    pays = pays,
                    cle_controle = cle_controle)
    session.add(banque)
    session.commit()
    return banque

def compte(session, nom, numero, cle, type_compte, banque, archive=True):
    compte = Compte(nom = nom,
                    numero = numero,
                    cle = cle,
                    type_compte = type_compte,
                    #banque_id = banque_id,
                    archive = archive)
    banque.comptes.append(compte)
    #session.add(compte)
    session.commit()
    return compte

def add_iban( session, nom_compte, nom, adresse, ville, cp, type_compte, iban):
    iban = string.replace(iban," ","")
    pays = iban[0:2]
    cle_controle = iban[2:4]
    code_banque = iban[4:9]
    code_guichet = iban[9:14]
    numero = iban[14:25]
    cle = iban[25:27]
    banque_tmp = banque(session, nom, adresse, ville, cp, code_banque, code_guichet)
    print type(banque_tmp)
    #session.add(banque_tmp)
    #session.commit()
    compte_tmp = compte(session, nom_compte, numero, cle, type_compte, banque_tmp)
    #session.add(compte_tmp)
    #session.commit()

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
        sys.exit(0)
    if options.banque:
        liste_banque(session)
        sys.exit(0)
    if options.solde:
        liste_solde(session,options.compte_index)
        sys.exit(0)
    if options.last:
        liste_last(session,options.compte_index)
        sys.exit(0)
    if options.add_ecriture:
        ecriture(session,options.compte_index,
                 options.nom,
                 options.montant,
                 options.date_ecriture,
                 type_ecriture = options.type_ecriture,
                 description = options.description,
                 categorie= options.categorie)
        sys.exit(0)
    if options.add_banque_compte:
        add_iban(session,
                 options.nom_compte,
                 options.nom_banque,
                 options.adresse,
                 options.ville,
                 options.cp,
                 options.type_compte,
                 options.iban)
        sys.exit(0)

if __name__ == "__main__":
    main()
