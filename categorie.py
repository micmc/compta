#!/usr/bin/python
# -*- coding: utf8 -*-

import optparse
import sys
import os
import sqlite3

if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-f", "--file",
                      help="file to import",
                      dest="file_import")
    parser.add_option("-i", "--index",
                      help="Compte index to add",
                      dest="compte_index", type="int")
    (options, args) = parser.parse_args()
    
    conn = sqlite3.connect('compta.db')
    cur_categorie = conn.cursor()
    cur_categorie.execute("select id,nom from categorie;")
    cur_ecriture = conn.cursor()
    i = 1
    for categorie in cur_categorie.fetchall():
        cur_ecriture.execute("select id from ecriture_categorie where categorie = '%s'" % (categorie[1]))
        for ecriture in cur_ecriture.fetchall():
            cur_ecriture.execute("update ecriture_categorie set categorie_id=%s where id=%s" % (str(categorie[0]),str(ecriture[0])))
    conn.commit()
    cur_ecriture.close()
    cur_categorie.close()
    conn.close()
    
