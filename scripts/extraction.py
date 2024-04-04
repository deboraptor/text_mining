"""
Récupération des commentaires steams sur Portal 2
auteurs : Baptiste et Débora
"""

from pathlib import Path
from bs4 import BeautifulSoup 
from langdetect import detect


    ##questions de prétraitement :
    ## - les qcm
    ## les emojis 
    ## les images avec dessinées avec des ___
    ## ne prendre en compte que les commentaires avec un certains nombre de mots : FAIT
    ## certains coms restent en anglais

def traitement_des_langues(chemin_resultat : str | Path) -> bool:

    print(len(chemin_resultat))
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


def chargement_commentaire_positif(soup : BeautifulSoup, chemin_resultat : str | Path) -> None:

    # surement pas la meilleure technique j'avais des problemes pour manipuler le tag cela m'indiquait que c'était un tag et non un str du coup j'ai fait une liste

    tag = soup.find_all(attrs={'class':'apphub_CardTextContent'})
    liste = []
    for element in tag:
        texte = element.get_text()
        texte = texte.lower()
        mots = texte.split()
        if len(mots) >= 10: # il doit y avoir plus de 10 mots dans le commentaire pour être pris en comtpe
            liste.append(element.get_text())
    try:
        for i, element in enumerate(liste[:20]): # on veut prendre que les 20 premiers commentaires
            element = element.lower() # on met tout en minuscule pour éviter les erreurs avec langdetect
            with open(f"{chemin_resultat}/commentaire_positif_{i}.txt", 'w', encoding='UTF8') as resultat:
                resultat.write(element.strip())
                if not traitement_des_langues(resultat.name):
                    # on supprime le fichier si c'est pas en français
                    resultat.close()
                    Path(resultat.name).unlink()
    except Exception as e:
        print(f"Il y'a eu une erreur : {e}")


def chargement_commentaire_negatif(soup : BeautifulSoup, chemin_resultat : str | Path):
    """même principe que la fonction commentaire positif"""

    # surement pas la meilleure technique j'avais des problemes pour manipuler le tag cela m'indiquait que c'était un tag et non un str du coup j'ai fait une liste

    tag = soup.find_all(attrs={'class':'apphub_CardTextContent'})
    liste = []
    for element in tag:
        texte = element.get_text()
        mots = texte.split()
        if len(mots) >= 10: # il doit y avoir plus de 10 mots dans le commentaire pour être pris en compte
            liste.append(element.get_text())
    try:
        for i, element in enumerate(liste[:20]): # on veut prendre que les 20 premiers commentaires
            element = element.lower() # on met tout en minuscule pour éviter les erreurs avec langdetect
            with open(f"{chemin_resultat}/commentaire_negatif_{i}.txt", 'w', encoding='UTF8') as resultat:
                resultat.write(element.strip())
    except Exception as e:
        print(f"Il y'a eu une erreur : {e}")


def main():
    resultat_pretraitement_positif = pretraitement("./positive_comments/page/Communauté Steam Portal 2.html") 
    chargement_commentaire_positif(resultat_pretraitement_positif, "./positive_comments")
    resultat_pretraitement_negatif = pretraitement("./negative_comments/page/Communauté Steam Portal 2.html")
    chargement_commentaire_negatif(resultat_pretraitement_negatif, "./negative_comments/") 


if __name__ == "__main__":
    main()