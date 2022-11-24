import csv
import datetime
import math
import os
import platform
import pytz
import sys
import time

# parks est remplie des données de parking du fichier parking-metropole.txt
# Cela donne concrètement un tableau deux dimensions (parks[0][0] retourne 'AMN0000')
parks = []

# entrees est remplie des données de stationnement du fichier stationnement.txt
# Comme parks, on a en gros un tableau deux dimensions
entrees = []

# Variables globales afin de garder en mémoire le nombre de parkings par ville
# On peut les afficher avec la fonction infoParkings()
nbParkingsTotal = 0
nbParkingsAmiens = 0
nbParkingsAlbert = 0
nbParkingsAbbeville = 0

enableFlux = 0

def parksLoading():
    """Lire le fichier parking-metropole.txt et ajouter ses données dans la liste
       Si parking défaillant, ajout de celui-ci dans un fichier à part defaillants.txt
    """
    # Remise à zéro des totaux de parkings opérationnels
    global nbParkingsTotal
    global nbParkingsAmiens
    global nbParkingsAlbert
    global nbParkingsAbbeville
    nbParkingsTotal = 0
    nbParkingsAmiens = 0
    nbParkingsAlbert = 0
    nbParkingsAbbeville = 0
    parks.clear() # Vider la liste au cas où on update la liste de parkings
    if os.path.exists(os.path.join(sys.path[0], 'defaillants.txt')): # Supprimer le fichier defaillants.txt, il sera recréé lors de l'importation
        os.remove(os.path.join(sys.path[0], 'defaillants.txt'))
    with open(os.path.join(sys.path[0], 'parking-metropole.txt'), 'r') as fichierParking: # Importation des données dans la liste parks[]
        lecture = csv.reader(fichierParking, delimiter = '\t')
        next(lecture) # skip du nom des colonnes
        i = 0
        for ligne in lecture:
            parks.append(ligne)
            nbParkingsTotal += 1
            if parks[i][4] == '.' or parks[i][4] == 'FERME':
                nbParkingsTotal -= 1
                if parks[i][3] == 'Amiens': nbParkingsAmiens -= 1
                elif parks[i][3] == 'Albert': nbParkingsAlbert -= 1
                elif parks[i][3] == 'Abbeville': nbParkingsAbbeville -= 1
                # Placement des infos des parkings défaillants
                with open(os.path.join(sys.path[0], 'defaillants.txt'), 'a') as fichierDefaillants: # Création du fichier defaillants.txt et ajout de ses parkings
                    for j in range(9):
                        fichierDefaillants.write(parks[i][j] + '\t')
                    fichierDefaillants.write('\n')
                del parks[-1]
                i -= 1
            if parks[i][3] == 'Amiens': nbParkingsAmiens += 1
            elif parks[i][3] == 'Albert': nbParkingsAlbert += 1
            elif parks[i][3] == 'Abbeville': nbParkingsAbbeville += 1
            i += 1

def entreesLoading():
    entrees.clear() # Vider la liste pour update selon stationnement
    with open(os.path.join(sys.path[0], 'stationnement.txt'), 'r') as fichierEntrees: # Importation des données dans la liste entrees[]
        lecture = csv.reader(fichierEntrees, delimiter = '\t')
        for ligne in lecture:
            entrees.append(ligne)

def getTemps():
    """Récupérer le temps local sur la timezone Europe/Paris

    Returns:
        datetime: date et heure
    """
    return datetime.datetime.now(pytz.timezone('Europe/Paris')).replace(microsecond = 0)

def etatStationnement(choixParking, plaque, tempsNow):
    """Écriture d'un fichier stationnement.txt enregistrant les clients stationnés

    Args:
        choixParking (str): identifiant du parking
        plaque (str): identifiant de plaque
        tempsNow (datetime): heure à un certain instant
    """
    with open(os.path.join(sys.path[0], 'stationnement.txt'), 'a') as stationnementTxt: # Création du fichier stationnement.txt et ajout des entrées
        stationnementTxt.write(choixParking + '\t' + plaque + '\t' + str(tempsNow) + '\n')

def parkMetropole2():
    if os.path.exists(os.path.join(sys.path[0], 'parking-metropole2.txt')): # Supprimer le fichier parking-metropole2.txt, on va le recréer
        os.remove(os.path.join(sys.path[0], 'parking-metropole2.txt'))
    with open(os.path.join(sys.path[0], 'parking-metropole2.txt'), 'a') as fichierParking2: # Exportation des données modifiées de parks[]
        fichierParking2.write('Identifiant\tNom\tAdresse\tVille\tEtat\tPlaces disponibles\tCapacité max\tDate de mise à jour\tAffichage panneaux\n')
        for i in range(len(parks)):
            fichierParking2.write(parks[i][0] + '\t' + parks[i][1] + '\t' + parks[i][2] + '\t' + parks[i][3] + '\t' + parks[i][4] + '\t' + parks[i][5] + '\t' + parks[i][6] + '\t' + str(getTemps()) + '\t' + parks[i][8] + '\n')

def flux(choixParking, plaque, tempsNow, statut):
    """Écriture d'un fichier flux.txt enregistrant l'historique d'entrée/sortie

    Args:
        choixParking (str): identifiant du parking
        plaque (str): identifiant de plaque
        tempsNow (datetime): heure à un certain instant
        statut (str): entrée ou sortie
    """
    with open(os.path.join(sys.path[0], 'flux.txt'), 'a') as fluxTxt:
        fluxTxt.write(choixParking + '\t' + plaque + '\t' + str(tempsNow) + '\t' + statut + '\n')

# Fonction pour vider le terminal (à des fins esthétiques)
# cls sous Windows et clear sous Linux / Mac OS
def clear():
    """Vider le terminal à des fins esthétiques (s'adapte à l'OS)
    """
    os.system('cls' if platform.system() == 'Windows' else 'clear')

# Fonction pour print le nombre de parkings dans la métropole
def infoParkings():
    print('Nombre total de parkings: ' + str(nbParkingsTotal))
    print('Parkings à Amiens: ' + str(nbParkingsAmiens))
    print('Parkings à Albert: ' + str(nbParkingsAlbert))
    print('Parkings à Abbeville: ' + str(nbParkingsAbbeville))

def rechercheStationnement():
    while True:
        ville = input('\nDans quelle ville souhaitez-vous stationner ? (Amiens, Albert, Abbeville)\n> ')
        clear()
        if ville == 'Amiens' or ville == 'Albert' or ville == 'Abbeville':
            break
    clear()
    print('\nVoici la liste des parkings d\'' + ville + ' :\n')
    for i in range(len(parks)):
        if parks[i][3] == ville:
            print(parks[i][0] + ' - ' + parks[i][1] + ' - ' + parks[i][2] + ' - ' + parks[i][4])
    choixParking = input('\nEntrez l\'identifiant du parking où entrer (0 pour abandonner) :\n> ')
    clear()
    return choixParking

def entreeParking(choixParking):
    if choixParking == '0':
        return
    for i in range(len(parks)):
        if parks[i][0] == choixParking:
            if parks[i][8] == 'ABONNES':
                while True:
                    abonne = input('\nVous avez choisi un parking avec abonnement. En possédez-vous un ? [Y/n]\n> ')
                    if abonne == 'Y' or abonne == 'n':
                        break
                if abonne == 'n':
                    return
                else:
                    clear()
            elif parks[i][8] == 'COMPLET':
                print('\nCe parking est complet. Retour au menu principal...')
                time.sleep(4)
                return
            print('Ville: ' + parks[i][3] + '\nNom: ' + parks[i][1] + '\nAdresse: ' + parks[i][2] + '\nPanneau d\'affichage: ' + parks[i][8] + ' places')
            placeDispo = int(parks[i][5])
            placeDispo -= 1
            parks[i][5] = str(placeDispo)
            panneauDispo = int(parks[i][8])
            panneauDispo -= 1
            parks[i][8] = str(panneauDispo)
            if parks[i][8] == '0':
                parks[i][4] = 'COMPLET'
                parks[i][8] = 'COMPLET'
    plaque = input('\n\nEntrez votre plaque d\'immatriculation (AA-111-BB)\n> ')
    timeNow = getTemps()
    etatStationnement(choixParking, plaque, timeNow)
    if enableFlux == 1:
        flux(choixParking, plaque, timeNow, 'ENTREE')
    print('\nEnregistrement du stationnement effectué !')
    time.sleep(4)

def sortieParking():
    plaque = input('\n\nEntrez votre plaque d\'immatriculation (AA-111-BB)\n> ')
    supprime = 0
    entreesLoading()
    for i in range(len(entrees)):
        if entrees[i][1] == plaque:
            supprime = 1
            placeDispo = int(parks[i][5])
            placeDispo += 1
            parks[i][5] = str(placeDispo)
            if parks[i][8] == 'COMPLET':
                parks[i][8] = '0'
            panneauDispo = int(parks[i][8])
            panneauDispo += 1
            parks[i][8] = str(panneauDispo)
            if parks[i][8] != 'COMPLET':
                parks[i][4] = 'OUVERT'
            parking = entrees[i][0]
            tempsNow = getTemps()
            deltaHeure = (tempsNow.replace(tzinfo=None) - datetime.datetime.strptime(entrees[i][2], '%Y-%m-%d %H:%M:%S+01:00')).total_seconds() / 3600
            print('\n' + str(4 * math.ceil(deltaHeure)) + '€ vous seront débités dans les prochains jours.\nÀ bientôt !')
            with open(os.path.join(sys.path[0], 'stationnement.txt'), 'r') as fr:
                lignes = fr.readlines()
                pointeur = 1
                with open(os.path.join(sys.path[0], 'stationnement.txt'), 'w') as fw:
                    for ligne in lignes:
                        if pointeur != i + 1:
                            fw.write(ligne)
                        pointeur += 1
    if enableFlux == 1:
        flux(parking, plaque, tempsNow, 'SORTIE')
    entreesLoading()
    if supprime == 0:
        print('\nCette plaque n\'est pas enregistrée dans notre registre.')
    time.sleep(4)

# Fonction boucle pour afficher les parkings
def afficherListeParkings():
    for i in range(len(parks)):
        print(parks[i][0] + ' ' + parks[i][1] + ' ' + parks[i][2] + ' ' + parks[i][3] + ' ' + parks[i][4] + ' ' + parks[i][5] + ' ' + parks[i][6] + ' ' + parks[i][7] + ' ' + parks[i][8])
    input('\nAppuyez sur Entrée pour continuer')

parksLoading()
entreesLoading()
while True:
    clear()
    infoParkings()
    choix = input('\n======================================\nBienvenue sur Amiens Métropole CarPark\n======================================\n'
                  '\n1. Afficher les parkings de la métropole'
                  '\n2. Rechercher un stationnement'
                  '\n3. Sortir de son stationnement'
                  '\n4. Activer/Désactiver l\'enregistrement du flux'
                  '\n5. Sauvegarder l\'état des parkings'
                  '\n6. Quitter'
                  '\n> ')
    clear()
    if choix == '1':
        afficherListeParkings()
    elif choix == '2':
        choixParking = rechercheStationnement()
        entreeParking(choixParking)
    elif choix == '3':
        sortieParking()
    elif choix == '4':
        if enableFlux == 0:
            enableFlux = 1
            print('\nEnregistrement du flux activé !')
            time.sleep(4)
        else:
            enableFlux = 0
            print('\nEnregistrement du flux désactivé !')
            time.sleep(4)
    elif choix == '5':
        parkMetropole2()
        print('\nL\'état des parkings a été sauvegardé dans parking-metropole2.txt')
        time.sleep(4)
    elif choix == '6':
        exit()
