import csv
import os
import platform
import sys
import datetime
import time
import pytz

# parks est remplie des données de parking du fichier parking-metropole.txt
# Cela donne concrètement un tableau deux dimensions (parks[0][0] retourne 'AMN0000')
parks = []

# Variables globales afin de garder en mémoire le nombre de parkings par ville
# On peut les afficher avec la fonction infoParkings()
nbParkingsTotal = 0
nbParkingsAmiens = 0
nbParkingsAlbert = 0
nbParkingsAbbeville = 0

drivers = [] # Liste drivers vide qui sera remplie au fur et à mesure d'objets client

exitCondition = 0

# La classe clients est remplie des données concernant les automobilistes
# Cela comprend l'identifiant du parking, la plaque du véhicule, la date et heure d'entrée
class clients:
    def __init__(self, choixParking, numPlaque, dateEtHeureDEntree):
        self.idParking = choixParking
        self.plaque = numPlaque
        self.dateHeureEntree = dateEtHeureDEntree
    def __repr__(self):
        return 'idParking: %s - plaque: %s - dateHeureEntree: %s - dateHeureSortie: %s - statutClient: %s' % (self.idParking, self.plaque, self.dateHeureEntree)

# Ouverture du fichier parking-metropole.txt en lecture
# afin d'importer ses données dans parks
with open(os.path.join(sys.path[0], 'parking-metropole.txt'), 'r') as fichierParking:
    lecture = csv.reader(fichierParking, delimiter = '\t')
    next(lecture)
    i = 0
    for ligne in lecture:
        parks.append(ligne)
        nbParkingsTotal += 1
        if parks[i][4] == '.':
            nbParkingsTotal -= 1
            # Placement des infos des parkings défaillants
            with open(os.path.join(sys.path[0], 'defaillants.txt'), 'a') as fichierDefaillants:
                for j in range(9):
                    fichierDefaillants.write(parks[i][j] + '\t')
                fichierDefaillants.write('\n')
            del parks[-1]
            i -= 1
        if parks[i][3] == 'Amiens' and parks[i][4] != '.': nbParkingsAmiens += 1
        elif parks[i][3] == 'Albert' and parks[i][4] != '.': nbParkingsAlbert += 1
        elif parks[i][3] == 'Abbeville' and parks[i][4] != '.': nbParkingsAbbeville += 1
        i += 1

# Fonction pour récupérer heure et date
def getTemps():
    return datetime.datetime.now(pytz.timezone('Europe/Paris')).replace(microsecond = 0)

# Fonction pour vider le terminal (à des fins esthétiques)
# cls sous Windows et clear sous Linux / Mac OS
def clear():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

# Fonction pour print le nombre de parkings dans la métropole
def infoParkings():
    print('Nombre total de parkings: ' + str(nbParkingsTotal))
    print('Parkings à Amiens: ' + str(nbParkingsAmiens))
    print('Parkings à Albert: ' + str(nbParkingsAlbert))
    print('Parkings à Abbeville: ' + str(nbParkingsAbbeville))

def rechercheStationnement():
    while True:
        ville = input('\nDans quelle ville souhaitez-vous stationner ?\n> ')
        clear()
        if ville == 'Amiens' or ville == 'Albert' or ville == 'Abbeville':
            break
    print('\nVoici la liste des parkings d\'' + ville + ' :\n')
    for i in range(len(parks)):
        if parks[i][3] == ville:
            print(parks[i][0] + ' - ' + parks[i][1] + ' - ' + parks[i][2] + ' - ' + parks[i][4])
    choixParking = input('\nEntrez l\'identifiant du parking entré (0 pour abandonner) :\n> ')
    clear()
    return choixParking

def entreeParking(choixParking):
    if choixParking == '0': exit()
    for i in range(len(parks)):
        if parks[i][0] == choixParking:
            print('Ville: ' + parks[i][3] + '\nNom: ' + parks[i][1] + '\nAdresse: ' + parks[i][2] + '\nPanneau d\'affichage: ' + parks[i][8] + ' places')
    plaque = input('\n\nEntrez votre plaque d\'immatriculation\n> ')
    drivers.append(clients(choixParking, plaque, str(getTemps())))
    # debug
    #print('Client saisi : parking=' + drivers[0].idParking + ' plaque=' + drivers[0].plaque + ' dateHeureEntree=' + drivers[0].dateHeureEntree + ' dateHeureSortie=' + drivers[0].dateHeureSortie + ' statutClient=' + drivers[0].statutClient)
    print('\nEnregistrement du stationnement effectué !')
    time.sleep(2.5)

def sortieParking():
    plaque = input('\n\nEntrez votre plaque d\'immatriculation\n> ')
    for i in range(len(drivers)):
        if drivers[i].plaque == plaque:
            delta = datetime.timedelta(drivers[i].dateHeureEntree, getTemps()) # buggé
    print(delta.total_seconds() / 60) # buggé

# Fonction boucle pour afficher les parkings
def afficherListeParkings():
    for i in range(len(parks)):
        print(parks[i][0] + ' ' + parks[i][1] + ' ' + parks[i][2] + ' ' + parks[i][3] + ' ' + parks[i][4] + ' ' + parks[i][5] + ' ' + parks[i][6] + ' ' + parks[i][7] + ' ' + parks[i][8])

while True:
    clear()
    infoParkings()
    choix = input('\n======================================\nBienvenue sur Amiens Métropole CarPark\n======================================\n'
                  '\n1. Afficher les parkings de la métropole'
                  '\n2. Rechercher un stationnement'
                  '\n3. Sortir de son stationnement'
                  '\n> ')
    clear()
    if choix == '1':
        afficherListeParkings()
    elif choix == '2':
        choixParking = rechercheStationnement()
        entreeParking(choixParking)
    elif choix == '3':
        sortieParking()