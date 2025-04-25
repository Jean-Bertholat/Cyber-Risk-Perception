import os
import tempfile
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Définition des scopes nécessaires
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def authenticate():
    """
    Authentifie l'utilisateur auprès de l'API Google Drive en utilisant 
    les credentials définis dans st.secrets (chargés depuis .streamlit/secrets.toml).
    """
    # Récupération des credentials depuis st.secrets
    creds_data = st.secrets["google_service_account"]

    # Construction d'un dictionnaire conforme aux attentes de la méthode from_service_account_info
    creds_dict = {
        "type": creds_data["type"],
        "project_id": creds_data["project_id"],
        "private_key_id": creds_data["private_key_id"],
        "private_key": creds_data["private_key"],
        "client_email": creds_data["client_email"],
        "client_id": creds_data["client_id"],
        "auth_uri": creds_data["auth_uri"],
        "token_uri": creds_data["token_uri"],
        "auth_provider_x509_cert_url": creds_data["auth_provider_x509_cert_url"],
        "client_x509_cert_url": creds_data["client_x509_cert_url"],
    }

    # Création des credentials et construction du service
    creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)
    return service

def upload_file(file_path):
    """
    Upload un fichier sur Google Drive dans le dossier spécifié.
    """
    # ID du dossier dans lequel le fichier sera uploadé (à adapter selon vos besoins)
    parentfolderid = "1R47H8nVvU18iVmcBCLjLl8eakeg3CJqJ"
    service = authenticate()
    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [parentfolderid]
    }
    media = MediaFileUpload(file_path, resumable=True)
    
    try:
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        return file["id"]
    except Exception as e:
        print(f"Erreur lors du téléchargement du fichier : {e}")
        return None

def test_authenticate():
    """
    Teste l'authentification auprès de l'API Google Drive.
    """
    print("Test de l'authentification en cours...")
    service = authenticate()
    if service:
        print("Authentification réussie !")
    else:
        print("Authentification échouée !")

def test_upload_file():
    """
    Teste l'upload d'un fichier en créant un fichier temporaire, en le téléchargeant,
    puis en affichant l'ID retourné par Google Drive.
    """
    print("Test de l'upload de fichier en cours...")
    # Création d'un fichier temporaire
    with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as tmp:
        tmp.write("Contenu de test pour l'upload sur Google Drive.")
        tmp_path = tmp.name

    print(f"Tentative d'upload du fichier temporaire : {tmp_path}")
    file_id = upload_file(tmp_path)
    
    if file_id:
        print(f"Fichier uploadé avec succès ! ID retourné : {file_id}")
    else:
        print("Échec de l'upload du fichier.")

    # Suppression du fichier temporaire local
    os.remove(tmp_path)

if __name__ == '__main__':
    # Pour que st.secrets soit chargé, exécutez ce script via Streamlit :
    #     streamlit run integration_test.py
    print("========== TEST D'AUTHENTIFICATION ==========")
    test_authenticate()
    print("\n========== TEST D'UPLOAD DE FICHIER ==========")
    test_upload_file()
