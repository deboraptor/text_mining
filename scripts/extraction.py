"""
Ce script récuppère les commentaires positifs et négatif du jeu skyrim, construit des fichiers pour chaque 
commentaire et ecrit ces commentaires dans un csv.
"""


import csv
from pathlib import Path
from bs4 import BeautifulSoup 
from langdetect import detect
from datascturtures import Commentaire
from typing import List

    ##questions de prétraitement :
    ## - les qcm
    ## les emojis 
    ## les images avec dessinées avec des ___
    ## ne prendre en compte que les commentaires avec un certains nombre de mots : FAIT
    ## certains coms restent en anglais

def traitement_des_langues(chemin_resultat : str | Path) -> bool:

    # print(len(chemin_resultat))
    chemin_resultat = Path(chemin_resultat)

    for file in chemin_resultat.glob("*.txt"):
        with open(file, "r") as f:
            content = f.read()
            langue = detect(content)
            if langue == 'fr':
                print(f"{file}\t{detect(content)}")
                return True
            else:
                print(f"On a skip cette langue : {langue}")
                return False


def pretraitement(page_html: str | Path) -> str:

    ## prétraitement : 
    ## il faut supprimer le tag date_posted car le résultat est moche et on ne le veut pas, il est contenu dans la balise qui contient le commentaire

    with open(page_html, 'r' ) as f:
        soup = BeautifulSoup(f, "html.parser", multi_valued_attributes=None)

    for tag in soup.find_all("div", class_="date_posted"):
        tag.decompose()
    return soup


def chargement_commentaire_positif(soup : BeautifulSoup, chemin_resultat : str | Path) -> List[Commentaire]:

    # surement pas la meilleure technique j'avais des problemes pour manipuler le tag cela m'indiquait que c'était un tag et non un str du coup j'ai fait une liste

    tag = soup.find_all(attrs={'class':'apphub_CardTextContent'})
    liste = []
    liste_objet_positif = []
    i = 0
    for element in tag:
        texte = element.get_text()
        texte = texte.lower()
        mots = texte.split()
        if len(mots) >= 10: ## il doit y avoir plus de 10 mots dans le commentaire pour être pris en compte
            liste.append(element.get_text()) ## ajout à la premiere liste
            commentaire_positif = Commentaire(id_fichier=i, sentiment="positif", commentaire=texte) ## ajout à la liste de notre dataclass commentaire
            liste_objet_positif.append(commentaire_positif)
            i+=1
    print(f'{len(liste)}')
    try:
        for i, element in enumerate(liste): 
            element = element.lower()
            with open(f"{chemin_resultat}/commentaire_positif_{i}.txt", 'w', encoding='UTF8') as resultat:
                resultat.write(element.strip())
                # if not traitement_des_langues(resultat.name):
                #     # on supprime le fichier si c'est pas en français
                #     resultat.close()
                #     Path(resultat.name).unlink()
    except Exception as e:
        print(f"Il y'a eu une erreur : {e}")
    
    return liste ,liste_objet_positif

def chargement_commentaire_negatif(soup : BeautifulSoup, chemin_resultat : str | Path) -> List[Commentaire]:
    """Récuppération des commentaires négatif, même principe que la fonction pour les commentaires positifs"""

    tag = soup.find_all(attrs={'class':'apphub_CardTextContent'})
    liste = []
    liste_objet_negatif = []
    i = 0
    for element in tag:
        texte = element.get_text()
        mots = texte.split()
        if len(mots) >= 10: 
            liste.append(element.get_text())
            commentaire_negatif = Commentaire(id_fichier=i, sentiment="negatif", commentaire=texte, )
            liste_objet_negatif.append(commentaire_negatif)
            i+= 1
    print(f'{len(liste)}')
    try:
        for i, element in enumerate(liste):
            element = element.lower() # on met tout en minuscule pour éviter les erreurs avec langdetect
            with open(f"{chemin_resultat}/commentaire_negatif_{i}.txt", 'w', encoding='UTF8') as resultat:
                resultat.write(element.strip())
    except Exception as e:
        print(f"Il y'a eu une erreur : {e}")

    return liste_objet_negatif

def ecrire_commentaire_csv(liste_commentaires, nom_fichier):
    with open(nom_fichier, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['id_fichier', 'sentiment', 'commentaire'])  # Écrire l'en-tête des colonnes
        for commentaire in liste_commentaires:
            writer.writerow([commentaire.id_fichier, commentaire.sentiment, commentaire.commentaire])  # Écrire chaque ligne


def main():

    resultat_pretraitement_positif = pretraitement("../data/commentaire_positif/page/Communauté Steam The Elder Scrolls V Skyrim Special Edition.html")  
    liste_commentaires_positifs = chargement_commentaire_positif(resultat_pretraitement_positif, "../data/commentaire_positif")
    resultat_pretraitement_negatif = pretraitement("../data/commentaire_negatif/page/Communauté Steam The Elder Scrolls V Skyrim Special Edition.html") 
    liste_commentaires_negatifs = chargement_commentaire_negatif(resultat_pretraitement_negatif, "../data/commentaire_negatif") 

    ##fusion des 2 listes de commentaires objets
    liste_commentaires = liste_commentaires_positifs + liste_commentaires_negatifs
    

    ecrire_commentaire_csv(liste_commentaires, '../data/commentaires.csv')

if __name__ == "__main__":
    main()