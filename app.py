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
modele_teachable_actif = "FXJoVB2HU/"

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

# Fonction de récupération de la liste des id teachable
def read_file_to_list(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            # Enlever les caractères de nouvelle ligne à la fin de chaque ligne
            lines = [line.strip() for line in lines]
        return lines
    except FileNotFoundError:
        print(f"Le fichier {file_path} n'a pas été trouvé.")
        return []
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
        return []

# Utilisation de la fonction pour lire le fichier id_teachable.txt
file_path = 'id_teachable.txt'


# Récupération d'un nouvel id
def write_to_file(file_path, text):
    try:
        with open(file_path, 'a') as file:
            file.write('\n' + text)
    except Exception as e:
        print(f"Une erreur est survenue lors de l'écriture dans le fichier : {e}")



app = Flask(__name__)

# Configuration de la broche GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)  # Remplacez 17 par le numéro de broche que vous utilisez

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        new_id = request.form['id_teachable']
        write_to_file('id_teachable.txt', new_id)
    # Lecture de la liste des fichiers
    list_id_teachable = read_file_to_list(file_path)   
    return render_template('index.html', list_id_teachable=list_id_teachable, modele_teachable_actif=modele_teachable_actif )

@app.route('/load_labels', methods=['POST'])
def load_labels():
    global labels_dict
    data = request.json
    labels = data.get('labels', [])
    labels_dict = {label: i for i, label in enumerate(labels)}
    return jsonify({'status': 'labels loaded', 'labels': labels_dict})

@app.route('/selectBoite', methods=['POST'])
def toggle_gpio():
    data = request.json
    label = data.get('label')
    numCaisse = int(labels_dict[label])
    print(f"Positionnement de la caisse {label } : {numCaisse}")

    # Positionnement de la caisse correspondant au label
    positionnerCaisse(numCaisse)
    return jsonify({'status': f'Caisse {numCaisse} positionnée'})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
