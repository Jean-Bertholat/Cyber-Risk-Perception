from random import sample
from auth import upload_file
from json2graph import json2graph
from utils import GLOBAL_RISKS, INTRODUCTION
from style import custom_css
import streamlit as st
import json
import os
from datetime import datetime

NUM_SELECTION_RANDOM = 2
MAX_SELECTION = 5
FILE_OUT_PATH= os.getcwd() + "\\responses"
os.makedirs(FILE_OUT_PATH, exist_ok=True)

# Fonction principale de l'application Streamlit
def main():
    st.title("Cartographie des Conséquences des Risques Globaux")
    st.markdown(custom_css, unsafe_allow_html=True)
    st.write(INTRODUCTION)
    st.subheader("Cartographie des risques:")
    
    # Stockage des données dans la session
    if "data" not in st.session_state:
        st.session_state.data = []

    # Stocker la sélection aléatoire une seule fois
    if "selected_risks" not in st.session_state:
        st.session_state.selected_risks = sample(GLOBAL_RISKS, k=NUM_SELECTION_RANDOM)

    # Récupérer les risques sélectionnés
    selected_risks = st.session_state.selected_risks

    # Interface pour chaque risque principal
    all_filled = True
    for risk in selected_risks:
        with st.expander(f"Risque identifié : {risk}", expanded=False):
            #st.write()
            consequences = st.session_state.get(f"consequences_{risk}", [])
            new_consequences = st.multiselect(
                f"Quels autres risques pourraient être déclenchés par : {risk} ?",
                options=[r for r in GLOBAL_RISKS if r != risk],
                key=f"choices_{risk}",
                max_selections=MAX_SELECTION
            )
            st.session_state[f"consequences_{risk}"] = new_consequences

            # Vérifiez si le formulaire est rempli
            if not new_consequences:
                all_filled = False

    st.subheader("Aperçu des données collectées")
    
    # Vérifiez si tous les formulaires sont remplis avant d'afficher le bouton "Soumettre"
    if all_filled:
        if st.button("Soumettre/visualiser les données"):
            # Collecter tous les choix
            st.session_state.data = [
                {"risk": risk, "consequences": st.session_state[f"choices_{risk}"]}
                for risk in selected_risks
            ]
            filename = f"risk_mapping_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            file_path = os.path.join(FILE_OUT_PATH, filename)
            data = json.dumps(st.session_state.data, indent=4, ensure_ascii=False)
            try:
                save_data_to_json_file(data, file_path)         # Sauvegarder temporairement le fichier sur le serveur
                st.success("Les données ont été sauvegardées sur le container")
            except:
                st.error(f"Une erreur est survenue lors de l'enregistrement sur le container : {e}")

            try:
                id = upload_file(file_path) # Télécharger sur Google Drive
                st.success(f'Les données ont été sauvegardées avec succès - \
                           Merci pour votre participation.')
            except:
                st.error(f"Une erreur est survenue lors du téléchargement sur Google Drive : {e}")
    
    # Affichage des données collectées
        if st.session_state.data:
            #st.json(st.session_state.data)
            
            #
            try:
                fig = json2graph(data)
                # Ajouter des interactions

                # Générer le code HTML
                html_code = fig.generate_html()

                # Afficher le graphe dans Streamlit
                st.components.v1.html(html_code, width=750, height=500)
            
            except:
                st.markdown("error graph visualisation")
                st.json(st.session_state.data)

            
    else:
        # Si certains champs sont vides, afficher un bouton "Compléter les formulaires"
        if st.button("Soumettre les données"):
            st.warning("Veuillez compléter tous les formulaires avant de soumettre.")


# Fonction pour sauvegarder les données dans un fichier JSON
def save_data_to_json_file(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)

# Lancer l'application Streamlit
if __name__ == "__main__":
    main()
