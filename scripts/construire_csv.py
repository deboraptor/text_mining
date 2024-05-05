import csv
import os
import spacy
import pandas as pd


nlp = spacy.load("fr_core_news_sm")

def construire_csv(chemin_dossier, csv_chemin):
    with open(csv_chemin, "w", newline="", encoding="utf-8") as fichier_csv:
        writer = csv.writer(fichier_csv)
        for nom_fichier in os.listdir(chemin_dossier):
            if nom_fichier.endswith(".txt"):
                with open(os.path.join(chemin_dossier, nom_fichier), "r", encoding="utf-8") as fichier_txt:
                    contenu = fichier_txt.read()
                    writer.writerow([contenu])


mots_a_exclure = ["ajd", "bcp", "bjr", "c", "chui", "dc", "dsl", "ds", "g", "mdr", "mdrr", "mnt", "mwa", "nrv", "osef", "pcq", "psk", "pck", "pb", "pk", "pq", "prk", "pr", "ptdr", "ptdrr", "srx", "stp", "svp", "tlm", "tjrs", "tjs", "tjr", "mod", "arpg", "antialiasing", "hotfixe", "gameplay"]


def lemmatiser_csv(csv_chemin_entree, dossier_sortie, mots_a_exclure):
    nom_fichier_sortie = os.path.basename(csv_chemin_entree).replace(".csv", "_lemmatises.csv")
    csv_chemin_sortie = os.path.join(dossier_sortie, nom_fichier_sortie)

    with open(csv_chemin_entree, "r", newline="", encoding="utf-8") as fichier_csv_entree:
        reader = csv.reader(fichier_csv_entree)
        with open(csv_chemin_sortie, "w", newline="", encoding="utf-8") as fichier_csv_sortie:
            writer = csv.writer(fichier_csv_sortie)
            for ligne in reader:
                contenu = ligne[0]
                doc = nlp(contenu)
                tokens_lemmatise = [token.lemma_ if token.text not in mots_a_exclure else token.text for token in doc]
                contenu_lemmatise = " ".join(tokens_lemmatise)
                writer.writerow([contenu_lemmatise])


def pretraitement(csv_pos, csv_neg):
    df_pos = pd.read_csv(csv_pos, header=None, encoding="utf-8")
    df_neg = pd.read_csv(csv_neg, header=None, encoding="utf-8")
    df = pd.concat([df_pos, df_neg], ignore_index=True)

    # Ajoute une colonne pour les étiquettes de classe (0 pour négatif, 1 pour positif)
    df["label"] = [0] * len(df_neg) + [1] * len(df_pos)

    # les caractéristiques : fréquences des mots ou n-grammes
    X = df[0]
    # les classes : positif ou negatif
    y = df["label"]

    return X, y


def main():
    construire_csv("../data/commentaires_negatifs", "../data/commentaires_negatifs/commentaires_negatifs.csv")
    construire_csv("../data/commentaires_positifs", "../data/commentaires_positifs/commentaires_positifs.csv")

    lemmatiser_csv("../data/commentaires_positifs/commentaires_positifs.csv", "../data/commentaires_positifs_lemmatises", mots_a_exclure)
    lemmatiser_csv("../data/commentaires_negatifs/commentaires_negatifs.csv", "../data/commentaires_negatifs_lemmatises", mots_a_exclure)

    X, y = pretraitement("../data/commentaires_positifs_lemmatises/commentaires_positifs_lemmatises.csv", "../data/commentaires_negatifs_lemmatises/commentaires_negatifs_lemmatises.csv")
    print("C'est fini !")


if __name__ == "__main__":
    main()
