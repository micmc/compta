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
- python server.py -p ecriture create -a compte_id=10
  Creer une nouvelle ecriture

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

David Micallef       <david@micallef.fr>
