# P9 - Système de Critiques et Tickets

Ce projet permet aux utilisateurs de créer des tickets, écrire des critiques, suivre d'autres utilisateurs et voir les critiques et tickets récents dans un flux.

## Fonctionnalités

- **Authentification** :

  - Inscription
  - Connexion
  - Déconnexion

- **Gestion des tickets** :

  - Création
  - Édition
  - Suppression

- **Gestion des critiques** :

  - Création
  - Édition
  - Suppression

- **Système d'abonnements** :

  - Suivre/Désabonner des utilisateurs

- **Flux** :
  - Affichage des tickets et critiques récents de l'utilisateur et de ceux qu'il suit

## Installation

1. Clonez ce dépôt : `git clone [URL REPO]`
2. Installez les dépendances: `pip install -r requirements.txt`
3. Appliquez les migrations : `python manage.py migrate`
4. Lancez le serveur : `python manage.py runserver`

## Utilisation

Accédez à `http://localhost:8000/` pour vous connecter ou vous inscrire. Une fois connecté, vous pouvez créer des tickets, écrire des critiques, suivre des utilisateurs et plus encore à partir des liens et des options disponibles sur la plateforme.
