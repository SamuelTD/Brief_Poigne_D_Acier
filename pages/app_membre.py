import streamlit as st
from generales_fonctions import afficher_navbar, sqmodel_to_dataframe
from models import Membres, Cours, Cartes_Acces, Inscriptions, Coachs
from init_db import engine
from sqlmodel import select, or_, col, Session
import utils as u
import pandas as pd


afficher_navbar()
st.session_state.admin_state = 1

if "list_inscriptions_actuel" not in st.session_state:
    st.session_state.list_inscriptions_actuel = u.obtenir_inscription(st.session_state.id_membre_actuel)
if "list_inscriptions_actuel" not in st.session_state:
    st.session_state.list_inscriptions_actuel = u.obtenir_inscription(st.session_state.id_membre_actuel)

def Accueil_membre():
    st.subheader("Nutrition & Mode de vie")
    st.image("nutrition.jpg")

def Consulter_cours():

    st.title ("Les cours disponibles")

    st.session_state.list_cours = u.obtenir_list_cours()
    data = sqmodel_to_dataframe(st.session_state.list_cours)
    st.dataframe(data=data)


def inscription_cours():

    st.title("Je veux m'inscrire")
    colms = st.columns((1, 2, 2, 1))
    fields = ['Coach', 'HORAIRE', 'Discipline.', 'Inscription']
    for col, field_name in zip(colms, fields):
        # header
        col.write(field_name)

    for cours in st.session_state.list_cours:
        
        inscrit= False
        for inscription in st.session_state.list_inscriptions_actuel:
            if inscription.cours_id == cours.id:
                inscrit = True
                break
        if not inscrit :
            col1, col2, col3, col4 = st.columns((1, 2, 2, 1))
            try:
                col1.write(u.obtenir_coach_par_id(cours.coach_id).nom)
            except:
                col1.write(":red[NULL]")
            col2.write(cours.horaire)
            col3.write(cours.nom)   
            
            # button_phold = col4.empty()
            # do_action = button_phold.button("❌", key=cours.id)
            # if do_action:
            #     u.annuler_mon_inscription(cours.id, st.session_state.id_membre_actuel)
            #     st.session_state.list_inscriptions_actuel = u.obtenir_inscription(st.session_state.id_membre_actuel)
            #     st.rerun()
      
            button_phold = col4.empty()
            do_action = button_phold.button("✅", key=cours.id)
            if do_action:
                u.inscription_membre(st.session_state.id_membre_actuel, cours.id)
                st.session_state.list_inscriptions_actuel = u.obtenir_inscription(st.session_state.id_membre_actuel)
                st.rerun()        


        #do_action = button_phold.button("✅", key=cours.id)
        
        #if do_action:
            #u.inscription_membre(st.session_state.id_membre_actuel,cours.id)
            #st.session_state.list_cours = u.obtenir_list_cours()
            #st.rerun()

def annuler_inscription():

    st.title("Je souhaite annuler un cours")
    st.session_state.list_inscriptions_actuel = u.obtenir_inscription(st.session_state.id_membre_actuel)

    colms = st.columns((2, 1, 2, 2))
    fields = ['Horaire', 'Spécialité','Coach', 'inscription']
        
    for col, field_name in zip(colms, fields):
        col.write(field_name)


    for inscription in st.session_state.list_inscriptions_actuel:
        try:
            cours = u.obtenir_cours(inscription.cours_id)
        except:
            continue
        coach = u.obtenir_coach_par_id(cours.coach_id)
        col1, col2, col3, col4 = st.columns((2,1,2, 2))
 
        col1.write(cours.horaire)  
        col2.write(cours.nom)
        try:
            col3.write(coach.nom)
        except:
            col3.write(":red-background[NULL]")

        button_phold = col4.empty()
        do_action = button_phold.button("❌", key=inscription.id)

        if do_action:
            u.annuler_mon_inscription(inscription.cours_id, st.session_state.id_membre_actuel)
            st.session_state.list_inscriptions_actuel = u.obtenir_inscription(st.session_state.id_membre_actuel)
            st.rerun()




def Historique():

    st.title("Accès à mon historique")
    st.session_state.historique = u.obtenir_historique(st.session_state.id_membre_actuel)
    
    fields = ['Spécialité', 'Horaire', 'Coach']
    colms = st.columns((2, 2, 2))

    for col, field_name in zip(colms, fields):
        col.write(field_name)
    
    
    for ligne in st.session_state.historique:
        col1, col2, col3 = st.columns((2, 2, 2,))
        
        try:
            nom_coach = (u.obtenir_coach_par_id(ligne.coach_id).nom)
        except:
            nom_coach = ":red[NULL]"
        col1.write(ligne.nom) 
        col2.write(ligne.horaire)  
        col3.write(nom_coach)




#Menu mon compte 
 
st.title("Poigne d'Acier 🏋️‍♀️")
st.sidebar.title("Mon compte")


choix =st.sidebar.radio(f"Que veux-tu faire, {st.session_state.nom_membre_actuel} ?", ["Accueil","Consulter les cours disponibles","S'inscrire à un cours", "Annuler une inscription", "Mon historique"])

if choix == "Consulter les cours disponibles" :
    Consulter_cours() 
    


elif choix == "S'inscrire à un cours" :
    inscription_cours()


elif choix == "Annuler une inscription":
    annuler_inscription()

elif choix == "Mon historique" : 
    Historique()

else:
    choix == "Accueil"
    Accueil_membre()

