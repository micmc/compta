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

== Optimisation de la base de données ==

Optimiser la base de données sur les categorie :
* Supprimer les doublons (fusion)
* voir s'il est possible de fusionner les petites categorie

== Insertion de nouvelle écriture ==

Il faut modifier l'affichage de la vue des categorie 
Max 10, pour le nombre des categorie

= Vue Banque =

* Regarder pour faire un sous menu sur les comptes

= Vue Tag =

Faire la vue 

= Vue Ecriture =

* Faire la vue, en utilisant les montant
* Ajouter des filtres
* Ajouter le mode multipage
* Essayer de voir s'il est possible d'ajouter les tags dans une liste ?
* Faire de tel sorte que les prélèvement / virement soit affiché.

= Stats =

* Réfléchir à des applis de graph
* Faire graph montant compte par mois
* Faire graph mouvement compte par mois avec moyenne
* Faire dépense mensuelle, annuellle pour les categorie sur un compte
* Pouvoir gérer les tags


