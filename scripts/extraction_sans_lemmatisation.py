"""
Ce script récuppère les commentaires positifs et négatif du jeu skyrim, construit des fichiers pour chaque 
commentaire et ecrit ces commentaires dans un csv.
"""
import re 
import csv
from pathlib import Path
from bs4 import BeautifulSoup 
from langdetect import detect
from datastructures import Commentaire
from typing import List

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
            mots = texte.split()
            if len(mots) >= 10: ## il doit y avoir plus de 10 mots dans le commentaire pour être pris en compte
                liste.append(element.get_text()) ## ajout à la premiere liste
                commentaire_positif = Commentaire(id_fichier=i, sentiment="positif", commentaire=texte) ## ajout à la liste de notre dataclass commentaire
                liste_objet_positif.append(commentaire_positif)
                i+=1
                if i == 244:
                    break
    print(f'{len(liste)}')
    
    try:
        for i, element in enumerate(liste): 
            element = element.lower()
            with open(f"{chemin_resultat}/commentaire_positif_{i}.txt", 'w', encoding='UTF-8') as resultat:
                resultat.write(element.strip())
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
        if commentaire_français(texte):
            mots = texte.split()

            if len(mots) >= 10: 
                liste.append(element.get_text())
                commentaire_negatif = Commentaire(id_fichier=i, sentiment="negatif", commentaire=texte, )
                commentaire_negatif = Commentaire(id_fichier=i, sentiment="negatif", commentaire=texte)
                liste_objet_negatif.append(commentaire_negatif)
                i+= 1
                if i == 244: ## on récupère 245 commentaires négatifs afin d'avoir le même nombre de commentaires négatifs et positifs
                    break
    print(f'{len(liste)}')
    
    try:
        for i, element in enumerate(liste):
            element = element.lower() ## on met tout en minuscule pour éviter les erreurs avec langdetect
            with open(f"{chemin_resultat}/commentaire_negatif_{i}.txt", 'w', encoding='UTF-8') as resultat:
                resultat.write(element.strip())
    except Exception as e:
        print(f"Il y'a eu une erreur : {e}")
    return liste_objet_negatif
def ecrire_commentaire_csv(liste_commentaires, nom_fichier):
    """ecriture des commentaires dans notre csv"""
    
    with open(nom_fichier, mode='w', newline='', encoding='UTF-8') as file:
        writer = csv.writer(file)
        writer.writerow(['id_fichier', 'sentiment', 'commentaire'])  
        for commentaire in liste_commentaires:
            writer.writerow([commentaire.id_fichier, commentaire.sentiment, commentaire.commentaire])  

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