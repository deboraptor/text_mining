import pandas as pd
import numpy as np
import nltk
import os
import csv
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
from sklearn.pipeline import make_pipeline
from nltk.corpus import stopwords





def construire_csv(chemin_dossier, csv_chemin):
    with open(csv_chemin, 'w', newline='', encoding='utf-8') as fichier_csv:
        writer = csv.writer(fichier_csv)
        for nom_fichier in os.listdir(chemin_dossier):
            if nom_fichier.endswith(".txt"):
                with open(os.path.join(chemin_dossier, nom_fichier), 'r', encoding='utf-8') as fichier_txt:
                    contenu = fichier_txt.read()
                    writer.writerow([contenu])


def pretraitement(csv_pos, csv_neg):
    df_pos = pd.read_csv(csv_pos, header=None, encoding='utf-8')
    df_neg = pd.read_csv(csv_neg, header=None, encoding='utf-8')
    df = pd.concat([df_pos, df_neg], ignore_index=True)

    # Ajoute une colonne pour les étiquettes de classe (0 pour négatif, 1 pour positif)
    df['label'] = [0] * len(df_neg) + [1] * len(df_pos)

    # les caractéristiques : fréquences des mots ou n-grammes
    X = df[0]
    # les classes : positif ou negatif
    y = df['label']

    return X, y


def SVM(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # TF-IDF
    nltk.download('stopwords')
    stop_words = stopwords.words('french')
    stop_words.remove("pas")
    vectorizer = make_pipeline(TfidfVectorizer(stop_words=stop_words), MultinomialNB)
    X_train_tfidf = vectorizer.fit(X_train)
    # X_test_tfidf = vectorizer.transform(X_test)

    # Création du modèle SVM 
    # type de noyau : linéaire / polynomial / radial
    # C = constante de régularisation  qui comntrôle maximisation de la marge et de la 
    # minimisation des erreurs de classification
  

    # Entraîne le modèle sur l'ensemble d'entraînement
    vectorizer.fit(X_train_tfidf, y_train)
    y_pred = vectorizer.predict(X)

    classification = classification_report(y_test, y_pred)
    return classification


def main():
    construire_csv("../data/commentaire_negatif", "../data/commentaire_negatif/commentaires_negatifs.csv")
    construire_csv("../data/commentaire_positif", "../data/commentaire_positif/commentaires_positif.csv")
    X, y = pretraitement("../data/commentaire_positif/commentaires_positif.csv", "../data/commentaire_negatif/commentaires_negatifs.csv")
    print(SVM(X, y))


if __name__ == "__main__":
    main()