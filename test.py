from flask import Flask, request, jsonify, render_template
import RPi.GPIO as GPIO
import time
import math


# Pour éviter les alertes de GPIO potentiellement occupées
GPIO.setwarnings(False)

# Déclaration des constantes
DELAI = 0.000002  
MICROSTEP = 32
NB_CAISSES = 4  # Modifié lors du choix du modèle teachable
Z_PIGNON = 18
MODULE = 1
DISTANCE_CREMA = 120      # course maximale de la glissière / crémaillère avec marge de sécuerité

PAS_ENTRE_CAISSES = int((200 * DISTANCE_CREMA * MICROSTEP)/ (NB_CAISSES* math.pi * MODULE * Z_PIGNON))
print(f"Déplacement pour une caisse : {PAS_ENTRE_CAISSES} steps")


# Mode GPIO
GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)

# Broches de pilotage du moteur
dir_pin = 17
step_pin = 19
ena_pin = 23

# Déclaration en sortie
GPIO.setup(dir_pin, GPIO.OUT)
GPIO.setup(ena_pin, GPIO.OUT)
GPIO.setup(step_pin, GPIO.OUT)

# Variables globales
num_caisse_actuelle = 0
modele_teachable_actif = "rz5ffTQqQ"
list_id_teachable = [] 

#Fonction de déplacement du moteur
def move_stepper(direc,steps, delay):
    GPIO.output(dir_pin, direc)
    steps = abs(steps)
    for i in range(steps):
        GPIO.output(step_pin, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(step_pin, GPIO.LOW)
        time.sleep(delay)

#Fonction d'arrêt du moteur        
def stop_stepper():
    GPIO.output(step_pin, GPIO.LOW)

# Positionnement d'une caisse
def positionnerCaisse(num_caisse_selectionnee):
    # Récupération de la variable globale
    global num_caisse_actuelle

    # Calcul du nombre de pas relatif à la position actuelle
    nb_pas_relatifs = abs(num_caisse_actuelle - num_caisse_selectionnee) * PAS_ENTRE_CAISSES

    # La direction dépend du signe de num_caisse_actuelle - num_caisse_selectionnee
    if num_caisse_actuelle <= num_caisse_selectionnee :
        direction = GPIO.HIGH
    else :
        direction = GPIO.LOW

    # Déplacement du moteur
    move_stepper(direction,nb_pas_relatifs,DELAI)

    # Mise à jour de la nouvelle caisse actuelle
    num_caisse_actuelle = num_caisse_selectionnee
    return True


numCaisse = 0
positionnerCaisse(numCaisse)