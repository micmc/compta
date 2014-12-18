#!/usr/bin/python
# -*- coding: utf8 -*-

import optparse
import sys     
import os      

from datetime import datetime

from xml.etree.ElementTree import ElementTree

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from compta.db.banque import Banque
from compta.db.compte import Compte
from compta.db.ecriture import Ecriture, EcritureCategorie
from compta.db.categorie import Categorie

def arg_parse():
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

    return options

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
                                                  
    tree = ElementTree()                          
    print options.file_import
    tree.parse(options.file_import)               
    xml_lines = tree.getiterator(U'Requête_export')
    compte = session.query(Compte).filter_by(id =  options.compte_index).one()
    for xml_line in xml_lines:
        print xml_line.find('FA_Categorie').text
        try:
            categorie = session.query(Categorie).filter_by(nom = xml_line.find('FA_Categorie').text).one()
        except:
            categorie = Categorie(nom= xml_line.find('FA_Categorie').text)
            session.add(categorie)
            session.commit()
        date_ecriture = datetime.strptime(xml_line.find('FA_Date').text,"%Y-%m-%dT%H:%M:%S")
        ecriture = Ecriture(date_ecriture=date_ecriture,
                            dc=xml_line.find('FA_DC').text,
                            type_ecriture='Cb',
                            nom=xml_line.find('FA_Nom').text,
                            valide = True,
                            compte_id=compte.id)
        ecriture_categorie = EcritureCategorie(categorie_id=categorie.id,
                                               description=xml_line.find('FA_Description').text,
                                               montant=xml_line.find('FA_Montant').text,
                                               categorie="fuck")
        ecriture.categories.append(ecriture_categorie)
        session.add(ecriture)
        session.commit()

if __name__ == "__main__":
    main()
