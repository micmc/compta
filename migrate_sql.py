#!/usr/bin/python
# -*- coding: utf8 -*-

import optparse
import sys
import os
from xml.etree.ElementTree import ElementTree


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "compta.settings")

    from ecriture.models import Ecriture, Categorie
    from banque.models import Compte

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
    
    tree = ElementTree()
    tree.parse(options.file_import)
    xml_lines = tree.getiterator('Requete_export')
    compte = Compte(pk=options.compte_index)
    tmp_cpt = 1
    for xml_line in xml_lines:
        import_date = xml_line.find('FA_Date')
        import_dc = xml_line.find('FA_DC')
        import_type = xml_line.find('FA_MPaiement')
        import_nom = xml_line.find('FA_Nom')
        import_categorie = xml_line.find('FA_Categorie')
        import_description = xml_line.find('FA_Description')
        import_montant = xml_line.find('FA_Montant')
        ecriture = Ecriture()
        ecriture.date = import_date.text.split('T')[0]
        ecriture.dc = import_dc.text
        ecriture.type = import_type.text
        ecriture.nom = import_nom.text
        ecriture.compte = compte
        ecriture.save()
        print ecriture
        categorie = Categorie()
        categorie.categorie = import_categorie.text
        if import_description != None:
            categorie.description = import_description.text
        categorie.montant = import_montant.text
        categorie.ecriture = ecriture
        categorie.save()
        print "Enregistrement effectué : " + str(tmp_cpt)
        tmp_cpt +=  1
        #for xml_child in xml_line.getchildren():
        #    print xml_child.text
        #    print xml_child.tag
