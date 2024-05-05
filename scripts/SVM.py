import nltk

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import confusion_matrix
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from nltk.corpus import stopwords

from construire_csv import pretraitement


def SVM(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # TF-IDF
    nltk.download("stopwords")
    stop_words = stopwords.words("french")
    stop_words.remove("pas")
    stop_words.remove("ne")
    vectorizer = TfidfVectorizer(stop_words=stop_words)
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    # Création du modèle SVM 
    # type de noyau : linéaire / polynomial / radial
    # C = constante de régularisation  qui comntrôle maximisation de la marge et de la 
    # minimisation des erreurs de classification
    clf = SVC(kernel="rbf", C=1.0)

    # Entraîne le modèle sur l'ensemble d'entraînement
    clf.fit(X_train_tfidf, y_train)
    y_pred = clf.predict(X_test_tfidf)
    classification = classification_report(y_test, y_pred)

    # VP = []
    # FP = []
    # VN = []
    # FN = []

    # for phrase, vraie_valeur, prediction in zip(???["textes"], ???[???], y_pred):

    #     if vraie_valeur == 1 and prediction == 1:
    #         VP.append((phrase, vraie_valeur, prediction))
    #     elif vraie_valeur == 0 and prediction == 1:
    #         FP.append((phrase, vraie_valeur, prediction))
    #     elif vraie_valeur == 0 and prediction == 0:
    #         VN.append((phrase, vraie_valeur, prediction))
    #     elif vraie_valeur == 1 and prediction == 0:
    #        FN.append((phrase, vraie_valeur, prediction))

    # Matrice de confusion
    matrice = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(matrice, annot=True, fmt="d", cmap="PuRd")
    plt.xlabel("Prédit")
    plt.ylabel("Vrai")
    plt.title("Matrice de confusion SVM lemmatisée")
    plt.savefig("../images/matrice_SVM_lemmatise.png")

    return classification


def main():
    # X, y = pretraitement("../data/commentaires_positifs/commentaires_positifs.csv", "../data/commentaires_negatifs/commentaires_negatifs.csv")
    X, y = pretraitement("../data/commentaires_positifs/commentaires_positifs.csv", "../data/commentaires_negatifs/commentaires_negatifs.csv")
    print(SVM(X, y))


if __name__ == "__main__":
    main()