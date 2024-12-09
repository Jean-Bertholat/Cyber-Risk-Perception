import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

import streamlit as st


SERVICE_ACCOUNT_FILE = '.streamlit/streamlitapp-444213-5531be505843.json'
SCOPES = ['https://www.googleapis.com/auth/drive.file']


# Authentifier avec le compte de service
def authenticate():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('drive', 'v3', credentials=creds)

# Télécharger un fichier sur Google Drive
def upload_file(file_path):
    service = authenticate()
    file_metadata = {'name': os.path.basename(file_path)}
    media = MediaFileUpload(file_path, resumable=True)
    
    # Télécharger le fichier
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    st.success(f'Fichier téléchargé avec succès: {file["id"]}')
    return file["id"]