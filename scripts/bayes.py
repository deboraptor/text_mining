import nltk
from nltk.corpus import stopwords 
nltk.download('stopwords')

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.naive_bayes import MultinomialNB
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd





def entrainement():

    french_stop_words = stopwords.words('french')

    corpus_dataframe = pd.read_csv('../data/commentaires.csv', header=0, sep=",", usecols=[1,2], names=['sentiment','commentaire'])
    corpus_dataframe = corpus_dataframe.dropna(subset=['sentiment'])
    train_corpus, test_corpus = train_test_split(corpus_dataframe, test_size=0.25, random_state=42, stratify=corpus_dataframe['commentaire'])

    model = make_pipeline(TfidfVectorizer(stop_words=french_stop_words), MultinomialNB())  
    model.fit(train_corpus['sentiment'], train_corpus['commentaire'])
    test_evaluation = model.predict(test_corpus['sentiment'])

    print("Taux d'accuracy :", accuracy_score(test_corpus['commentaire'], test_evaluation))
    print("Classification Report:")
    print(classification_report(test_corpus['commentaire'], test_evaluation))

    return test_evaluation, test_corpus

def matrice_de_confusion(test_evaluation, test_corpus):


    matrice = confusion_matrix(test_corpus['commentaire'], test_evaluation)
    sns.heatmap(matrice, square=True, annot=True, fmt='d',cmap='Spectral', cbar=False, xticklabels=['Positif (P)', 'Négatif (N)'], yticklabels=['Positif (P)', 'Négatif (N)'])
    plt.xlabel('Vraies valeurs')
    plt.ylabel('Valeurs prédites')
    plt.title('Matrice de confusion')
    plt.show()



def main():

    evaluation, corpus = entrainement()
    matrice_de_confusion(evaluation, corpus)


if __name__ == "__main__":
    main()
