"""récupération des commentaires steams sur Portal 2"""

from pathlib import Path
from bs4 import BeautifulSoup 

    ##questions de prétraitement :
    ## - les qcm
    ## les emojis 
    ## les images avec dessinées avec des ___
    ## ne prendre en compte que les commentaires avec un certains nombre de mots : FAIT
    ## certains coms restent en anglais

def pretraitement(page_html: str | Path) -> str:

   ## prétraitement : 
    ##il faut supprimer le tag date_posted car le résultat est moche et on ne le veut pas, il est contenu dans la balise qui contient le commentaire

    with open(page_html, 'r' ) as f:
        soup = BeautifulSoup(f, "html.parser", multi_valued_attributes=None)

    for tag in soup.find_all("div", class_="date_posted"):
        tag.decompose()
    return soup

def chargement_commentaire_positif(soup : BeautifulSoup, chemin_resultat : str | Path) -> None:

    ##surement pas la meilleure technique j'avais des problemes pour manipuler le tag cela m'indiquait que c'était un tag et non un str du coup j'ai fait une liste

    tag = soup.find_all(attrs={'class':'apphub_CardTextContent'})
    liste = []
    for element in tag:
        texte = element.get_text()
        mots = texte.split()
        if len(mots) >= 10: ##il doit y avoir plus de 10 mots dans le commentaire pour être pris en comtpe
            liste.append(element.get_text())

    try:
        for i,element in enumerate(liste):
            with open(f"{chemin_resultat}/commentaire_positif_{i}", 'w', encoding='UTF8') as resultat:
                resultat.write(element.strip())
    except Exception as e:
        print(f"Il y'a eu une erreur : {e}")


def chargement_commentaire_negatif(soup : BeautifulSoup, chemin_resultat : str | Path):
    """même principe que la fonction commentaire positif"""

    ##surement pas la meilleure technique j'avais des problemes pour manipuler le tag cela m'indiquait que c'était un tag et non un str du coup j'ai fait une liste

    
    tag = soup.find_all(attrs={'class':'apphub_CardTextContent'})
    liste = []
    for element in tag:
        texte = element.get_text()
        mots = texte.split()
        if len(mots) >= 10: ##il doit y avoir plus de 10 mots dans le commentaire pour être pris en compte
            liste.append(element.get_text())
    try:
        for i,element in enumerate(liste):
            with open(f"{chemin_resultat}/commentaire_negatif_{i}", 'w', encoding='UTF8') as resultat:
                resultat.write(element.strip())
    except Exception as e:
        print(f"Il y'a eu une erreur : {e}")

def main():

    resultat_pretraitement_positif = pretraitement("./positif_comments/page/Communauté Steam Portal 2.html") 
    chargement_commentaire_positif(resultat_pretraitement_positif, "./positif_comments")
    resultat_pretraitement_negatif = pretraitement("./negative_comments/page/Communauté Steam Portal 2.html")
    chargement_commentaire_negatif(resultat_pretraitement_negatif, "./negative_comments/") 
    print("tout s'est bien passé bonhomme ! ")


if __name__ == "__main__":
    main()