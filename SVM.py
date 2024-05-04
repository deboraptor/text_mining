# from sklearn import svm
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler

# import glob
# import numpy as np


# #############################################################
# # on tranforme les .txt en matrices exploitables par l'algo #
# #############################################################

# # Liste des fichiers txt
# commentaires_negatifs = glob.glob("./data/commentaire_negatif/*")
# commentaires_positifs = glob.glob("./data/commentaire_positif/*")


# # les caractéristiques : fréquences des mots ou n-grammes
# X = []

# # les classes : positif ou negatif
# y = []

# # Lecture des données à partir de chaque fichier txt
# for file in files:
#     data = np.loadtxt(file)
#     X.append(data[:, :-1])
#     y.append(data[:, -1])

# # Conversion des listes en matrices
# X = np.concatenate(X)
# y = np.concatenate(y)

# ############
# # algo SVM #
# ############

# # Données d'origine
# X = [[0, 1], [1, 0], [1, 1], [2, 2], [3, 3]]
# y = [0, 0, 1, 1, 1]

# # Séparation des données en ensembles d'entraînement et de test
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

# # Normalisation des données : éviter que certaines caaractéristiques ne dominent les autres
# #On veut que chaque échantillon ait une moyenne de 0 et une variance de 1
# scaler = StandardScaler()
# X_train = scaler.fit_transform(X_train)
# X_test = scaler.transform(X_test)

# # Création du modèle SVM : 
# # type de noyau : linéaire / polynomial / radial
# # C = constante de régularisation  qui comntrôle maximisation de la marge et de la 
# # minimisation des erreurs de classification
# clf = svm.SVC(kernel='linear', C=1.0)

# # Entraînement du modèle
# clf.fit(X_train, y_train)

# # Évaluation du modèle
# y_pred = clf.predict(X_test)

# # Affichage des résultats
# print('Précision :', clf.score(X_test, y_test))
# print('Rappel :', metrics.recall_score(y_test, y_pred))
# print('F1-score :', metrics.f1_score(y_test, y_pred))

##############################################

# import os
# import numpy as np
# import nltk
# from nltk.corpus import stopwords
# from nltk.stem import SnowballStemmer
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler
# from sklearn.svm import SVC
# from sklearn.metrics import classification_report
# from keras.preprocessing.sequence import pad_sequences

# # Répertoire contenant les fichiers de commentaires positifs et négatifs
# data_dir = "./data"

# # Liste vide pour stocker les caractéristiques des commentaires
# X = []

# # Liste vide pour stocker les étiquettes de classe (0 pour négatif, 1 pour positif)
# y = []

# # Liste des stop words à supprimer
# stop_words = set(stopwords.words('french'))

# # Stemmer pour réduire les mots à leur racine
# stemmer = SnowballStemmer('french')

# # Parcours les fichiers dans les deux dossiers "positif" et "négatif"
# for label in ['commentaire_negatif', 'commentaire_positif']:
#     for file in os.listdir(os.path.join(data_dir, label)):
#         # Lit le contenu du fichier
#         with open(os.path.join(data_dir, label, file), 'r') as f:
#             text = f.read()

#         # Tokenise le texte en mots
#         tokens = nltk.word_tokenize(text.lower())

#         # Supprime les stop words et les ponctuations
#         tokens = [token for token in tokens if token not in stop_words and token.isalnum()]

#         # Réduit les mots à leur racine
#         tokens = [stemmer.stem(token) for token in tokens]

#         # Calcule la fréquence des mots comme caractéristiques
#         freqs = nltk.FreqDist(tokens)
#         features = np.array([freqs[token] for token in freqs.keys()])

#         # Ajoute les caractéristiques et l'étiquette de classe à la liste correspondante
#         X.append(features)
#         y.append(1 if label == 'positif' else 0)

# # Calcule la longueur maximale des séquences
# max_len = max([len(seq) for seq in X])

# # Ajoute des zéros à la fin des séquences les plus courtes pour qu'elles aient la même longueur que les séquences les plus longues
# X = pad_sequences(X, maxlen=max_len, padding='post', truncating='post')

# # Normalise les caractéristiques
# X = StandardScaler().fit_transform(X)

# # Divise les données en ensembles d'entraînement et de test
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Crée un modèle SVM avec un noyau radial et une constante de régularisation C égale à 1
# clf = SVC(kernel='rbf', C=1.0)

# # Entraîne le modèle sur l'ensemble d'entraînement
# clf.fit(X_train, y_train)

# # Évalue la performance du modèle sur l'ensemble de test
# y_pred = clf.predict(X_test)
# print(classification_report(y_test, y_pred))


###########################################
# import os
# import csv


# chemin_dossier = './data/commentaire_negatif'
# csv_chemin = './data/commentaire_negatif/commentaires_negatifs.csv'

# with open(csv_chemin, 'w', newline='', encoding='utf-8') as csvfile:
#     writer = csv.writer(csvfile)
#     for nom_fichier in os.listdir(chemin_dossier):
#         if nom_fichier.endswith(".txt"):
#             with open(os.path.join(chemin_dossier, nom_fichier), 'r', encoding='utf-8') as txtfile:
#                 contenu = txtfile.read()
#                 writer.writerow([contenu])

###############################################################

import pandas as pd
import numpy as np
import nltk
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from nltk.corpus import stopwords

# Charge les données à partir des fichiers CSV
df_pos = pd.read_csv('./data/commentaire_positif/commentaires_positif.csv', header=None, encoding='utf-8')
df_neg = pd.read_csv('./data/commentaire_negatif/commentaires_negatifs.csv', header=None, encoding='utf-8')

# Concatène les deux dataframes en un seul
df = pd.concat([df_pos, df_neg], ignore_index=True)

# Ajoute une colonne pour les étiquettes de classe (0 pour négatif, 1 pour positif)
df['label'] = [0] * len(df_neg) + [1] * len(df_pos)

# Sépare les données en deux ensembles : commentaires et étiquettes
X = df[0]
y = df['label']

# Divise les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Vectorise les commentaires en utilisant TF-IDF
nltk.download('stopwords')
stop_words = stopwords.words('french')
vectorizer = TfidfVectorizer(stop_words=stop_words)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Entraîne un modèle SVM avec un noyau RBF
clf = SVC(kernel='rbf', C=1.0)
clf.fit(X_train_tfidf, y_train)

# Évalue les performances du modèle sur l'ensemble de test
y_pred = clf.predict(X_test_tfidf)
print(classification_report(y_test, y_pred))
