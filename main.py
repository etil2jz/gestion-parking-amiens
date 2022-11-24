import csv
import datetime
import math
import os
import platform
import pytz
import sys
import time

# parks est remplie des données de parking du fichier parking-metropole.txt
# Cela donne concrètement un tableau deux dimensions (parks[0][0] retourne
# 'AMN0000')
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

enableFlux = 0  # État de la fonctionnalité 'flux'


def parksLoading():
    """Lire le fichier parking-metropole.txt et ajouter ses données dans la
       liste. Si parking défaillant, ajout de celui-ci dans un fichier à part.
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
    parks.clear()  # Vider la liste au cas où on update la liste de parkings
    # Supprimer le fichier defaillants.txt, il sera recréé lors de
    # l'importation
    if os.path.exists(os.path.join(sys.path[0], 'defaillants.txt')):
        os.remove(os.path.join(sys.path[0], 'defaillants.txt'))
    # Importation des données dans la liste parks[]
    with open(os.path.join(sys.path[0], 'parking-metropole.txt'), 'r') as fichierParking:
        # lecture du fichier avec les tab
        lecture = csv.reader(fichierParking, delimiter='\t')
        next(lecture)  # skip du nom des colonnes
        i = 0
        for ligne in lecture:
            parks.append(ligne)
            nbParkingsTotal += 1
            # Exclure les parkings au statut '.' ou 'FERME',
            # les mettre dans défaillants. Aussi faire -1 aux totaux
            if parks[i][4] == '.' or parks[i][4] == 'FERME':
                nbParkingsTotal -= 1
                if parks[i][3] == 'Amiens':
                    nbParkingsAmiens -= 1
                elif parks[i][3] == 'Albert':
                    nbParkingsAlbert -= 1
                elif parks[i][3] == 'Abbeville':
                    nbParkingsAbbeville -= 1
                # Placement des infos des parkings défaillants
                # Création du fichier defaillants.txt et ajout de ses parkings
                with open(os.path.join(sys.path[0], 'defaillants.txt'), 'a') as fichierDefaillants:
                    for j in range(9):
                        fichierDefaillants.write(parks[i][j] + '\t')
                    fichierDefaillants.write('\n')
                del parks[-1]
                i -= 1
            # +1 à chaque parking d'une ville
            if parks[i][3] == 'Amiens':
                nbParkingsAmiens += 1
            elif parks[i][3] == 'Albert':
                nbParkingsAlbert += 1
            elif parks[i][3] == 'Abbeville':
                nbParkingsAbbeville += 1
            i += 1


def entreesLoading():
    """Enregistrer les entrées stationnement dans un fichier
       texte et rafraîchir la liste des entrées.
    """
    entrees.clear()  # Vider la liste pour update selon stationnement
    # Importation des données dans la liste entrees[]
    with open(os.path.join(sys.path[0], 'stationnement.txt'), 'r') as fichierEntrees:
        lecture = csv.reader(fichierEntrees, delimiter='\t')
        for ligne in lecture:
            entrees.append(ligne)


def getTemps():
    """Récupérer le temps local sur la timezone Europe/Paris.

    Returns:
        datetime: date et heure
    """
    return datetime.datetime.now(pytz.timezone(
        'Europe/Paris')).replace(microsecond=0)


def etatStationnement(choixParking, plaque, tempsNow):
    """Écrire un fichier stationnement.txt enregistrant
       les clients stationnés.

    Args:
        choixParking (str): identifiant du parking
        plaque (str): identifiant de plaque
        tempsNow (datetime): heure à un certain instant
    """
    # Création du fichier stationnement.txt et ajout des entrées
    with open(os.path.join(sys.path[0], 'stationnement.txt'), 'a') as stationnementTxt:
        stationnementTxt.write(
            choixParking +
            '\t' +
            plaque +
            '\t' +
            str(tempsNow) +
            '\n')


def parkMetropole2():
    """Créer une sauvegarde des parkings à jour.
    """
    # Supprimer le fichier parking-metropole2.txt, on va le recréer
    if os.path.exists(os.path.join(sys.path[0], 'parking-metropole2.txt')):
        os.remove(os.path.join(sys.path[0], 'parking-metropole2.txt'))
    # Exportation des données modifiées de parks[]
    with open(os.path.join(sys.path[0], 'parking-metropole2.txt'), 'a') as fichierParking2:
        fichierParking2.write(
            'Identifiant\tNom\tAdresse\tVille\tEtat\tPlaces disponibles'
            '\tCapacité max\tDate de mise à jour\tAffichage panneaux\n')
        for i in range(len(parks)):
            fichierParking2.write(parks[i][0] +
                                  '\t' +
                                  parks[i][1] +
                                  '\t' +
                                  parks[i][2] +
                                  '\t' +
                                  parks[i][3] +
                                  '\t' +
                                  parks[i][4] +
                                  '\t' +
                                  parks[i][5] +
                                  '\t' +
                                  parks[i][6] +
                                  '\t' +
                                  str(getTemps()) +
                                  '\t' +
                                  parks[i][8] +
                                  '\n')


def flux(choixParking, plaque, tempsNow, statut):
    """Écrire un fichier flux.txt enregistrant l'historique d'entrée/sortie.

    Args:
        choixParking (str): identifiant du parking
        plaque (str): identifiant de plaque
        tempsNow (datetime): heure à un certain instant
        statut (str): entrée ou sortie
    """
    with open(os.path.join(sys.path[0], 'flux.txt'), 'a') as fluxTxt:
        fluxTxt.write(
            choixParking +
            '\t' +
            plaque +
            '\t' +
            str(tempsNow) +
            '\t' +
            statut +
            '\n')


def clear():
    """Vider le terminal à des fins esthétiques (s'adapte à l'OS).
    """
    os.system('cls' if platform.system() == 'Windows' else 'clear')


def infoParkings():
    """Afficher le nombre de parkings dans la métropole.
    """
    print('Nombre total de parkings: ' + str(nbParkingsTotal))
    print('Parkings à Amiens: ' + str(nbParkingsAmiens))
    print('Parkings à Albert: ' + str(nbParkingsAlbert))
    print('Parkings à Abbeville: ' + str(nbParkingsAbbeville))


def rechercheStationnement():
    """Demander à l'utilisateur sur quel parking
       souhaite-t-il se rendre.

    Returns:
        string: identifiant du parking sélectionné
    """
    # Boucle avec sélection de la ville
    while True:
        ville = input(
            '\nDans quelle ville souhaitez-vous stationner ?'
            ' (Amiens, Albert, Abbeville)\n> ')
        clear()
        if ville == 'Amiens' or ville == 'Albert' or ville == 'Abbeville':
            break
    clear()
    # Affichage filtré des parkings
    print('\nVoici la liste des parkings d\'' + ville + ' :\n')
    for i in range(len(parks)):
        if parks[i][3] == ville:
            print(
                parks[i][0] +
                ' - ' +
                parks[i][1] +
                ' - ' +
                parks[i][2] +
                ' - ' +
                parks[i][4])
    choixParking = input(
        '\nEntrez l\'identifiant du parking où entrer'
        ' (0 pour abandonner) :\n> ')
    clear()
    return choixParking


def entreeParking(choixParking):
    """Enregistrer l'entrée d'un utilisateur sur
       un parking.

    Args:
        choixParking (str): identifiant du parking où l'entrée se passe
    """
    # Abandon si identifiant vaut 0
    if choixParking == '0':
        return
    for i in range(len(parks)):
        if parks[i][0] == choixParking:
            # Exception si le parking est statut ABONNÉS
            if parks[i][8] == 'ABONNES':
                while True:
                    abonne = input(
                        '\nVous avez choisi un parking avec abonnement.'
                        ' En possédez-vous un ? [Y/n]\n> ')
                    if abonne == 'Y' or abonne == 'n':
                        break
                if abonne == 'n':
                    return
                else:
                    clear()
            # Exception si le parking est statut COMPLET
            elif parks[i][8] == 'COMPLET':
                print('\nCe parking est complet. Retour au menu principal...')
                time.sleep(4)
                return
            print(
                'Ville: ' +
                parks[i][3] +
                '\nNom: ' +
                parks[i][1] +
                '\nAdresse: ' +
                parks[i][2] +
                '\nPanneau d\'affichage: ' +
                parks[i][8] +
                ' places')
            # Soustraction d'une place sur le parking
            placeDispo = int(parks[i][5])
            placeDispo -= 1
            parks[i][5] = str(placeDispo)
            panneauDispo = int(parks[i][8])
            panneauDispo -= 1
            parks[i][8] = str(panneauDispo)
            # 0 place vaut COMPLET
            if parks[i][8] == '0':
                parks[i][4] = 'COMPLET'
                parks[i][8] = 'COMPLET'
    plaque = input(
        '\n\nEntrez votre plaque d\'immatriculation (AA-111-BB)\n> ')
    timeNow = getTemps()
    etatStationnement(choixParking, plaque, timeNow)
    if enableFlux == 1:
        flux(choixParking, plaque, timeNow, 'ENTREE')
    print('\nEnregistrement du stationnement effectué !')
    time.sleep(4)


def sortieParking():
    """Enregistrer la sortie d'un utilisateur sur
       un parking.
    """
    plaque = input(
        '\n\nEntrez votre plaque d\'immatriculation (AA-111-BB)\n> ')
    supprime = 0
    entreesLoading()
    for i in range(len(entrees)):
        if entrees[i][1] == plaque:
            supprime = 1
            # Addition d'une place sur le parking
            placeDispo = int(parks[i][5])
            placeDispo += 1
            parks[i][5] = str(placeDispo)
            if parks[i][8] == 'COMPLET':
                parks[i][8] = '0'
            panneauDispo = int(parks[i][8])
            panneauDispo += 1
            parks[i][8] = str(panneauDispo)
            # Comme le parking n'est plus complet,
            # on le passe en OUVERT
            if parks[i][8] != 'COMPLET':
                parks[i][4] = 'OUVERT'
            parking = entrees[i][0]
            tempsNow = getTemps()
            # Différence entre l'heure d'entrée et de sortie
            # pour pouvoir calculer le prix du stationnement
            deltaHeure = (
                tempsNow.replace(
                    tzinfo=None) - datetime.datetime.strptime(
                    entrees[i][2],
                    '%Y-%m-%d %H:%M:%S+01:00')).total_seconds() / 3600
            print('\n' + str(4 * math.ceil(deltaHeure)) +
                  '€ vous seront débités dans les prochains jours.'
                  '\nÀ bientôt !')
            # Suppression dans stationnement.txt du client
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


def afficherListeParkings():
    """Afficher la liste des parkings hors ceux
       considérés comme défaillants.
    """
    for i in range(len(parks)):
        print(
            parks[i][0] +
            ' ' +
            parks[i][1] +
            ' ' +
            parks[i][2] +
            ' ' +
            parks[i][3] +
            ' ' +
            parks[i][4] +
            ' ' +
            parks[i][5] +
            ' ' +
            parks[i][6] +
            ' ' +
            parks[i][7] +
            ' ' +
            parks[i][8])
    input('\nAppuyez sur Entrée pour continuer')


# Chargement au lancement du programme
# des données parkings et stationnements
parksLoading()
entreesLoading()

# Menu utilisateur avec sélection de l'action
while True:
    clear()
    infoParkings()
    choix = input(
        '\n======================================'
        '\nBienvenue sur Amiens Métropole CarPark'
        '\n======================================\n'
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
        print('\nL\'état des parkings a été sauvegardé'
              ' dans parking-metropole2.txt')
        time.sleep(4)
    elif choix == '6':
        exit()
