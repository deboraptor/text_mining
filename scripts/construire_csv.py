import csv
import os


def construire_csv(chemin_dossier, csv_chemin):
    with open(csv_chemin, 'w', newline='', encoding='utf-8') as fichier_csv:
        writer = csv.writer(fichier_csv)
        for nom_fichier in os.listdir(chemin_dossier):
            if nom_fichier.endswith(".txt"):
                with open(os.path.join(chemin_dossier, nom_fichier), 'r', encoding='utf-8') as fichier_txt:
                    contenu = fichier_txt.read()
                    writer.writerow([contenu])

def main():
    construire_csv("./data/commentaire_negatif", "./data/commentaire_negatif/commentaires_negatifs.csv")

if __name__ == "__main__":
    main()