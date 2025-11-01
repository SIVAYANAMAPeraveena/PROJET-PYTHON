import streamlit as st
import datetime
import pandas as pd
import random
import time

# --- COULEURS GLOBALES ---
COLOR_BLANC = "#ffffff"
COLOR_BEIGE = "#ebe1d6"
COLOR_MARRON = "#5c4329"

def init_session():
    """Initialise tous les états de session nécessaires."""
    if "users" not in st.session_state:
        # Utilisateur de test pour la démo
        st.session_state.users = {"test@test.com": {"username": "DemoUser", "password": "0000", "birthday": "1990-01-01"}}
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "username" not in st.session_state:
        st.session_state.username = None
    if "page" not in st.session_state:
        st.session_state.page = "cgu" # Démarre sur CGU
    if "reservations" not in st.session_state:
        st.session_state.reservations = [] 
    if "bilan" not in st.session_state:
        st.session_state.bilan = {} # {date: {task: checked}}
    if "last_quiz_result" not in st.session_state:
        st.session_state.last_quiz_result = None
    if "cgu_accepted" not in st.session_state:
        st.session_state.cgu_accepted = False

# --- FONCTIONS DE RENDU (Pages) ---

def set_page(page_name):
    st.session_state.page = page_name
    st.rerun()

def render_circle_badge(score_total):
    badge, msg = get_badge_from_score(score_total)
    
    MAX_SCORE_DISPLAY = 150 
    
    percent = min(100, (score_total / MAX_SCORE_DISPLAY) * 100) 
    
    # Paramètres SVG pour un cercle de rayon 15.9155 (circonférence = 100)
    radius = 15.9155
    circumference = 2 * 3.14159 * radius
    stroke_dashoffset = circumference - (percent / 100) * circumference
    
    st.markdown(f"""
        <div class="circle-progress-container">
            <h3 style="color:{COLOR_MARRON};">Récompense du mois</h3>
            <svg width="120" height="120" viewBox="0 0 36 36">
                <!-- Cercle de fond -->
                <circle class="progress-ring-circle-bg"
                    cx="18" cy="18" r="{radius}">
                </circle>
                <!-- Arc de progression -->
                <circle class="progress-ring-circle-fg"
                    cx="18" cy="18" r="{radius}"
                    stroke-dasharray="{circumference} {circumference}"
                    stroke-dashoffset="{circumference}"
                    style="stroke-dashoffset: {stroke_dashoffset};">
                </circle>
                <!-- Texte au centre (score) -->
                <text x="18" y="20.35" text-anchor="middle" font-size="6" fill="{COLOR_MARRON}">
                    {score_total} pts
                </text>
            </svg>
            <div class="badge-title">🏆 {badge}</div>
            <small style="text-align:center; display:block;">{msg}</small>
        </div>
    """, unsafe_allow_html=True)

# --- FONCTIONS UTILITAIRES DE GESTION DE DONNÉES ---

def is_authenticated():
    return st.session_state.get("authenticated", False)

def get_monthly_scores():
    today = datetime.date.today()
    current_month_str = today.strftime("%Y-%m")
    
    data = []
    for date_str, score in st.session_state.get("scores", {}).items():
        try:
            date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            if date_obj.strftime("%Y-%m") == current_month_str:
                data.append({"Date": date_obj, "Score": score})
        except ValueError:
            continue
            
    df = pd.DataFrame(data)
    if not df.empty:
        df = df.sort_values(by="Date").reset_index(drop=True)
    return df

def get_badge_from_score(score):
    if score >= 30:
        return "Diamant", "Félicitations ! Vous êtes notre client le plus fidèle. Profitez d'une réduction de 20% sur votre prochain soin."
    elif score >= 20:
        return "Saphir", "Excellent travail ! Vous avez gagné un soin du visage offert."
    elif score >= 10:
        return "Émeraude", "Bonne progression ! Vous avez accès aux vidéos bien-être Premium du mois."
    else:
        return "Quartz", "Continuez votre chemin vers le bien-être. Accumulez plus de points pour débloquer votre première récompense."

def add_event(activity_title, activity_date):
    date_str = activity_date.isoformat() if isinstance(activity_date, (datetime.date, datetime.datetime)) else str(activity_date)
    if not any(e["title"] == activity_title and e["date"] == date_str for e in st.session_state["events"]):
        st.session_state["events"].append({"title": activity_title, "date": date_str})
    # Recalculer le score dynamiquement
    st.session_state.score = len(st.session_state["events"]) * 10

def header():
    col_logo, col_menu, col_auth = st.columns([2, 5, 2])
    
def apply_global_styles():
    st.markdown(f"""
    <style>
    /* Styles généraux */
    .stApp {{ background-color: {COLOR_BLANC}; color: {COLOR_MARRON}; }}
    h1, h2, h3, h4, .css-10trblm {{ color: {COLOR_MARRON}; }}
    /* Boutons */
    .stButton>button, .css-qbe2i3, .css-1aum3gq, .css-1cpx96c, .stTabs button {{
        background-color: {COLOR_BEIGE} !important; color: {COLOR_MARRON} !important;
        border: 1px solid {COLOR_MARRON}; border-radius: 5px;
    }}
    .stButton>button:hover, .css-qbe2i3:hover, .css-1aum3gq:hover, .css-1cpx96c:hover, .stTabs button:hover {{
        background-color: {COLOR_MARRON} !important; color: {COLOR_BLANC} !important;
    }}
    /* Tabs actifs */
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {{
        background-color: {COLOR_MARRON} !important;
        color: {COLOR_BLANC} !important;
    }}
    </style>
    """, unsafe_allow_html=True)

def header():
    col_logo, col_menu, col_auth = st.columns([2, 5, 2])
    with col_logo:
        st.markdown(f"<h2 class='header_logo' style='color:{COLOR_MARRON};'>💎 Minerals</h2>", unsafe_allow_html=True)
    with col_menu:
        menu_items = ["Accueil", "Soins", "Personnalisation", "À propos"]
        page_to_index = {"accueil": 0, "soins": 1, "personnalisation": 2, "a_propos": 3}
        default_index = page_to_index.get(st.session_state.page, 0)
        
        selected_menu = st.radio("Menu", menu_items, index=default_index, horizontal=True, label_visibility="collapsed", key="main_menu")
        
        if selected_menu == "Accueil": set_page("accueil")
        elif selected_menu == "Soins": set_page("soins")
        elif selected_menu == "Personnalisation": set_page("personnalisation")
        elif selected_menu == "À propos": set_page("a_propos")
    
    with col_auth:
        if is_authenticated():
            if st.button("Mon espace", key="btn_mon_espace_top"):
                set_page("mon_espace")
        else:
            if st.button("e connecter / S'inscrire", key="btn_conn_inscr"):
                set_page("connexion")
    st.markdown("---")

def update_daily_bilan(key, value):
    today = str(datetime.date.today())
    if today in st.session_state.bilan and key in st.session_state.bilan[today]:
        st.session_state.bilan[today][key] = value

def add_daily_score():
    today = str(datetime.date.today())
    if today not in st.session_state.bilan:
        return
    total = sum(st.session_state.bilan[today].values())
    st.session_state.scores[today] = total

def get_recommendation(quiz):
    # Massage détente
    if quiz["preoccupation"] in ["Stress / Fatigue", "Tensions musculaires"] and quiz["zone"] in ["Dos / Jambes", "Corps complet"]:
        if quiz["intensite"] <= 5:
            return {
                "titre": "Massage dos anti-stress (30 min)",
                "description": "Détente profonde des tensions du dos, idéale pour le stress ou la fatigue.",
                "prix": "45€",
                "duree": "30 minutes",
                "image": "https://images.unsplash.com/photo-1616690710400-a16d86e09d36"
            }
        else:
            return {
                "titre": "Massage thaï aux huiles chaudes (1h)",
                "description": "Étirements doux, pressions ciblées et rééquilibrage énergétique complet.",
                "prix": "70€",
                "duree": "1 heure",
                "image": "https://images.unsplash.com/photo-1600180758890-6ee37f9d8f29"
            }

    # Soins minceur / drainage
    if quiz["objectif"] in ["Éliminer les toxines / affiner", "Raffermir & tonifier"] or "Rétention" in quiz["preoccupation"]:
        if "Bas du visage" in quiz["zone"]:
            return {
                "titre": "Radiofréquence menton (30 min)",
                "description": "Raffermit et redéfinit le bas du visage pour un profil plus net.",
                "prix": "30€",
                "duree": "30 minutes",
                "image": "https://images.unsplash.com/photo-1585238342028-4b6c45a04a9f"
            }
        elif quiz["effet"] == "Résultat durable (minceur, raffermissement, anti-âge)":
            return {
                "titre": "Combo drainage + sauna infrarouge (1h30)",
                "description": "Triple action : élimine les toxines, stimule la sudation et affine la silhouette.",
                "prix": "150€",
                "duree": "1h30",
                "image": "https://images.unsplash.com/photo-1606820276166-e8e4158a8c85"
            }
        else:
            return {
                "titre": "Drainage lymphatique Signature (1h)",
                "description": "Drainage manuel complet pour activer la circulation et détoxifier le corps.",
                "prix": "110€",
                "duree": "1 heure",
                "image": "https://images.unsplash.com/photo-1599058917212-d750089bc07e"
            }

    # Soins visage
    if quiz["zone"] == "Visage":
        if "Teint" in quiz["preoccupation"]:
            return {
                "titre": "Soin coup d’éclat express (30 min)",
                "description": "Nettoyage et masque éclat pour un effet immédiat avant un évènement.",
                "prix": "50€",
                "duree": "30 minutes",
                "image": "https://images.unsplash.com/photo-1611217752492-1a8db26f7f31"
            }
        elif "Rides" in quiz["preoccupation"] or "Corriger rides" in quiz["objectif"]:
            return {
                "titre": "Soin anti-rides au rétinol (1h)",
                "description": "Lisse les ridules et stimule le renouvellement cellulaire pour une peau plus jeune.",
                "prix": "120€",
                "duree": "1 heure",
                "image": "https://images.unsplash.com/photo-1612817159949-2343f9c00d93"
            }
        elif "Tâches" in quiz["preoccupation"]:
            return {
                "titre": "Peeling mandélique anti-tâche (1h)",
                "description": "Corrige les taches pigmentaires et unifie le teint, même pour les peaux sensibles.",
                "prix": "120€",
                "duree": "1 heure",
                "image": "https://images.unsplash.com/photo-1600431521340-491eca880813"
            }
        else:
            return {
                "titre": "Soin purifiant anti-imperfection (1h)",
                "description": "Nettoyage en profondeur, désincrustation et masque purifiant.",
                "prix": "50€",
                "duree": "1 heure",
                "image": "https://images.unsplash.com/photo-1600180759123-62e03a7344a3"
            }

    # Par défaut
    return {
        "titre": "Massage détente personnalisé",
        "description": "Un soin sur mesure selon vos besoins pour une expérience de relaxation complète.",
        "prix": "60€",
        "duree": "45 minutes",
        "image": "https://images.unsplash.com/photo-1589987607627-616cac5bfb07"
    }
def recommend_from_quiz(answers: dict):
    recos = []
    objectif = answers.get("objectif", "").lower()

    if "hydrat" in objectif:
        recos += ["Soin hydratant profond (1h)", "Massage aux huiles végétales"]
    if "anti" in objectif:
        recos += ["Soin anti-âge au collagène", "Massage facial raffermissant"]
    if "éclat" in objectif:
        recos += ["Soin coup d’éclat express", "Gommage éclat du visage"]
    if "minceur" in objectif:
        recos += ["Massage minceur drainant", "Soin tonifiant du corps"]
    if "apais" in objectif:
        recos += ["Massage relaxant aux pierres chaudes", "Rituel détente aromatique"]
    if "répar" in objectif:
        recos += ["Soin nourrissant réparateur", "Enveloppement au karité"]

    if not recos:
        recos = ["Soin découverte personnalisé", "Massage bien-être 30 min"]

    return recos   