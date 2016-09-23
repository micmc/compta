 Compta
 -----------

Compta is a software to do accounting with a cli client and by html web site

 ------------
 Requirements
 ------------

 * GNU/Linux
 * Python 2.7 (x >= 4)
 * python-sqlalchemy
 * python-requests
 * Bottle

 -------------
 Documentation
 -------------

Local API documentation is available, just type:

    $ pydoc Compta

Some usual commands : 
- python lib/compta/server/server.py
  Launche server
- python lib/compta/cli/server.py -p compte list
  afficher la liste des comptes
- python lib/compta/cli/server.py -p compte list -f type=prs archive=false
  n'afficher que les comptes actifs de type compte courant
- python lib/compta/cli/server.py  ecriture list -f compte_id=10 sum
  Afficher les montants actuels pour la compte numéro 10
- python lib/compta/cli/server.py -p ecriture create -a compte_id=10
  Creer une nouvelle ecriture
- python server.py -p ecriture import  -i test.csv -a compte_id=10 tag=2016-06 type=Cb
  Importer des ecritures depuis une fichier avec un tag
  Utile pour importer les cartres bleus...
  Le fichier csv doit être dans ce format : nom;montant;date
  La catégorie est 5 par défaut où prendre le prompt pour choisir...

Par exemple pour fortnueo est l'exportation
Exporter les données en csv
- Ouvrir le csv avec libre office, supprimer les deux première colonnes
- grep "^carte" file > filen.csv
- sed -ie 's/^carte\ //g' filen.csv
- sed -ie 's/^\([0-9][0-9]\/[0-9][0-9]\)\ \(.*\)$/\1\/2015;\2/g' filen.csv

Ensuite mettre les intitulé 
date;nom;montant

Il ne reste plus qu'à importer...
- python lib/compta/cli/server.py -p ecriture import  -i ~/Documents/2014_04.csv -a compte_id=51 tag=banque_2015-08 type=Cb
- python lib/compta/cli/server.py -p ecriture create -a compte_id=51 tag=banque_2015-07 
- python lib/compta/cli/server.py -p ecriture create -a compte_id=33 tag=banque_2015-07

 ------------
 Installation
 ------------
 
 python setup.py install -O1 --skip-build --root ~/tmp/compta --record=INSTALLED_FILES

 -----
 Links
 -----

 -------
 Authors
 -------

David Micallef       <github@micallef.fr>
