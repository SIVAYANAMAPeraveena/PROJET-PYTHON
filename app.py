import streamlit as st
import random
import time
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from authentification import login, sign_up
from reservation import afficher_reservation, delete_reservation, reservation
from score import put_score
from utils import *

# --- CONFIGURATION INITIALE ---
COLOR_BLANC = "#ffffff"
COLOR_BEIGE = "#ebe1d6"
COLOR_MARRON = "#5c4329"

st.set_page_config(
    page_title="Minerals",
    page_icon="assets/logo.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.session_state.setdefault("monespace_section", "Mes informations")
st.session_state.setdefault("confirm_cancel", None)
st.session_state.setdefault("events", [])
st.session_state.setdefault("rerun_flag", False)
st.session_state.setdefault("reservations", [])
st.session_state.setdefault("bilan", {})
st.session_state.setdefault("scores", {}) 
st.session_state.setdefault("users", {}) 
try:
    from streamlit_calendar import calendar
    CALENDAR_AVAILABLE = True
except ImportError:
    CALENDAR_AVAILABLE = False

# --- FONCTIONS UTILITAIRES ---

def set_page(page_name):
    st.session_state.page = page_name
    st.rerun()

def calculer_score_bien_etre():
    score = 0
    if "todo_list" in st.session_state:
        score += sum(10 for item in st.session_state.todo_list if item['checked'])
    if "reservations" in st.session_state:
        score += len(st.session_state.reservations) * 10
    if st.session_state.get("humeur_slider", 5) > 7:
        score += 5
    return score

def save_user_data_to_csv(data):
    file_path = "reservation_data.csv"
    df = pd.DataFrame([data])
    if os.path.exists(file_path):
        df.to_csv(file_path, mode='a', header=False, index=False)
    else:
        df.to_csv(file_path, index=False)


# --- ETATS DE SESSION ---
# Initialisation de toutes les variables nécessaires
if "cgu_accepted" not in st.session_state:
    st.session_state.cgu_accepted = False
if "page" not in st.session_state:
    st.session_state.page = "cgu" 
if "authentification" not in st.session_state:
    st.session_state.authentification= False
if "email" not in st.session_state:
    st.session_state.email = ""
if "prenom" not in st.session_state:
    st.session_state.prenom = ""
if "selected_institut" not in st.session_state:
    st.session_state.selected_institut = None
if "reservations" not in st.session_state:
    st.session_state.reservations = [] 
if "header_index" not in st.session_state:
    st.session_state.header_index = 0
if "last_update" not in st.session_state:
    st.session_state.last_update = time.time()
if "todo_list" not in st.session_state:
    st.session_state.todo_list = [
        {"task": "Boire 1.5L d'eau", "checked": False},
        {"task": "Faire 30 min d'exercice", "checked": False},
        {"task": "Écrire mon journal d'humeur", "checked": False},
    ]
if "humeur_slider" not in st.session_state:
    st.session_state.humeur_slider = 5
if "stress_slider" not in st.session_state:
    st.session_state.stress_slider = 5

# --- DONNÉES DE L'APPLICATION ---
HEADER_IMAGES_PLACEHOLDERS = [
    "assets/ambiance.jpeg", 
    "assets/ambiance2.jpeg"
]
INSTITUTS = {
    "Paris": ["Le Spa Park Hyatt", "Les Bains du Marais"],
    "Lille": ["Spa Hermitage Gantois", "Spa Center Lille"],
    "Bordeaux": ["Spa de Sèze", "Les Bains de Léa"]
}
data = {
    'lat': [48.521619, 48.7782, 48.9602260],  
    'lon': [2.182400,  2.45426,2.5428670]  
}
df = pd.DataFrame(data)
# --- STYLE CSS (Minimaliste & Zen) ---
st.markdown(f"""
<style>
/* Style général pour ambiance zen et les couleurs du projet */
.stApp {{
    background-color: {COLOR_BLANC};
    color: {COLOR_MARRON};
}}
/* Boutons */
.stButton>button, .css-qbe2i3, .css-1aum3gq {{
    background-color: {COLOR_BEIGE} !important;
    color: {COLOR_MARRON} !important;
    border: 1px solid {COLOR_MARRON};
    border-radius: 5px;
}}
.stButton>button:hover, .css-qbe2i3:hover, .css-1aum3gq:hover {{
    background-color: {COLOR_MARRON} !important;
    color: {COLOR_BLANC} !important;
}}
/* Titres */
h1, h2, h3, h4, .css-10trblm {{
    color: {COLOR_MARRON};
}}
/* Footer */
.footer {{
    position: fixed; 
    bottom: 0; 
    width: 100%; 
    background-color: {COLOR_BEIGE}; 
    color: {COLOR_MARRON}; 
    text-align: center; 
    padding: 10px 0; 
    font-size: 14px; 
    border-top: 1px solid {COLOR_MARRON};
}}
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
def render_header():
    col_logo, col_menu, col_auth = st.columns([2, 5, 2])
    with col_logo:
        try:
            st.image("assets/logo.png", width=65)
        except FileNotFoundError:
            st.markdown("<h2 class='header_logo'> Minerals</h2>", unsafe_allow_html=True)
            st.caption("Fichier logo.png non trouvé. Utilisation du texte de secours.")
    with col_menu:
        menu_items = ["Accueil", "Nos Soins", "Personnalisation", "À propos", "Contact"]
        page_to_index = {"accueil": 0, "soins": 1, "personnalisation": 2, "a_propos":3, "contact":4}
        default_index = page_to_index.get(st.session_state.page, 0)
        selected_menu = st.radio("Menu", menu_items, index=default_index, horizontal=True, label_visibility="collapsed", key="main_menu")
        main_menu_pages = page_to_index.keys()
        
        if selected_menu == "Accueil" and st.session_state.page != "accueil":
            if st.session_state.page in main_menu_pages:
                set_page("accueil")
        elif selected_menu == "Nos Soins" and st.session_state.page != "soins": set_page("soins")
        elif selected_menu == "À propos" and st.session_state.page != "a_propos": set_page("a_propos")
        elif selected_menu == "Personnalisation" and st.session_state.page != "personnalisation": set_page("personnalisation")
        elif selected_menu == "Contact" and st.session_state.page != "contact": set_page("contact")
        
    with col_auth:
        if st.session_state.authentification:
            if st.button(" Mon espace", key="btn_mon_espace_top"):
                set_page("mon_espace")
        else:
            if st.button("Se connecter / S'inscrire", key="btn_conn_inscr"):
                set_page("connexion")
    st.markdown("---")
    
# --- DÉBUT DE LA LOGIQUE DES PAGES ---

# PAGE CGU - Page de démarrage
if st.session_state.page == "cgu":
    st.markdown(f"<h1 style='text-align:center; color:{COLOR_MARRON};'>Bienvenue sur Minerals</h1>", unsafe_allow_html=True)
    st.markdown("""
        ### Conditions Générales d’Utilisation (CGU)
        Veuillez accepter nos conditions avant de continuer :
        * Service d'information et de prise de rendez-vous pour des soins de bien-être.
        * Vos données (humeur, score, réservations) sont enregistrées dans un fichier CSV pour analyse interne.
        * Respect des données personnelles.
    """)
    if st.button("J’accepte les conditions d’utilisation", use_container_width=True, key="cgu_accept_btn", type="primary"):
        st.session_state.cgu_accepted = True
        set_page("accueil") 
    st.stop()

# Si CGU acceptées, affichage du Header pour toutes les autres pages
if st.session_state.cgu_accepted:
    render_header()

# --- PAGE ACCUEIL ---
if st.session_state.page == "accueil":
    # Bannière
    col1, col2 = st.columns([1, 3])
    with col1:
        img_path = HEADER_IMAGES_PLACEHOLDERS[st.session_state.header_index]
        if os.path.exists(img_path):
            st.image(img_path, width=200, use_container_width=False)
        else:
            st.warning("Image du header introuvable : " + img_path)
    with col2:
        st.markdown("""
        <div style='font-style: italic; color:#000000; line-height:1.7;'>
            <p> Plus d'évasion, profitez de nos services exclusifs. N'hésitez pas à réserver vos places au plus vite pour une expérience sensorielle unique.</p>
            <p>Découvrez la quiétude et l'harmonie au cœur de chaque soin, pensés pour revitaliser corps et esprit.</p>
            <p>Chez <strong>Minerals</strong>, chaque instant est une invitation au bien-être, à la beauté et à la sérénité.</p>
            <p>Laissez-vous emporter par nos rituels exclusifs, inspirés des minéraux les plus purs et des traditions du monde entier.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")

    # Filtre par soin et ville
    st.markdown("<h1 style='text-align:center;'>Trouvez votre soin idéal</h1>", unsafe_allow_html=True)
    st.subheader("Sélectionnez votre région")
    col_ville, col_soin = st.columns(2)
    with col_ville:
        selected_ville = st.selectbox("Sélectionnez votre ville", list(INSTITUTS.keys()), key="select_ville_accueil")
    with col_soin:
        soins_disponibles = ["Massage bien-être", "Soins minceur", "Soin visage", "Tous les soins"]
        st.selectbox("Sélectionnez le type de soin", soins_disponibles, key="select_soin_accueil")

    st.markdown("---")
    
    # Affichage des instituts
    instituts_affiches = INSTITUTS.get(selected_ville, [])
    
    if instituts_affiches:
        st.subheader(f"Instituts disponibles à {selected_ville}")
        for institut_nom in instituts_affiches:
            st.markdown(f"**{institut_nom}**")
            st.write("Spa de luxe avec soins personnalisés.") 
            st.markdown("⭐" * random.randint(3, 5))
            
            # Bouton Réserver
            if st.button(f"Réserver chez {institut_nom}", key=f"res_{institut_nom.replace(' ', '_')}"):
                st.session_state.selected_institut = institut_nom
                set_page("reservation")
            st.markdown("---")
    else:
        st.info(f"Aucun institut trouvé pour {selected_ville}.")

# --- PAGE RESERVATION ---
elif st.session_state.page == "reservation":
    institut_nom = st.session_state.get("selected_institut", "un institut")
    st.header(f"Réservation chez {institut_nom}")
    print(st.session_state.authentification)
    
    if st.session_state.authentification == False:
        st.info("Veuillez vous connecter ou créer un compte pour choisir une séance et réserver (300).")
        colA, colB = st.columns(2)
        with colA:
            if st.button("Se connecter", key="btn_res_connex_page", use_container_width=True):
                set_page("connexion")
        with colB:
            if st.button("Créer un compte", key="btn_res_create_page", use_container_width=True):
                set_page("connexion")
    else:
        st.subheader(f"Bienvenue, {st.session_state.email}!")
        
        col_select, col_calendar = st.columns([3, 2])

        with col_select: 
            st.markdown("### Choisissez votre séance et l'heure")
            col_date, col_heure, col_soin = st.columns(3)
            soins = {
            "Massage dos anti-stress (30 min - 45€)": 45,
            "Massage thaï (1h - 70€)": 70,
            "Drainage lymphatique (1h - 110€)": 110,
            "Soin visage purifiant (1h - 50€)": 50,
        }
        with col_date:
            st.markdown("### Choisissez votre séance et l'heure")
            col_date, col_heure, col_soin = st.columns(3)
            soins = {
                "Massage dos anti-stress (30 min - 45€)": 45,
                "Massage thaï (1h - 70€)": 70,
                "Drainage lymphatique (1h - 110€)": 110,
                "Soin visage purifiant (1h - 50€)": 50,
            }
            with col_date:
                selected_date = st.date_input("Date", datetime.date.today(), key="res_date")
            with col_heure:
                selected_heure = st.time_input("Heure", datetime.time(14, 0), key="res_heure")
            with col_soin:
                selected_soin_res = st.selectbox("Soins disponibles", list(soins.keys()), key="res_soin")
            prix_estime = soins.get(selected_soin_res, 0)
            st.markdown(f"**Prix estimé:** {soins.get(selected_soin_res, 0)}€")
        
        with col_calendar: 
            st.markdown("### Calendrier")
            if 'CALENDAR_AVAILABLE' in globals() and CALENDAR_AVAILABLE:
                calendar_options = {
                    "headerToolbar": {
                        "left": "today prev,next",
                        "center": "title",
                        "right": "dayGridMonth,timeGridWeek"
                    },
                    "initialView": "dayGridMonth",
                    "editable": False,
                    "locale": "fr",
                }
                calendar_events = []
                start_date = selected_date.isoformat()
                for resa in st.session_state.reservations:
                    try:
                        calendar_events.append(
                            {
                            "title": resa.get("soin", "Rendez-vous"),
                            "start": f"{resa['date']}T{resa['heure']}",
                            "color": COLOR_MARRON, 
                            }
                        )
                    except:
                        pass
                calendar(
                    events=calendar_events,
                    options=calendar_options,
                    custom_css="""
                        .fc-event-title { color: white !important; }
                        .fc-event { background-color: #5c4329 !important; border-color: #5c4329 !important; }
                    """,
                    key="full_calendar_view"
                )
            else:
                st.warning("Le composant 'streamlit_calendar' n'est pas disponible. Exécutez 'pip install streamlit-calendar' pour l'activer.")
        
        if st.button("Confirmer la Réservation", key="btn_confirmer_resa", type="primary", use_container_width=True):
            prix_estime_int = soins.get(st.session_state.res_soin, 0)
            new_resa = {
                "email": st.session_state.email,
                "institut": institut_nom,
                "date": selected_date.strftime("%d/%m/%Y"),
                "heure": selected_heure.strftime("%H:%M"),
                "soin": selected_soin_res,
                "prix": soins.get(selected_soin_res, 0)
            }
            st.session_state.reservations = new_resa
            reservation(st.session_state.email,institut_nom,selected_date.strftime("%d/%m/%Y"),selected_heure.strftime("%H:%M"),selected_soin_res)
            st.success(
                """
                ** Votre rendez-vous a été confirmé !**
                * **Récapitulatif de votre réservation :**
                    * Date : {date}
                    * Heure : {heure}
                    * Soin : {soin}
                    * Prix estimé : {prix}
                
                Un récapitulatif complet a été envoyé à votre adresse e-mail.
                """.format(**new_resa)
            )
            
            st.info("Réservation confirmée ! Redirection vers 'Mon Espace'...")
            set_page("mon_espace")

# --- PAGE CONNEXION ---
elif st.session_state.page == "connexion":
    st.header("Connexion / Création de compte")
    
    col_conn, col_insc = st.columns(2)
    
    with col_conn:
        st.subheader("Se connecter")
        with st.form("login_form", clear_on_submit=False):
            email = st.text_input("Identifiant", key="login_email_input")
            password = st.text_input("Mot de passe ", type="password", key="login_password_input")
            submit_login = st.form_submit_button("Se connecter", type="primary", use_container_width=True)
            if submit_login:
                if(login(email,password) == 0):
                    prenom = st.session_state.prenom
                    st.session_state.authentification = True
                    st.success(f"Bienvenue {prenom} Connexion réussie !")
                    set_page("reservation")
                else:
                    st.error("Identifiant ou mot de passe incorrect ")
    
    with col_insc:
        st.subheader("Créer un compte")
        with st.form("inscription_form", clear_on_submit=False):
            username = st.text_input("Nom d'utilisateur", key="insc_username")
            email_insc = st.text_input("Adresse mail", key="insc_email")
            password = st.text_input("Mot de passe", type="password", key="insc_password")
            submit_insc = st.form_submit_button("S'inscrire", type="primary", use_container_width=True)
            if submit_insc:
                if sign_up(email_insc,password,username) == 0 :
                    st.session_state.authentification = True
                    st.success("Inscription réussie !")
                    set_page("reservation")
                else:
                    st.error("Erreur lors de l'inscription ")
                

# --- PAGE SOINS (Détail des soins) ---
elif st.session_state.page == "soins":
    st.header("Notre Carte de Soins")
    
    # Types de soins
    soins_categories = {
        "Massage bien-être & sportif": [
            ("Massage dos anti-stress", "30 minutes", "45€", "Détente profonde des tensions du dos. Idéale en cas de stress ou de fatigue."),
            ("Massage thaï aux huiles chaudes", "1 heure", "70€", "Étirements doux, pression ciblée et énergie rééquilibrées."),
            ("Massage jambes lourdes", "35 minutes", "50€", "Active la circulation, diminue les gonflements et offre une sensation de jambes légères.")
        ],
        "Soins minceur & drainage lymphatique": [
            ("Drainage lymphatique Signature", "1 heure", "110€", "Drainage manuel complet pour activer la circulation, détoxifier et affiner."),
            ("Traitement du relâchement cutané par radiofréquence menton", "30 minutes", "30€", "Redéfinit le bas du visage, raffermit et améliore le profil."),
            ("Combo drainage ou Lipo + Sauna infrarouge", "1h 30 minutes", "150€", "Triple action : élimination des toxines, réduction de graisse, sudation profonde. Idéale pour une perte de poids.")
        ],
        "Soin visage": [
            ("Soin purifiant anti-imperfection", "1h", "50€", "Nettoyage en profondeur, désincrustation, masque purifiant. Peau nette et pores resserrés."),
            ("Soin coup d'éclat express", "30 minutes", "50€", "Nettoyage et masque éclat pour un résultat immédiat. Parfait avant un évènement."),
            ("Peeling Glycolique", "1h", "150€", "Peeling rénovateur pour teints ternes ou irréguliers."),
            ("Soin anti-rides au rétinol", "1h", "120€", "Lisse les ridules, booste le renouvellement cellulaire."),
            ("Peeling mandelique anti-tâche", "1h", "120€", "Corrige les tâches, lisse la texture de la peau et convient aux peaux sensibles.")
        ]
    }
    
    for category, soins in soins_categories.items():
        st.markdown(f"### {category}")
        for nom, duree, prix, description in soins:
            st.markdown(f"**{nom}** - {duree} pour **{prix}**")
            st.caption(description)
        st.markdown("---")

# --- PAGE MON ESPACE ---
elif st.session_state.page == "mon_espace":
    if not st.session_state.authentification:
        st.warning("Veuillez vous connecter pour accéder à votre espace.")
        if st.button("Connexion", key="btn_espace_connexion"):
            set_page("connexion")
        st.stop()
    if "reservations" not in st.session_state or not isinstance(st.session_state.reservations, dict):
         st.session_state.reservations = {}
    
    # -------------------------
    # LAYOUT GLOBAL
    # -------------------------   
    st.header(f"Mon Espace Personnel {st.session_state.email}")
    st.markdown("---")
    
    col_menu, col_content = st.columns([1, 3])   
    username = st.session_state.get("username", "Utilisateur")

    # =============================
    # BARRE LATÉRALE
    # =============================
    with col_menu:
        menu_items = ["Mes informations", "Mes réservations", "Mon bilan quotidien", "Mes recommandations"]
        for item in menu_items:
            if st.button(item, key=f"me_{item}", use_container_width=True):
                st.session_state.monespace_section = item
        if st.button(" Déconnexion", key="btn_deconnexion", use_container_width=True):
            st.session_state.authentification = False
            st.session_state.email = ""
            st.session_state.reservations = []
            st.success("Vous êtes déconnecté.")
            set_page("accueil")

    with col_content:
        section = st.session_state.monespace_section

        # === INFOS ===
        if section == "Mes informations":
            st.subheader("Informations personnelles")
            st.write(f"**Nom d'utilisateur :** {username}")
            mail = next((k for k, v in st.session_state.users.items() if v.get("username") == username), "Non renseigné")
            st.write(f"**Adresse e-mail :** {mail}")
            st.info("Vos données sont sécurisées et ne seront jamais partagées.")

        # === BILAN ===
        elif section == "Mon bilan quotidien":
            st.subheader("Bilan du jour")
            # ---------------------------
            # ➕ AJOUT MANUEL D’UNE ACTIVITÉ
            # ---------------------------
            st.markdown("---")
            st.markdown("### Ajouter une activité de bien-être")

            col1, col2 = st.columns([2, 1])
            with col1:
                activity_title = st.text_input("Nom de l’activité", placeholder="Ex: Méditation, balade, lecture...")
            with col2:
                activity_date = st.date_input("Date", datetime.date.today())

            if st.button("Ajouter l’activité", use_container_width=True, type="primary"):
                if activity_title:
                    add_event(activity_title, activity_date)
                    st.success(f" Activité '{activity_title}' ajoutée avec succès !")
                    st.session_state.rerun_flag = True
                else:
                    st.warning("Veuillez entrer un nom d’activité avant d’ajouter.")

            today = str(datetime.date.today())
            if today not in st.session_state.bilan:
                st.session_state.bilan[today] = {
                    "Hydratation (1L minimum)": False,
                    "Massage ou soin du corps": False,
                    "Routine visage complète": False,
                    "Moment de détente / respiration": False,
                    "Séance de sport": False,
                    "Méditation": False,
                    "Sommeil réparateur (7h+)": False,
                }

            st.write("Cochez vos actions bien-être du jour :")

            for action in st.session_state.bilan[today].keys():
                st.session_state.bilan[today][action] = st.checkbox(
                    action, value=st.session_state.bilan[today][action]
                )

            # Score en direct
            total_actions = len(st.session_state.bilan[today])
            done = sum(st.session_state.bilan[today].values())
            progress = int((done / total_actions) * 100)

            # Barre de progression
            st.markdown(f"""
            <div class="progress-bar">
                <div class="progress" style="width:{progress}%;">
                    {progress}%
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Message dynamique
            if progress == 0:
                st.info("Commencez votre journée bien-être 🌿")
            elif progress < 60:
                st.info("Très bien ! Continuez, vous y êtes presque 💪")
            elif progress < 100:
                st.success("Super ! Encore un petit effort pour tout compléter ✨")
            else:
                st.success("Bravo ! Vous avez complété toutes vos actions du jour !")

            # Bouton Enregistrer
            if st.button("Enregistrer ma journée"):
                put_score(st.session_state.email,progress,activity_date)

                add_daily_score()
                with st.spinner("Mise à jour de votre progression..."):
                    time.sleep(1)
                st.toast("Votre progression du jour a été enregistrée !")

            st.markdown('</div>', unsafe_allow_html=True)

            # =============================
            # PROGRESSION MENSUELLE
            # =============================
            st.markdown("<hr>", unsafe_allow_html=True)
            st.subheader("Bilan du mois")

            df = get_monthly_scores()
            if df.empty:
                st.info("Aucune donnée enregistrée pour le moment. Commencez votre premier bilan dès aujourd’hui !")
                st.stop()

            # --- graphique + récompense côte à côte
            col_graph, col_reward = st.columns([2, 1], gap="large")
            with col_graph:
                st.markdown("Évolution du mois")
                fig, ax = plt.subplots(figsize=(4.5, 2.5))
                ax.plot(df["Date"], df["Score"], marker="o", linewidth=1.5, color="black")
                ax.fill_between(df["Date"], df["Score"], color="#ebe1d6", alpha=0.5)
                ax.set_xlabel("Date", fontsize=4)
                ax.set_ylabel("Score", fontsize=4)
                ax.set_title("Progression du mois", fontsize=5, color="black")
                ax.tick_params(axis='both', labelsize=7)
                ax.grid(True, alpha=0.3)
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                plt.tight_layout(pad=0.5)
                st.pyplot(fig, use_container_width=True)

            with col_reward:
                st.markdown("Récompense du mois")
                score_total = df["Score"].sum()
                badge, message = get_badge_from_score(score_total)

                moyenne = df["Score"].mean()
                percent = min(100, moyenne * 10)

                # Indicateur circulaire animé
                st.markdown(f"""
                    <div style='display:flex;justify-content:center;margin:10px;'>
                        <svg width="120" height="120" viewBox="0 0 36 36">
                            <path d="M18 2.0845
                                a 15.9155 15.9155 0 0 1 0 31.831
                                a 15.9155 15.9155 0 0 1 0 -31.831"
                                fill="none" stroke="#ebe1d6" stroke-width="2"/>
                            <path d="M18 2.0845
                                a 15.9155 15.9155 0 0 1 0 31.831"
                                fill="none" stroke="#5c4329" stroke-width="2"
                                stroke-dasharray="{percent},100" stroke-linecap="round">
                                <animate attributeName="stroke-dasharray"
                                    from="0,100" to="{percent},100"
                                    dur="1s" fill="freeze" />
                            </path>
                            <text x="18" y="20.35" fill="#5c4329"
                                text-anchor="middle" font-size="6">{moyenne:.1f}/10</text>
                        </svg>
                    </div>
                """, unsafe_allow_html=True)

                # Texte de récompense
                st.markdown(f"<p style='text-align:center;color:#000000;'>{message}</p>", unsafe_allow_html=True)

                seuil = 30
                if score_total >= seuil:
                    st.success("Promotion débloquée : récompense exclusive ! 💎")
                else:
                    st.info(f"Encore {seuil - score_total} points avant la prochaine récompense 🌸")
  
    # === RÉSERVATIONS ===
        elif section == "Mes réservations":
            st.subheader("Mes réservations")
            user_resas =  afficher_reservation(st.session_state.email)
            calendar_events=[]
            if user_resas:
                for r in user_resas:
                    try: 
                        date_obj = datetime.datetime.strptime(r['date'], "%d/%m/%Y").date()
                        calendar_events.append({
                        "title": r["soin"],
                        "start": f"{date_obj.isoformat()}T{r['heure']}", 
                        "color": COLOR_MARRON,
                    })
                    except Exception as e:
                        st.warning(f"Erreur de format de réservation : {e}")

                if 'CALENDAR_AVAILABLE' in globals() and CALENDAR_AVAILABLE:
                    calendar_options = {
                        "headerToolbar": {
                            "left": "today prev,next",
                            "center": "title",
                            "right": "dayGridMonth,listWeek" 
                        },
                        "initialView": "dayGridMonth",
                        "height": 450,
                        "editable": False,
                        "selectable": False,
                        "locale": "fr",
                    }
                    with st.container():
                        st.markdown("#####Calendrier des Rendez-vous")
                        calendar(
                            events=calendar_events, 
                            options=calendar_options,
                            custom_css="""
                                .fc-event-title { color: white !important; }
                                .fc-event { background-color: #5c4329 !important; border-color: #5c4329 !important; }
                            """,
                            key="mon_espace_calendar"
                        )
                else:
                    st.info("Le composant 'streamlit_calendar' n'est pas disponible pour l'affichage visuel.")
                st.markdown("#### Détails des Réservations")
                if user_resas:
                    for r in user_resas:
                        st.write(f"**Institut:** {r.get('institut', 'N/A')}")
                        st.write(f"**Date:** {r['date']}")
                        st.write(f"**Heure:** {r['heure']}")
                        st.write(f"**Soin:** {r['soin']}")
                        st.write(f"**Prix estimé:** {r.get('prix', 'N/A')}")
                        st.markdown("---")
                else:
                    st.info("Vous n'avez aucune réservation de soin de bien-être planifiée.")
                        
                # ---------------------------
                # GESTION DES ANNULATIONS
                # ---------------------------
                st.markdown("### Gérer vos réservations")

                for i, resa in enumerate(user_resas):
                    colA, colB = st.columns([3, 1])
                    with colA:
                        st.write(f"{resa['date']} – {resa['soin']}")
                    with colB:
                        if st.session_state.confirm_cancel is None:
                            if st.button("Annuler", key=f"annuler_{i}"):
                                st.session_state.confirm_cancel = i

                # Confirmation d'annulation
                if st.session_state.confirm_cancel is not None:
                    i = st.session_state.confirm_cancel
                    if i < len(user_resas): 
                        resa = user_resas[i]
                        st.warning(f"Êtes-vous sûr de vouloir annuler votre réservation du **{resa['date']} - {resa['soin']}** ?")
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("Oui, annuler", key=f"oui_{i}"):
                                delete_reservation(user_resas[i])
                                st.session_state.reservations[username] = user_resas
                                st.session_state.confirm_cancel = None
                                st.success("Réservation annulée !")
                                st.rerun() 
                        with col2:
                            if st.button("Non", key=f"non_{i}"):
                                st.session_state.confirm_cancel = None
                                st.info("La réservation est conservée.")
                    else:
                        st.session_state.confirm_cancel = None
                        st.rerun()
            else:
                st.info("Vous n'avez aucune réservation pour le moment.")
     
        # === RECOMMANDATIONS ===
        elif section == "Mes recommandations":
            st.subheader("Mes recommandations beauté")
            last_quiz = st.session_state.get("last_quiz_result")

            if last_quiz:
                st.image(last_quiz.get("image"), caption=last_quiz.get("titre"), use_container_width=True)
                st.markdown(f"**{last_quiz['titre']}** — {last_quiz['prix']} ({last_quiz['duree']})")
                st.write(last_quiz["description"])

                if st.button(f"Réserver {last_quiz['titre']}", type="primary"):
                    st.session_state.selected_soin_reco = last_quiz['titre']
                    st.session_state.page = "reservation" 
                    st.rerun()

            else:
                st.info("Aucune recommandation disponible. Faites le test dans l’onglet **Personnalisation**.")

# --- PAGE PERSONNALISATION ---
elif st.session_state.page == "personnalisation":
    st.header("Quiz de Personnalisation : Trouvez votre soin idéal")
    st.info("Répondez à quelques questions pour obtenir une recommandation personnalisée.")
    
    if "quiz" not in st.session_state:
        st.session_state.quiz = {}

    # -------------------- QUESTION 1 --------------------
    st.markdown('<div class="question"> Quelle est votre principale préoccupation ?</div>', unsafe_allow_html=True)
    q1 = st.radio(
        "",
        ["Stress / Fatigue", "Tensions musculaires", "Teint terne ou fatigué", "Rétention d’eau ou jambes lourdes", "Perte de fermeté", "Tâches ou rides apparentes"],
        key="q1"
    )
    st.session_state.quiz["preoccupation"] = q1

    # -------------------- QUESTION 2 --------------------
    st.markdown('<div class="question"> Quelle zone souhaitez-vous cibler en priorité ?</div>', unsafe_allow_html=True)
    q2 = st.radio(
        "",
        ["Visage", "Corps complet", "Dos / Jambes", "Bas du visage (menton / cou)"],
        key="q2"
    )
    st.session_state.quiz["zone"] = q2

    # -------------------- QUESTION 3 --------------------
    st.markdown('<div class="question"> Quelle intensité préférez-vous pour un soin ou massage ?</div>', unsafe_allow_html=True)
    q3 = st.slider("De 1 (très doux) à 10 (très intense)", 1, 10, 5, key="q3")
    st.session_state.quiz["intensite"] = q3

    # -------------------- QUESTION 4 --------------------
    st.markdown('<div class="question"> Cherchez-vous un effet immédiat ou sur la durée ?</div>', unsafe_allow_html=True)
    q4 = st.radio(
        "",
        ["Effet immédiat (relaxation ou éclat rapide)", "Résultat durable (minceur, raffermissement, anti-âge)"],
        key="q4"
    )
    st.session_state.quiz["effet"] = q4

    # -------------------- QUESTION 5 --------------------
    st.markdown('<div class="question"> Quelle texture ou ambiance préférez-vous ?</div>', unsafe_allow_html=True)
    q5 = st.radio(
        "",
        ["Huiles chaudes relaxantes", "Produits frais et tonifiants", "Masques visage / textures douces"],
        key="q5"
    )
    st.session_state.quiz["ambiance"] = q5

    # -------------------- QUESTION 6 --------------------
    st.markdown('<div class="question"> Quel est votre objectif principal ?</div>', unsafe_allow_html=True)
    q6 = st.selectbox(
        "",
        ["Détente & anti-stress", "Raffermir & tonifier", "Éliminer les toxines / affiner", "Illuminer le teint", "Corriger rides ou tâches"],
        key="q6"
    )
    st.session_state.quiz["objectif"] = q6

    # -------------------- SUBMIT --------------------
    
    st.divider()
    if st.button("Découvrir mon soin idéal", key="btn_result"):
        result = get_recommendation(st.session_state.quiz)

        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.markdown(f" {result['titre']}")
        st.write(result["description"])
        st.image(result["image"], use_container_width=True)
        st.markdown(f"Prix : {result['prix']} — {result['duree']}")
        st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE A PROPOS ---
elif st.session_state.page == "a_propos":
    st.markdown("<h1 style='text-align:center;'>Minerals</h1>", unsafe_allow_html=True)

    # --- Section 1: Mission & Image Ambiance ---
    col_text1, col_img1, col_maps = st.columns([2, 2, 2])
    with col_text1:
        st.markdown("""
        <div style='text-align:left; font-size:18px;'>
            <p>Chez <strong>Minerals</strong>, nous croyons au pouvoir de la nature et de la sérénité.</p>
            <p>Notre mission est de vous offrir une évasion sensorielle complète, combinant l'expertise de nos thérapeutes et les bienfaits des produits naturels pour une revitalisation complète du corps et de l'esprit.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_img1:
        if os.path.exists("assets/a_propos2.jpeg", ):
            st.image("assets/a_propos2.jpeg", width=300, caption="Le sanctuaire Minerals", use_container_width=False)
        else:
            st.warning("Le sanctuaire Minerals")
    with col_maps: 
        st.markdown("""Nos boutiques""")
        st.map(df, zoom=5)

    # --- Section 2: Valeurs & Image Expertise ---
    col_img2, col_text2 = st.columns([4, 3])
    
    with col_img2:
        if os.path.exists("assets/a_propos1.jpeg"):
            st.image("assets/a_propos1.jpeg", width=300, caption="Expertise et douceur", use_container_width=FloatingPointError)
        else:
            st.warning("Notre team d'amour")
            
    with col_text2:
        st.subheader("Nos Valeurs Fondamentales")
        st.markdown("""
        * **Authenticité :** Utilisation de minéraux et d'ingrédients bruts, sourcés éthiquement.
        * **Expertise :** Thérapeutes hautement qualifiés et formés aux techniques du monde entier.
        * **Personnalisation :** Chaque soin est adapté à vos besoins uniques et à votre profil bien-être.
        """)
    
    st.markdown("---")
    
    st.subheader("Contactez-nous")
    st.info("Prêt à commencer votre voyage de bien-être ? Contactez-nous pour toute information ou prise de rendez-vous.")
    if st.button("Contactez-nous", key="btn_go_contact_apropos", type="primary"):
        set_page("contact")

# --- PAGE CONTACT ---
elif st.session_state.page == "contact":
    st.markdown("<h1 style='text-align:center; color:#000000;'>Contactez-nous</h1>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align:center; font-size:18px; color:#000000;'>
        <p>Une question, un besoin d’information ou une demande particulière ?</p>
        <p>Notre équipe est à votre écoute </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # --- Formulaire de contact ---
    with st.form("contact_form"):
        nom = st.text_input("Votre nom")
        email = st.text_input("Votre e-mail")
        message = st.text_area("Votre message")
        submit = st.form_submit_button("Envoyer")

        if submit:
            if nom.strip() and email.strip() and message.strip():
                st.success("Merci pour votre message. Nous vous répondrons très bientôt !")
            else:
                st.error("Veuillez remplir tous les champs avant d’envoyer.")

    st.markdown("---")

    # --- Image illustrant le contact ---
    col1, col2 = st.columns([2, 3])
    with col1:
        st.image("assets/contact1.jpeg", use_container_width=True)
    with col2:
        st.image("assets/contact2.jpeg", width=350, use_container_width=False)

# --- FOOTER ---
st.markdown("""
<div class="footer">
    © 2025 Minerals | 
    <a href="#" style="color: #5c4329; text-decoration: none; font-weight: bold;">Conditions Générales d’Utilisation</a> | 
    <a href="#" style="color: #5c4329; text-decoration: none; font-weight: bold;">Politique de Confidentialité</a>
</div>
""", unsafe_allow_html=True)