import nltk

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import confusion_matrix
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from nltk.corpus import stopwords

from construire_csv import pretraitement

def multinomial_naive_bayes(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # TF-IDF
    nltk.download("stopwords")
    stop_words = stopwords.words("french")
    stop_words.remove("pas")
    stop_words.remove("ne")

    vectorizer = TfidfVectorizer(stop_words=stop_words)
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    # Création du modèle Multinomial Naive Bayes
    clf = MultinomialNB()

    # Entraîne le modèle sur l'ensemble d'entraînement
    clf.fit(X_train_tfidf, y_train)
    y_pred = clf.predict(X_test_tfidf)

    classification = classification_report(y_test, y_pred)

    # Matrice de confusion
    matrice = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(matrice, annot=True, fmt="d", cmap="Reds")
    plt.xlabel("Prédit")
    plt.ylabel("Vrai")
    plt.title("Matrice de confusion Naive Bayes")
    plt.savefig("../images/matrice_naive_bayes.png")

    return classification


def main():
    # X, y = pretraitement("../data/commentaires_positifs_lemmatises/commentaires_positifs_lemmatises.csv", "../data/commentaires_negatifs_lemmatises/commentaires_negatifs_lemmatises.csv")
    X, y = pretraitement("../data/commentaires_positifs/commentaires_positifs.csv", "../data/commentaires_negatifs/commentaires_negatifs.csv")
    
    print(multinomial_naive_bayes(X, y))


if __name__ == "__main__":
    main()