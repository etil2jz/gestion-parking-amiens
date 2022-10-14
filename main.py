import csv
import os
import sys

# La structure parks est remplie des données de parking du fichier parking-metropole.txt
# Cela donne concrètement des tableaux dans un tableau (parks[0][0] retourne 'AMN0000')
parks = []
nbParkingsTotal = 0
nbParkingsAmiens = 0
nbParkingsAlbert = 0
nbParkingsAbbeville = 0

with open(os.path.join(sys.path[0], 'parking-metropole.txt'), 'r') as fichierParking:
    lecture = csv.reader(fichierParking, delimiter = '\t')
    next(lecture)
    i = 0
    for ligne in lecture:
        parks.append(ligne)
        nbParkingsTotal += 1
        if parks[i][3] == 'Amiens': nbParkingsAmiens += 1
        if parks[i][3] == 'Albert': nbParkingsAlbert += 1
        if parks[i][3] == 'Abbeville': nbParkingsAbbeville += 1
        i += 1

def infoParkings():
    print('Nombre total de parkings: ' + str(nbParkingsTotal))
    print('Parkings à Amiens: ' + str(nbParkingsAmiens))
    print('Parkings à Albert: ' + str(nbParkingsAlbert))
    print('Parkings à Abbeville: ' + str(nbParkingsAbbeville))

def rechercheStationnement():
    ville = input('\nDans quelle ville souhaitez-vous stationner ?\n> ')
    print("\nVoici la liste des parkings d'" + ville + " :\n")
    for i in range(27):
        if parks[i][3] == ville:
            print(parks[i][0] + ' - ' + parks[i][1] + ' - ' + parks[i][2] + ' - ' + parks[i][4])
    choixParking = input("\nEntrez l'identifiant du parking désiré :\n> ")
    return choixParking

infoParkings()
print('\n======================================\nBienvenue sur Amiens Métropole CarPark\n======================================\n\n1. Rechercher un stationnement')
choix = input('> ')
if choix == '1': choixParking = rechercheStationnement()