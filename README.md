# Projet SI - Palissy 2024 - Reconnaissance / tri d'objets
Ce projet est une application web utilisant Flask pour le backend, TensorFlow.js pour l'inférence côté client, et RPi.GPIO pour contrôler les broches GPIO d'un Raspberry Pi.
## Table des Matières
1. [Prérequis](#prérequis)
2. [Installation](#installation)
   - [Cloner le Dépôt](#cloner-le-dépôt)
   - [Créer et Activer un Environnement Virtuel](#créer-et-activer-un-environnement-virtuel)
   - [Installer les Dépendances](#installer-les-dépendances)
3. [Configuration](#configuration)
4. [Exécution de l'Application](#exécution-de-lapplication)
5. [Utilisation de l'Application](#utilisation-de-lapplication)
6. [Dépannage](#dépannage)
7. [Contribuer](#contribuer)
8. [Licence](#licence)
## Prérequis
Assurez-vous d'avoir installé les éléments suivants sur votre machine :
- Python 3.x
- `pip` (le gestionnaire de paquets pour Python)
- Un environnement virtuel (recommandé)
## Installation
### Cloner le Dépôt
Clonez le dépôt sur votre machine locale :
```sh
git clone https://github.com/votre-utilisateur/votre-repo.git
cd votre-repo
```
### Créer et Activer un Environnement Virtuel
1. Créer un environnement virtuel :
```sh
python -m venv venv
```
2. Activer l'environnement virtuel :
* Sous Windows :
```sh
venv\Scripts\activate
```
* Sous macOS et Linux :
```sh
source venv/bin/activate
```
Vérifier que le prompt commence bien par (venv). À présent, il est possible d'installer les dépendances uniquement pour cet environnement virtuel.
### Installer les Dépendances
Installez les dépendances à partir du fichier requirements.txt :
```sh
pip install -r requirements.txt
```
### Configuration
Assurez-vous que les fichiers suivants sont présents et correctement configurés :

* `app.py` : Le fichier principal de l'application Flask.
* `templates/index.html` : La page HTML principale utilisant TensorFlow.js pour l'inférence.