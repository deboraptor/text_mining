# Fouille de textes
Projet pour le cours de fouille de textes dans le cadre du master TAL.

## Qui sommes-nous ?
Nous sommes en première année de master TAL et dans le cadre du cours de Fouille de textes nous devons réaliser
une analyse de données avec le logiciel _Weka_.

## Notre sujet
Récupérer des commentaires de jeux vidéos et essayer de trier automatiquement les commentaires avec la polarité 
négatif/positifs.

## Notre corpus
Nous avons extrait notre corpus du site internet __Steam__. 

## Etape 1 : anonymisation
Dans notre cas, il va falloir retirer les images et les pseudo des utilisateurs.

## Etape 2 : nettoyage du corpus
### Nos problèmes 
* Certains commentaires en anglais apparaissent aussi -> langdetect
* Il faut supprimer les émojis.

## Pourquoi nettoyer ?
Il est important de nettoyer notre corpus car nous allons par la suite utiliser un script qui s'appelle 
`vectorisation.py` pour convertir notre corpus collecté en données utilsables par _Weka_, un logiciel d'analyse
et d'exploiration de données pour le traitement automatique. 

## Etape n : intérprétation des données dans Weka
Il faut faire : 
* les métriques (précision, rappel et f-mesure)
* Naive Bayes (théorème de Bayes)
* matrice de confusion (?)
* SVM (SMO sur Weka)
* arbre de décision C4,5 (J48 sur Weka)

# Installer un environnement virtuel 
Pour éviter les conflits de version, nous allons créer un environnement virtuel.

Pour créer un environnement virtuel, vous pouvez procéder comme cela : 

`python3 -m venv nom_du_venv`
<br>
`source nom_du_venv/bin/activate`


La deuxième commande permet d’activer l’environnement. Lorsque c’est fait, vous verrez entre parenthèse le nom de votre environnement tout à gauche de la ligne de commande.

`pip install -r requirements.txt`


N’oubliez pas de désactiver l’environnement lorsque vous avez terminé.

`deactivate`

