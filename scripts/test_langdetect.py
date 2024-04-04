from langdetect import detect
import glob


path = glob.glob("./negative_comments/*.txt")

# on a 20 fichiers en tout
print(len(path))

for file in path:
    with open(file, "r") as f:
        content = f.read()
        langue = detect(content)
        if langue == 'fr':
            print(f"{file}\t{detect(content)}")
        else:
            print(f"On a skip cette langue : {langue}")

# Voici notre output
# Je vérifie à la main si c'est correct
# ./negative_comments/commentaire_negatif_5.txt   fr -> c'est bon 
# ./negative_comments/commentaire_negatif_19.txt  fr -> c'est bon 
# ./negative_comments/commentaire_negatif_12.txt  en -> c'est bon 
# ./negative_comments/commentaire_negatif_15.txt  fr -> c'est bon 
# ./negative_comments/commentaire_negatif_14.txt  en -> PAS BON
# ./negative_comments/commentaire_negatif_0.txt   fr -> c'est bon 
# ./negative_comments/commentaire_negatif_3.txt   en -> c'est bon 
# ./negative_comments/commentaire_negatif_10.txt  fr -> c'est bon 
# ./negative_comments/commentaire_negatif_8.txt   fr -> c'est bon 
# ./negative_comments/commentaire_negatif_2.txt   fr -> c'est bon 
# ./negative_comments/commentaire_negatif_9.txt   fr -> c'est bon 
# ./negative_comments/commentaire_negatif_11.txt  fr -> c'est bon 
# ./negative_comments/commentaire_negatif_13.txt  fr -> c'est bon 
# ./negative_comments/commentaire_negatif_6.txt   fr -> c'est bon 
# ./negative_comments/commentaire_negatif_7.txt   fr -> c'est bon 
# ./negative_comments/commentaire_negatif_4.txt   fr -> c'est bon 
# ./negative_comments/commentaire_negatif_1.txt   en -> c'est bon 
# ./negative_comments/commentaire_negatif_17.txt  fr -> c'est bon 
# ./negative_comments/commentaire_negatif_16.txt  fr -> c'est bon 
# ./negative_comments/commentaire_negatif_18.txt  en -> PAS BON
# On peut voir que 14 et 18 sont écrits en français et qu'ils ont été détectés en anglais..
# C'est peut-être parce que les deux sont entièrement écrit en majuscule ? 
# Oui !! Après avoir tout mis en minscule c'est bon !! -> solution, tout traiter en minuscule

# ./negative_comments/commentaire_negatif_5.txt   fr
# ./negative_comments/commentaire_negatif_19.txt  fr
# ./negative_comments/commentaire_negatif_12.txt  en
# ./negative_comments/commentaire_negatif_15.txt  fr
# ./negative_comments/commentaire_negatif_14.txt  fr
# ./negative_comments/commentaire_negatif_0.txt   fr
# ./negative_comments/commentaire_negatif_3.txt   en
# ./negative_comments/commentaire_negatif_10.txt  fr
# ./negative_comments/commentaire_negatif_8.txt   fr
# ./negative_comments/commentaire_negatif_2.txt   fr
# ./negative_comments/commentaire_negatif_9.txt   fr
# ./negative_comments/commentaire_negatif_11.txt  fr
# ./negative_comments/commentaire_negatif_13.txt  fr
# ./negative_comments/commentaire_negatif_6.txt   fr
# ./negative_comments/commentaire_negatif_7.txt   fr
# ./negative_comments/commentaire_negatif_4.txt   fr
# ./negative_comments/commentaire_negatif_1.txt   en
# ./negative_comments/commentaire_negatif_17.txt  fr
# ./negative_comments/commentaire_negatif_16.txt  fr
# ./negative_comments/commentaire_negatif_18.txt  fr
# C'est donc un 100% de réussite !