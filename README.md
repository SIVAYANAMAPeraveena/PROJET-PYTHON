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

| Onglet | Fonctionnalité | Rôle Clé |
| :--- | :--- | :--- |
| **Réservations** | Calendrier des Rendez-vous | Permet de consulter, gérer et annuler les réservations. Utilise la fonction `afficher_reservation()` et intègre le calendrier (`streamlit_calendar`). |
| **Bilan** | Gestion des Activités de Bien-être | Permet d’ajouter, suivre et cocher les activités du jour. Utilise la fonction `add_event()` pour enregistrer les activités et mettre à jour le score. |
| **Scoring** | Motivation par la Gamification | Calcul et affichage du score de bien-être en temps réel basé sur les activités accomplies et les réservations. Utilise `calculer_score_bien_etre()` et les graphiques matplotlib. |
| **Personnalisation** | Recommandation de Soins | Questionnaire interactif pour déterminer le soin idéal selon l’utilisateur. Utilise la fonction `get_recommendation()`. |
| **Soin / Tarifs** | Transparence des Prix | Affiche tous les soins disponibles et leurs prix fixes pour chaque institut. Utilise simplement des dictionnaires et st.markdown pour la présentation. |
| **Mes Informations** | Profil Utilisateur | Affiche les informations personnelles (nom, email, username) stockées dans `st.session_state.users`. |
| **Contacts** | Support et Communication | Permet de contacter l’équipe Minerals via un formulaire. Fonction : formulaire `contact_form` avec validation. |
| **À propos** | Présentation du Projet | Affiche la mission, valeurs, images illustratives et carte des boutiques intégrée (`st.map(df)`). |
 
## 3. Fonctionnalités Utilitaires

Afficher les étoiles (afficher_etoiles(spa_name)) : Affiche une note aléatoire (3 à 5 étoiles) pour chaque institut.

Gestion du carrousel d’images : next_image_callback(key, n) et prev_image_callback(key, n) permettent de naviguer dans les images des instituts.

Ajout d’événements (add_event(title, date)) : Ajoute des activités ou réservations dans le calendrier personnel de l’utilisateur, en évitant les doublons.

## 4. Interface et Navigation

Multi-page : Navigation fluide entre Accueil, Connexion, Réservation et Espace Personnel via st.session_state.

Design Zen : CSS minimaliste et harmonieux (couleurs beige et marron).

CGU : Acceptation obligatoire des Conditions Générales d’Utilisation avant accès à l’application.

## 5. Authentification et Gestion de Session

Formulaires dédiés pour connexion et création de compte.

Déconnexion possible, réinitialisant les données de session.

## 6. Bilan Quotidien et Gamification

Score de bien-être dynamique : Calculé en fonction des actions accomplies, des réservations et des niveaux d’humeur/stress.

To-Do List : Liste d’activités quotidiennes de bien-être qui contribuent au score.

Visualisation : Graphique de l’évolution du score et indicateurs de récompense mensuelle.

Encouragements : Messages et badges pour motiver la progression.

## 7. Personnalisation et Utilitaire Social

Quiz de recommandation : Permet de déterminer le soin le plus adapté selon l’utilisateur.

Récompenses et promotions : Déclenchées lorsque le score dépasse un seuil défini.

Persistance des données : Les données des utilisateurs (réservations, bilans, scores) sont sauvegardées localement via CSV.
