# Analyse des sentiments commentaire Steam sur le jeu Skyrim
---------------

- GILLET Baptiste
- VAN Débora 



# Choix du Sujet

Débora et moi sommes deux passionnés de jeux vidéos et lorsque l'enjeu de ce projet nous a été présenté nous avons de suite penser à le relier à ce domaine.
Nous avons décidé de nous servir de la platforme steam qui lors du parcours du ./robots de la page n'interdisait pas le scrapping. 
Pour ce qui est du choix du jeu nous avons décidé de prendre un monument du jeu qui suscite beaucoup de commentaire à savoir "**Skyrim**".



### Librairies utilisées 

- Sckipit Learn
- BeautifulSoup : pour scrapper nos pages steam
- Languedetect pour identifier la langue
-----

# Organisation du projet :

Vous retrouverez dans notre Github, les différents scripts qui nous ont permis de récuppérer les commentaires.
La logique était la suivante, nous récupérons, grâce au script extraction,les commentaires positifs d'un côté et les négatifs de l'autre grâce à BeautifulSoup. Pour chaque commentaire nous créons un fichier.
Les commentaires sont rangés dans des fichiers commentaire_negatif, commentaire positif.



## Prétraitement des données

Nous le savons les gamers ont tendance à être assez tatillon lorsqu'il s'agit de laisser un commentaire sur un jeu qu'ils aiment où non. Nous avons été confronté à plusieurs difficultés qu'il a fallu gérer lors du prétraitement de nos données.
