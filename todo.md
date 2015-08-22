#David Micallef
#2015-07-31

= cli client =

== fast insert ==

Ajouter une nouvelle options.
faire l'import de fichier xml ou csv

* On verifie s'il y a une entête de fichier
* Pour chaque champ on vérifie l'équivalence et on propose si besoin
* On ignore ensuite le reste du fichier
* On import ensuite dans la base de données.

Champs obligatoire : 
* type,
* dc,
* compte_id,
* date,
* nom
* montant
* categorie_id : consommation ou inconnue

= Vue Ecriture =

Bogue sur DC :
Revoir le fonctionnement.
Faire abastraction de la base de données. Un montant est soit positif ou négatif.
DC doit-il être supprimé, mais facultatif
On sauvegarde en valeur absolur type int
Si montant < 0 : dc type debit

* Faire de tel sorte que les prélèvement / virement soit affiché.

= Stats =

* Réfléchir à des applis de graph
* Faire graph montant compte par mois
* Faire graph mouvement compte par mois avec moyenne
* Faire dépense mensuelle, annuellle pour les categorie sur un compte
* Pouvoir gérer les tags


