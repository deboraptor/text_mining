"""Ce script est juste un petit bonus où nous avons entrainé notre modele naives bayes 
et écrivons manuellement des commentaires et il doit deviner si c'est positif ou négatif"""


import pandas as pd
import nltk 
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn import naive_bayes
from sklearn.metrics import roc_auc_score
import numpy as np



df = pd.read_csv("../data/commentaires.csv", sep=",", skiprows=1, usecols=[1, 2],names=['sentiment', 'commentaire'])

print(df.head())
                 
## nous allons vectoriser notre texte en utilisant tfidf la variable sentiment est notre variable dépendante
## et on entrainer notre naive bayes classifier a donné sentiment positif ou négatif basé sur le commentaire

french_stop_words = stopwords.words('french')
vectorizer = TfidfVectorizer(use_idf=True, lowercase=True, strip_accents='ascii', stop_words=french_stop_words)



y = df.sentiment ##on définit notre variable dépendante

x = vectorizer.fit_transform(df.commentaire)

# print(y.shape)
# print(x.shape)

x_train, x_test, y_train, y_test = train_test_split(x, y)

## entrainement du naive bayes classifieur

clf = naive_bayes.MultinomialNB()
clf.fit(x_train, y_train)


## tester la présicion de notre modele 
 
print(roc_auc_score(y_test, clf.predict_proba(x_test)[:,1]))

commentaire = np.array(["Ce jeu est trop nul franchement !"])
commentaire_vecteur = vectorizer.transform(commentaire)

print(clf.predict(commentaire_vecteur))