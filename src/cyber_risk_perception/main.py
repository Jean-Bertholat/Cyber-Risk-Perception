from random import sample

import bleach
from cyber_risk_perception.auth import upload_file
from cyber_risk_perception.json2graph import json2graph
from cyber_risk_perception.utils import GLOBAL_RISKS, INTRODUCTION, TITLE
from cyber_risk_perception.style import custom_css
import streamlit as st
import json
import os
from datetime import datetime
import logging


NUM_SELECTION_RANDOM = 6
MAX_SELECTION = 5
FILE_OUT_PATH= os.getcwd() + "\\responses"
os.makedirs(FILE_OUT_PATH, exist_ok=True)

# Configurer le logger
logging.basicConfig(
    filename='app.log',  # Enregistrer les logs dans un fichier
    level=logging.INFO,  # Niveau de log
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Fonction principale de l'application Streamlit
def main():
    st.title(TITLE)
    st.markdown(custom_css, unsafe_allow_html=True)
    st.write(INTRODUCTION)
    st.subheader("Risks Cartography:")
    
    # Stockage des données dans la session
    if "data" not in st.session_state:
        st.session_state.data = []

    # Stocker la sélection aléatoire une seule fois
    filtered_risks = [risk for risk in GLOBAL_RISKS if risk not in ["Other", "None"]]

    if "selected_risks" not in st.session_state:
        st.session_state.selected_risks = sample(filtered_risks, k=NUM_SELECTION_RANDOM)
    
    selected_risks = st.session_state.selected_risks

    # Interface pour chaque risque principal
    all_filled = True
    for risk in selected_risks:
        with st.expander(f"Identified Risk : {risk}", expanded=False):
            consequences = st.session_state.get(f"consequences_{risk}", [])
            new_consequences = st.multiselect(
                f"What other risks could be triggered by:{risk} ?",
                options=[r for r in GLOBAL_RISKS if r != risk],
                key=f"choices_{risk}",
                max_selections=MAX_SELECTION
            )
            st.session_state[f"consequences_{risk}"] = new_consequences

            # Vérifiez si le formulaire est rempli
            if not new_consequences:
                all_filled = False

    st.subheader("Overview of data collected")

    profession = st.text_input("Please indicate your profession *", key="profession")
    raw_other_risks = st.text_area("Are there any other risks you'd like to mention?")
    other_risks = bleach.clean(raw_other_risks.strip(), tags=[], attributes={}, protocols=[], strip=True)


    # Vérifiez si tous les formulaires sont remplis avant d'afficher le bouton "Soumettre"
    if all_filled:
        if st.button("Submit/view data"):
            # Collecter tous les choix
            if not profession.strip():
                st.error("Please fill in the 'Profession' field to submit your data.")
                return

            st.session_state.data = [
                {"risk": risk, "consequences": st.session_state[f"choices_{risk}"]}
                for risk in selected_risks
            ]

            output = {
            "profession": profession,
            "responses": st.session_state.data,
            "other_risks": other_risks.strip()
            }

            filename = f"risk_mapping_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            file_path = os.path.join(FILE_OUT_PATH, filename)
            data = json.dumps(output, indent=4, ensure_ascii=False)
            try:
                save_data_to_json_file(data, file_path)         # Sauvegarder temporairement le fichier sur le serveur
                logging.info("The data has been saved on the container")
            except Exception as e:
                logging.error(f"An error has occurred during registration on the container : {e}")

            try:
                id = upload_file(file_path) # Télécharger sur Google Drive
                st.success(f'Data successfully saved - \
                           Thank you for your participation.')
            except Exception as e:
                st.error(f"An error occurred while saving the results: {e}")
                logging.error(f"An error occurred while uploading to Google Drive : {e}")


    
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
        if st.button("Submit data"):
            st.warning("Please complete all forms before submitting.")


# Fonction pour sauvegarder les données dans un fichier JSON
def save_data_to_json_file(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)

# Lancer l'application Streamlit
if __name__ == "__main__":
    main()
