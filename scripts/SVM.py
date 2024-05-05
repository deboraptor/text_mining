import pandas as pd
import nltk

from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
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
    return classification


def main():
    print(SVM(X, y))


if __name__ == "__main__":
    main()