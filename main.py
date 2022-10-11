import csv

# La structure parks est remplie des données de parking du fichier parking-metropole.txt
# Cela donne concrètement un tableau à 2 dimensions (parks[0][0] retourne 'Identifiant')
parks = []

def chargerFichierParking():
    with open("parking-metropole.txt", "r") as fichierParking:
        lecture = csv.reader(fichierParking, delimiter = '	')
        next(lecture)
        for ligne in lecture:
            parks.append(ligne)
    print(parks)

def main():
    print("\n=============================================\nBienvenue sur Amiens Métropole CarPark Valpha\n=============================================\n")
    chargerFichierParking()

main()