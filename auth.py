import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

import streamlit as st

#SERVICE_ACCOUNT_FILE = '.streamlit/secrets.toml'
SCOPES = ['https://www.googleapis.com/auth/drive.file']


# Authentifier avec le compte de service
def authenticate():
    
    creds_data = st.secrets["google_service_account"]

    # Convert the TOML data back to JSON
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

    # Authenticate using the JSON-like dictionary
    creds = service_account.Credentials.from_service_account_info(
        creds_dict, scopes=SCOPES)
    return build('drive', 'v3', credentials=creds)

# Télécharger un fichier sur Google Drive
# def upload_file(file_path):
#     service = authenticate()
#     file_metadata = {'name': os.path.basename(file_path)}
#     media = MediaFileUpload(file_path, resumable=True)
    
#     # Télécharger le fichier
#     file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()        
#     return file["id"]

def upload_file(file_path):
    parentfolderid = "1R47H8nVvU18iVmcBCLjLl8eakeg3CJqJ"
    service = authenticate()
    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [parentfolderid]  # Ajoute le dossier partagé comme parent
    }
    media = MediaFileUpload(file_path, resumable=True)
    
    try:
        file = service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink').execute()
        #st.success(f"Fichier téléchargé avec succès !")
        st.write(f"[Voir le fichier sur Google Drive](https://drive.google.com/file/d/{file['id']}/view)")
        return file["id"]
    except Exception as e:
        st.error(f"Erreur lors du téléchargement du fichier : {e}")
        return None