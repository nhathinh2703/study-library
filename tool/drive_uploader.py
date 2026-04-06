from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os, pickle

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def get_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # luôn lấy đường dẫn tuyệt đối tới credentials.json
            cred_path = os.path.join(os.path.dirname(__file__), "credentials.json")
            flow = InstalledAppFlow.from_client_secrets_file(cred_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('drive', 'v3', credentials=creds)

def upload_file(file_path, folder_id=None):
    service = get_service()
    file_metadata = {'name': os.path.basename(file_path)}
    if folder_id:
        file_metadata['parents'] = [folder_id]
    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    file_id = file.get('id')
    # tạo link chia sẻ
    service.permissions().create(fileId=file_id, body={'role': 'reader', 'type': 'anyone'}).execute()
    return f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"

def create_folder(name, parent_id=None):
    service = get_service()
    folder_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    if parent_id:
        folder_metadata['parents'] = [parent_id]
    folder = service.files().create(body=folder_metadata, fields='id').execute()
    return folder.get('id')

def update_file(file_id, file_path, mime_type="application/pdf"):
    service = get_service()
    media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)
    updated = service.files().update(
        fileId=file_id,
        media_body=media
    ).execute()
    # giữ nguyên quyền chia sẻ
    service.permissions().create(fileId=file_id, body={'role': 'reader', 'type': 'anyone'}).execute()
    return f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"

def delete_file(file_id):
    service = get_service()
    service.files().delete(fileId=file_id).execute()
    return True