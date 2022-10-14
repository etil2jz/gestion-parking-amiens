import csv
import os
import sys

# La structure parks est remplie des données de parking du fichier parking-metropole.txt
# Cela donne concrètement des tableaux dans un tableau (parks[0][0] retourne 'AMN0000')
parks = []

def chargerFichierParking():
    with open(os.path.join(sys.path[0], 'parking-metropole.txt'), 'r') as fichierParking:
        lecture = csv.reader(fichierParking, delimiter = '	')
        next(lecture)
        for ligne in lecture:
            parks.append(ligne)
    print(parks) #print de debug

def main():
    print('\n======================================\nBienvenue sur Amiens Métropole CarPark\n======================================\n')
    chargerFichierParking()

main()