from random import sample

import bleach
from cyber_risk_perception.auth import upload_file
from cyber_risk_perception.json2graph import json2graph
from cyber_risk_perception.utils import GLOBAL_RISKS, INTRODUCTION, MAX_SELECTION, NUM_SELECTION_RANDOM, TITLE
from cyber_risk_perception.style import custom_css
import streamlit as st
import json
import os
from datetime import datetime
import logging


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

    # Initialisation des clés session_state avant la boucle
    for risk in selected_risks:
        if f"other_{risk}" not in st.session_state:
            st.session_state[f"other_{risk}"] = False
        if f"consequences_{risk}" not in st.session_state:
            st.session_state[f"consequences_{risk}"] = []

    # Interface pour chaque risque principal
    all_filled = True
    for risk in selected_risks:
        with st.expander(f"Identified Risk : {risk}", expanded=False):

            new_consequences = st.multiselect(
                f"What risks could be triggered by:{risk} ?",
                options=[r for r in GLOBAL_RISKS if r != risk],
                key=f"choices_{risk}",
                max_selections=MAX_SELECTION
            )

            if "Other" in new_consequences:
                st.session_state[f"other_{risk}"] = True

                raw_risk: str = st.text_input("Please could you specify", key=f"other_for_{risk}")
                cleaned_risk: str = bleach.clean(raw_risk.strip(), tags=[], attributes={}, protocols=[], strip=True)
                
                if raw_risk:
                    # Remplacer "Other" par la valeur nettoyée
                    new_consequences = [c if c != "Other" else cleaned_risk for c in new_consequences]
                else:
                    all_filled = False  # Bloque la soumission si "Other" non rempli 
            
            st.session_state[f"consequences_{risk}"] = new_consequences

            # Vérifiez si le formulaire est rempli
            if not new_consequences:
                all_filled = False

    profession = st.text_input("Please indicate your profession *", key="profession")
    raw_comments = st.text_area("Are there any comments you'd like to mention?")
    comments = bleach.clean(raw_comments.strip(), tags=[], attributes={}, protocols=[], strip=True)


    st.subheader("Overview of data collected")

    if 'submitted' not in st.session_state:
        st.session_state.submitted = False

    # Vérifiez si tous les formulaires sont remplis avant d'afficher le bouton "Soumettre"
    if all_filled and profession and not st.session_state.submitted:
        if st.button("Submit/view data"):

            st.session_state.data = [
                {"risk": risk, "consequences": st.session_state[f"consequences_{risk}"], "other": st.session_state[f"other_{risk}"]}
                for risk in selected_risks
            ]

            output = {
            "profession": profession,
            "responses": st.session_state.data,
            "comments": comments.strip()
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
            
            st.session_state.submitted = True

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

    # Afficher un message après soumission
    if st.session_state.submitted:
        st.success("Form Submitted !")
        st.stop()  # Arrête l'exécution du script

    if not (all_filled and profession and not st.session_state.submitted):
        # Si certains champs sont vides, afficher un bouton "Compléter les formulaires"
        if st.button("In Progress"):
            st.warning("Please complete all forms before submitting.")



# Fonction pour sauvegarder les données dans un fichier JSON
def save_data_to_json_file(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)

# Lancer l'application Streamlit
if __name__ == "__main__":
    main()
