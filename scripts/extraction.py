"""
Ce script récuppère les commentaires positifs et négatif du jeu skyrim, construit des fichiers pour chaque 
commentaire et ecrit ces commentaires dans un csv.
"""

import re 
import csv
import spacy
from pathlib import Path
from bs4 import BeautifulSoup 
from langdetect import detect
from datastructures import Commentaire
from typing import List


def lemmatiser_texte(texte):
    """Lemmatisation des commentaires"""

    nlp = spacy.load("fr_core_news_sm")
    liste_lemmes = []
    doc = nlp(texte)
    for token in doc:
        liste_lemmes.append(token.lemma_)
    return " ".join(liste_lemmes)


def commentaire_français(texte : str | Path) -> bool:
    """Vérifie si un texte est en français."""
    if len(texte) < 9:  ## on prédéfinit que notre texte doit avoir plus de 9 caractères
        return False
    langue = detect(texte)
    return langue == 'fr'

def pretraitement(page_html: str | Path) -> str:
    """Fonction qui permet de mieux supprimer le tag de la date et aussi prétraiter le texte"""

    ## il faut supprimer le tag date_posted car le résultat est moche et on ne le veut pas, il est contenu dans la balise qui contient le commentaire
    with open(page_html, 'r' ) as f:
        soup = BeautifulSoup(f, "html.parser", multi_valued_attributes=None)

    for tag in soup.find_all("div", class_="date_posted"):
        tag.decompose()

    ## pour enlever les tabulations
    for tag in soup.find_all(attrs={'class':'apphub_CardTextContent'}):
        tag.string = tag.get_text(strip=True)

    ## utilisation d'une expression régulière afin de retirer les commentaire qui sont des dessins graphiques
    for tag in soup.find_all(attrs={'class':'apphub_CardTextContent'}):
        cleaned_text = re.sub(r'[^\w\s-]', '', tag.get_text()) 
        tag.string = cleaned_text.lower()  
    
    return soup


def chargement_commentaire_positif(soup : BeautifulSoup, chemin_resultat : str | Path) -> List[Commentaire]:
    """Cette fonction créee un fichier par commentaire positif, elle vérifie que le commentaire est français
    et """
    # surement pas la meilleure technique j'avais des problemes pour manipuler le tag cela m'indiquait que c'était un tag et non un str du coup j'ai fait une liste

    tag = soup.find_all(attrs={'class':'apphub_CardTextContent'})
    liste = []
    liste_objet_positif = []
    i = 0

    for element in tag:
        texte = element.get_text()
        texte = texte.lower()
        # print(texte)
        if commentaire_français(texte):
            mots_lemmatiser = lemmatiser_texte(texte)
            mots = mots_lemmatiser.split()
            if len(mots) >= 10: ## il doit y avoir plus de 10 mots dans le commentaire pour être pris en compte
                liste.append(mots) ## ajout à la premiere liste
                commentaire_positif = Commentaire(id_fichier=i, sentiment="positif", commentaire=mots) ## ajout à la liste de notre dataclass commentaire
                liste_objet_positif.append(commentaire_positif)
                i+=1
                if i == 244:
                    break

    print(f'{len(liste)}')
    
    try:
        for i, mots_lemmatiser in enumerate(liste): 
            commentaire_texte = ' '.join(mots_lemmatiser)  ## pour ne pas avoir notre resultat sous forme de liste 
            commentaire_texte = commentaire_texte.lower()  
            with open(f"{chemin_resultat}/commentaire_positif_{i}.txt", 'w', encoding='UTF-8') as resultat:
                resultat.write(commentaire_texte.strip()) 


    except Exception as e:
        print(f"Il y'a eu une erreur : {e}")
    
    
    return liste_objet_positif

def chargement_commentaire_negatif(soup : BeautifulSoup, chemin_resultat : str | Path) -> List[Commentaire]:
    """Récuppération des commentaires négatif, même principe que la fonction pour les commentaires positifs"""

    tag = soup.find_all(attrs={'class':'apphub_CardTextContent'})
    liste = []
    liste_objet_negatif = []
    i = 0
    
    for element in tag:
            texte = element.get_text()
            texte = texte.lower()
            # print(texte)
            if commentaire_français(texte):
                mots_lemmatiser = lemmatiser_texte(texte)
                mots = mots_lemmatiser.split()
                if len(mots) >= 10: ## il doit y avoir plus de 10 mots dans le commentaire pour être pris en compte
                    liste.append(mots) ## ajout à la premiere liste
                    commentaire_negatif = Commentaire(id_fichier=i, sentiment="negatif", commentaire=mots) ## ajout à la liste de notre dataclass commentaire
                    liste_objet_negatif.append(commentaire_negatif)
                    i+=1
                    if i == 244:
                        break

    print(f'{len(liste)}')
    
    try:
        for i, mots_lemmatiser in enumerate(liste): 
            commentaire_texte = ' '.join(mots_lemmatiser)  ## pour ne pas avoir notre resultat sous forme de liste 
            commentaire_texte = commentaire_texte.lower()  
            with open(f"{chemin_resultat}/commentaire_negatif_{i}.txt", 'w', encoding='UTF-8') as resultat:
                resultat.write(commentaire_texte.strip()) 
    
    except Exception as e:
        print(f"Il y'a eu une erreur : {e}")
    
    return liste_objet_negatif


# def ecriture_commentaire_csv(liste_commentaires, nom_fichier):
#     """Écriture des commentaires dans notre CSV"""

#     with open(nom_fichier, mode='w', newline='', encoding='UTF-8') as file:
#         writer = csv.writer(file)
#         writer.writerow(['commentaire'])  
#         for commentaire in liste_commentaires:
#             writer.writerow([commentaire.commentaire])
    
def ecrire_commentaire_csv_total(liste_commentaires, nom_fichier):
    """Écriture des commentaires dans notre CSV"""

    with open(nom_fichier, mode='w', newline='', encoding='UTF-8') as file:
        writer = csv.writer(file)
        writer.writerow(['id_fichier', 'sentiment', 'commentaire'])
        for commentaire in liste_commentaires:
            commentaire_texte = ' '.join(commentaire.commentaire)  
            writer.writerow([commentaire.id_fichier, commentaire.sentiment, commentaire_texte])  
  



def main():

    resultat_pretraitement_positif = pretraitement("../data/commentaires_positifs/page/Communauté Steam The Elder Scrolls V Skyrim Special Edition.html")  
    liste_commentaires_positifs = chargement_commentaire_positif(resultat_pretraitement_positif, "../data/commentaire_positifs")
    resultat_pretraitement_negatif = pretraitement("../data/commentaires_negatifs/page/Communauté Steam The Elder Scrolls V Skyrim Special Edition.html") 
    liste_commentaires_negatifs = chargement_commentaire_negatif(resultat_pretraitement_negatif, "../data/commentaire_negatifs") 

    ## Ecriture des commentaires dans 2 csv différents
    #ecriture_commentaire_csv(liste_commentaires_negatifs, '../data/commentaire_negatifs/commentaires_negatifs.csv')
    #ecriture_commentaire_csv(liste_commentaires_positifs, '../data/commentaire_positifs/commentaires_positifs.csv')

    ##fusion des 2 listes de commentaires objets
    liste_commentaires = liste_commentaires_positifs + liste_commentaires_negatifs

    ecrire_commentaire_csv_total(liste_commentaires, '../data/commentaires.csv')




if __name__ == "__main__":
    main()