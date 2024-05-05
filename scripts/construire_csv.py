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


def lemmatiser_csv(csv_chemin_entree, csv_chemin_sortie):
    with open(csv_chemin_entree, "r", newline="", encoding="utf-8") as fichier_csv_entree:
        reader = csv.reader(fichier_csv_entree)

        with open(csv_chemin_sortie, "w", newline="", encoding="utf-8") as fichier_csv_sortie:
            writer = csv.writer(fichier_csv_sortie)

            for ligne in reader:
                contenu = ligne[0]
                doc = nlp(contenu)
                tokens_lemmatise = [token.lemma_ for token in doc]
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
    X, y = pretraitement("../data/commentaire_positif/commentaires_positif.csv", "../data/commentaire_negatif/commentaires_negatifs.csv")
    construire_csv("../data/commentaire_negatif", "../data/commentaire_negatif/commentaires_negatifs.csv")

if __name__ == "__main__":
    main()