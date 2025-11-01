# MINI-PROJET-PYTHON
# 💎 Minerals : Plateforme de Bien-être et d'Utilité Sociale

## Objectif du Projet

**Minerals** est une plateforme entièrement dédiée au bien-être et à la détente, avec pour but principal de **maximiser l'utilité sociale des utilisateurs**. Cette application web propose de multiples fonctionnalités pour la rendre utile et à fort potentiel de relaxation en encourageant activement la valorisation du bien-être intérieur, ce qui est primordial dans nos sociétés dominées par le stress.

## Principales Fonctionnalités

### 1. Recherche, Localisation et Processus de Réservation

* **Filtrage par Région :** Une `selectbox` permet de sélectionner une région afin de filtrer et d'afficher immédiatement les établissements disponibles avec leur notation et leur adresse.
* **Localisation Instantanée :** En cliquant sur l'adresse, l'utilisateur est directement dirigé vers **Google Maps** pour la localisation et l'itinéraire.
* **Processus de Réservation :** Le bouton de réservation initie un **processus d'identification** nécessaire pour poursuivre :
    * L'utilisateur peut se **connecter** avec son identifiant et mot de passe.
    * Il peut aussi **créer un compte** via un questionnaire d'informations personnelles.
    * Cette étape mène à l'accès au calendrier pour **finaliser le choix du créneau horaire du spa**.

### 2. Espace Personnel Structuré

| Onglet | Fonctionnalité Clé | Description |
| :--- | :--- | :--- |
| **Réservations** | **Gestion des Rendez-vous & Calendrier** | Consultation du **calendrier** pour voir les rendez-vous réservés et gérer les futures réservations. |
| **Bilan** | **Gestion du Scoring et Activités** | Permet d'**ajouter ou de retirer des activités** contribuant au bien-être, ce qui a un impact direct sur le **scoring** de l'utilisateur. |
| **Scoring** | **Motivation par la Gamification** | Ce score augmente ou baisse selon les activités gérées dans l'onglet "Bilan". Son objectif est de motiver les efforts pour le bien-être personnel. |
| **Personnalisation** | **Recommandation de Soins** | Questionnaire permettant de déterminer quel soin serait le plus bénéfique en fonction de l'humeur de l'utilisateur. |
| **Soin / Tarifs** | **Information des Prix** | Présentation de l'ensemble des prestations et de leurs prix. Les tarifs sont **fixes**, quelle que soit la région du spa. |
| **Contacts** | **Support et Communication** | Accès aux coordonnées de l'équipe Minerals. |
| **À Propos** | **Présentation du Projet** | Informations complémentaires sur la création de l'application. |
 

### 3. afficher_etoiles(spa_name)

Rôle : Affiche une notation aléatoire (3 à 5 étoiles) pour chaque institut de spa.

Logique : Utilise st.session_state pour conserver la note entre les sessions Streamlit.

 ### 4.next_image_callback(key, n)

Rôle : Fait défiler les images suivantes du carrousel de chaque institut.

Logique : Incrémente l’index de l’image affichée dans st.session_state.

### 5. prev_image_callback(key, n)

Rôle : Permet de revenir à l’image précédente du carrousel.

Logique : Décrémente l’index de l’image affichée dans st.session_state.

### 6. add_event(title, date)

Rôle : Ajoute un événement (réservation ou activité) dans le calendrier personnalisé de l’utilisateur.

Logique : Empêche les doublons d’événements et met à jour le score de bien-être en fonction du nombre d’activités.

### 7. Interface et Navigation
Gestion Multi-Page : Utilisation de l'état de session (st.session_state) pour une navigation fluide entre l'Accueil, la Connexion, la Réservation et l'Espace Personnel, simulant une application web classique.

### 8.Design Personnalisé (Zen) : Injection de CSS pour appliquer un style visuel minimaliste et zen (couleurs Beige/Marron) pour une ambiance cohérente.

Conformité CGU : Écran de démarrage obligatoire demandant l'Acceptation des Conditions Générales d’Utilisation (CGU) avant d'accéder à l'application.

### 9. Authentification et Accès
Connexion / Inscription : Formulaires dédiés pour la connexion et la création de compte (logique simplifiée/simulée).

Gestion de Session : Fonctionnalité complète de déconnexion qui réinitialise l'état de la session utilisateur.


### 10. Bilan Quotidien et Gamification
Scoring de Bien-être Dynamique : Le score est calculé en temps réel en fonction des actions de l'utilisateur (tâches accomplies, réservations effectuées).

To-Do List (Tâches Quotidiennes) : Liste d'activités de bien-être qui, une fois cochées, augmentent le score (mécanisme de gamification).

Suivi Personnalisé : Des curseurs permettent l'enregistrement du niveau d'humeur et de stress, ces données contribuant également au score.

Visualisation : Un graphique en ligne simule l'évolution du score de bien-être.

### 11. Personnalisation et Utilitaire Social
Quiz de Recommandation : Quiz interactif qui structure les questions pour générer une recommandation de soin personnalisé.

Incitations et Évènements : Logique promotionnelle déclenchant des offres spéciales (ex: animation st.balloons et promotions) dès qu'un seuil de score est atteint.

Persistance des Données : Les données utilisateur (réservations, bilans, etc.) sont enregistrées dans un fichier local (user_data.csv) via la fonction save_user_data_to_csv (simulée).
