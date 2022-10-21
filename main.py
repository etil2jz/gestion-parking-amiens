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
    def __init__(self, choixParking, numPlaque, temps, dateOut, heureOut, minuteOut):
        self.idParking = choixParking
        self.plaque = numPlaque
        self.dateArrivee = temps
        self.dateSortie = dateOut
        self.heureSortie = heureOut
        self.minuteSortie = minuteOut
    def __repr__(self):
        return 'idParking: %s - plaque: %s - dateArrivee: %s - dateSortie: %s - heureSortie: %s - minuteSortie: %s' % (self.idParking, self.plaque, self.dateArrivee, self.dateSortie, self.heureSortie, self.minuteSortie)

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
    clear()
    return choixParking

def inscriptionStationnement(choixParking):
    if choixParking == '0': exit()
    for i in range(27):
        if parks[i][0] == choixParking:
            print('Ville: ' + parks[i][3] + '\nNom: ' + parks[i][1] + '\nAdresse: ' + parks[i][2] + "\nPanneau d'affichage: " + parks[i][8] + ' places')
    plaque = input("\n\nEntrez votre plaque d'immatriculation\n> ")
    dateSortie = input('\nEntrez votre date de sortie\n> ')
    heureSortie = input('\nEntrez votre horaire de sortie\n> Heure : ')
    minuteSortie = input('> Minute : ')
    drivers.append(clients(choixParking, plaque, temps(), dateSortie, heureSortie, minuteSortie))
    print(drivers[0]) # debug

clear()
infoParkings()
choix = input('\n======================================\nBienvenue sur Amiens Métropole CarPark\n======================================\n'
              '\n1. Rechercher un stationnement'
              '\n> ')
clear()
if choix == '1':
    choixParking = rechercheStationnement()
    inscriptionStationnement(choixParking)