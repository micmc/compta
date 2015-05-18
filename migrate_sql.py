#!/usr/bin/python
# -*- coding: utf8 -*-

import optparse
import sys
#import os
from decimal import Decimal
from xml.etree.ElementTree import ElementTree
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import sessionmaker
#from sqlalchemy.exc import IntegrityError
#from sqlalchemy.sql import func

from compta.db.base import Base
from compta.db.banque import Banque
from compta.db.compte import Compte
from compta.db.ecriture import Ecriture, EcritureCategorie
from compta.db.categorie import Categorie

def main():
    """ Main Page """

    #Initialize database engine
    engine = create_engine('sqlite:///./db/compta.db', echo=False)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)

    db_session = sessionmaker(bind=engine)
    session = db_session()

    #Parse arguments
    parser = optparse.OptionParser()
    parser.add_option("-f", "--file",
                      help="file to import",
                      dest="file_import")
    parser.add_option("-i", "--index",
                      help="Compte index to add",
                      dest="compte_index", type="int")
    (options, args) = parser.parse_args()

    if options.file_import is None:
        print "options -f is missing"
        sys.exit(1)
    if options.compte_index is None:
        print "options -i is missing"
        sys.exit(1)

    #Check if compte exist
    try:
        compte = session.query(Compte).\
                         filter(Compte.id == options.compte_index).\
                         one()
    except NoResultFound:
        print "Compte inexistant"
        sys.exit(1)
    print "migration pour le compte %s" % (compte.nom,)

    #Read xml file
    tree = ElementTree()
    tree.parse(options.file_import)
    xml_lines = tree.getiterator(u'Requête_export')
    #compte = Compte(pk=options.compte_index)
    tmp_cpt = 1
    for xml_line in xml_lines:
        import_date = xml_line.find('FA_Date')
        import_dc = xml_line.find('FA_DC')
        import_type = xml_line.find('FA_MPaiement')
        import_nom = xml_line.find('FA_Nom')
        import_categorie = xml_line.find('FA_Categorie')
        import_description = xml_line.find('FA_Description')
        import_montant = xml_line.find('FA_Montant')
        #Write Ecriture
        ecriture = Ecriture(nom=import_nom.text,
                            date=datetime.strptime(import_date.text.split('T')[0], "%Y-%m-%d"),
                            dc=import_dc.text,
                            type=import_type.text,
                            compte_id=compte.id)
        session.add(ecriture)
        session.commit()
        #Write EcritureCategorie
        ecriture_categorie = EcritureCategorie(montant=int(Decimal(import_montant.text)*100),
                                               ecriture_id=ecriture.id)
        try:
            categorie = session.query(Categorie.id).\
                                     filter(Categorie.nom == import_categorie.text).\
                                     one()
        except NoResultFound:
            categorie = Categorie(nom=import_categorie.text)
            session.add(categorie)
            session.commit()
        ecriture_categorie.categorie_id = categorie.id

        if import_description != None:
            categorie.description = import_description.text
        session.add(ecriture_categorie)
        session.commit()

        print "Enregistrement effectué : " + str(tmp_cpt)
        tmp_cpt += 1

if __name__ == "__main__":
    main()
