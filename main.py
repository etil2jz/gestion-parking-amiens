import csv
import os
import platform
import sys
import socket
import struct
import datetime
import time


# parks est remplie des données de parking du fichier parking-metropole.txt
# Cela donne concrètement des tableaux dans un tableau (parks[0][0] retourne 'AMN0000')
parks = []

# Variables globales afin de garder en mémoire le nombre de parkings par ville
# On peut les afficher avec la fonction infoParkings()
nbParkingsTotal = 0
nbParkingsAmiens = 0
nbParkingsAlbert = 0
nbParkingsAbbeville = 0

drivers = [] # Liste drivers vide qui sera remplie au fur et à mesure d'objets clients

# La classe clients est remplie des données concernant les automobilistes
# Cela comprend l'identifiant du parking, la plaque du véhicule, la date et heure d'entrée
class clients:
    def __init__(self, choixParking, numPlaque, temps):
        self.idParking = choixParking
        self.plaque = numPlaque
        self.date = temps
    def __repr__(self):
        return 'idParking: %s - plaque: %s - date: %s' % (self.idParking, self.plaque, self.date)

# Ouverture du fichier parking-metropole.txt en lecture
# afin d'importer ses données dans parks
with open(os.path.join(sys.path[0], 'parking-metropole.txt'), 'r') as fichierParking:
    lecture = csv.reader(fichierParking, delimiter = '\t')
    next(lecture)
    i = 0
    for ligne in lecture:
        parks.append(ligne)
        nbParkingsTotal += 1
        if parks[i][3] == 'Amiens': nbParkingsAmiens += 1
        elif parks[i][3] == 'Albert': nbParkingsAlbert += 1
        elif parks[i][3] == 'Abbeville': nbParkingsAbbeville += 1
        i += 1

# Fonction pour récupérer le temps OFFICIEL dans le cas où
# l'utilisateur serait tenté de modifier son heure locale
def temps():
    REF_TIME_1970 = 2208988800
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = b'\x1b' + 47 * b'\0'
    client.sendto(data, ('0.fr.pool.ntp.org', 123))
    data, address = client.recvfrom(1024)
    if data:
        t = struct.unpack('!12I', data)[10]
        t -= REF_TIME_1970
    return datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S+01:00')

# Fonction pour vider le terminal à des fins esthétiques
# cls sous Windows et clear sous Linux / Mac OS
def clear():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def infoParkings():
    print('Nombre total de parkings: ' + str(nbParkingsTotal))
    print('Parkings à Amiens: ' + str(nbParkingsAmiens))
    print('Parkings à Albert: ' + str(nbParkingsAlbert))
    print('Parkings à Abbeville: ' + str(nbParkingsAbbeville))

def rechercheStationnement():
    cool = 1
    while True:
        ville = input('\nDans quelle ville souhaitez-vous stationner ?\n> ')
        clear()
        if ville == 'Amiens': break
        elif ville == 'Albert': break
        elif ville == 'Abbeville': break
    print("\nVoici la liste des parkings d'" + ville + " :\n")
    for i in range(27):
        if parks[i][3] == ville:
            print(parks[i][0] + ' - ' + parks[i][1] + ' - ' + parks[i][2] + ' - ' + parks[i][4])
    choixParking = input("\nEntrez l'identifiant du parking désiré (0 pour abandonner) :\n> ")
    #debut anti-con choix parking
    if ville == 'Amiens':
        for i in range(18):
            if choixParking == parks[0][0] or parks[1][0] or parks[2][0] or parks[3][0] or parks[4][0] or parks[5][0] or parks[5][0] or parks[6][0] or parks[7][0] or parks[8][0] or parks[9][0] or parks[10][0] or parks[11][0] or parks[12][0] or parks[13][0] or parks[14][0] or parks[15][0] or parks[16][0] or parks[17][0] or parks[18][0]:            
                print("amiens")
                break
            if choixParking == parks[i][0]:
                print("Tu t'es pas troper mon con\n" + str(i))
                break
            if choixParking != parks[0][0] or parks[1][0] or parks[2][0] or parks[3][0] or parks[4][0] or parks[5][0] or parks[5][0] or parks[6][0] or parks[7][0] or parks[8][0] or parks[9][0] or parks[10][0] or parks[11][0] or parks[12][0] or parks[13][0] or parks[14][0] or parks[15][0] or parks[16][0] or parks[17][0] or parks[18][0]:            
                print("Sale con tu clc")
            else:
                cool+=1
    return choixParking

def inscriptionClient(choixParking):
    plaque = input("\n\nEntrez votre plaque d'immatriculation :\n> ")

def gestionStationnement(choixParking):
    if choixParking == '0': exit()
    for i in range(27):
        if parks[i][0] == choixParking:
            print('Nom: ' + parks[i][1] + '\nAdresse: ' + parks[i][2] + "\nPanneau d'affichage: " + parks[i][8] + ' places')
    inscriptionClient(choixParking)

clear()
infoParkings()
#drivers.append(clients('AMN0000', 'CR-709-ZF', temps()))
#drivers.append(clients('AMN0001', 'EA-726-LR', temps()))
print('\n======================================\nBienvenue sur Amiens Métropole CarPark\n======================================\n'
      '\n1. Rechercher un stationnement')
choix = input('> ')
clear()
if choix == '1':
    choixParking = rechercheStationnement()
    gestionStationnement(choixParking)

elif choix == '2':
    for i in range(27):
            print(parks[i][0] + ' - ' + parks[i][1] + ' - ' + parks[i][2] + ' - ' + parks[i][3] + ' - ' + parks[i][4] + ' - ' + parks[i][5] + ' - ' + parks[i][6] + ' - ' + parks[i][7] + ' - ' + parks[i][8])

elif choix == '3':
    print("Ton père le bucheron\n")

