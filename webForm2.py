from random import sample
from json2graph import json2graph
import streamlit as st
import json
import os
from datetime import datetime
from utils import GLOBAL_RISKS


NUM_SELECTION_RANDOM = 10
MAX_SELECTION = 5
FILE_OUT_PATH= "C:/Users/jbertholat/Desktop/Formulaire/responses"

os.makedirs(FILE_OUT_PATH, exist_ok=True)


custom_css = """
    <style>
    div.stButton > button:first-child {
        background-color: #4CAF50; /* Vert */
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 8px;
    }
    div.stButton > button:first-child:hover {
        background-color: #45a049; /* Vert foncé au survol */
    }
    </style>
    """

# Fonction principale de l'application Streamlit
def main():
    st.title("Cartographie des Conséquences des Risques Globaux")
    st.markdown(
        """
        Cette application vous permet de sélectionner les interconnexions entre différents risques globaux.
        Pour chaque risque principal, choisissez jusqu'à 5 autres risques qui pourraient être déclenchés.
        """
    )
    
    st.markdown(custom_css, unsafe_allow_html=True)

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
            save_data_to_json_file(st.session_state.data, file_path)
            st.success("Les données ont été sauvegardées\n Merci pour votre participation.")
    
    # Affichage des données collectées
        if st.session_state.data:
            #st.json(st.session_state.data)
            
            #
            try:
                fig = json2graph(file_path)
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
        json.dump(data, f, indent=4, ensure_ascii=False)

# Lancer l'application Streamlit
if __name__ == "__main__":
    main()
