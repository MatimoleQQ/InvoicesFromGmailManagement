import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Email użytkownika
EMAIL = "eauperfau@gmail.com"

# Pliki z klientem Google
CLIENT_SECRET_FILE = os.path.join(os.path.dirname(__file__), "clientSecretFile",'client_secret.json')
TOKEN_PICKLE = os.path.join(os.path.dirname(__file__), 'token.pkl')

# Zakres wymagany do IMAP XOAUTH2
SCOPES = ['https://mail.google.com/']

creds = None

# Sprawdzenie czy istnieje zapisany token
if os.path.exists(TOKEN_PICKLE):
    with open(TOKEN_PICKLE, 'rb') as token:
        creds = pickle.load(token)

# Odświeżenie tokenu jeśli wygasł
if creds and creds.expired and creds.refresh_token:
    creds.refresh(Request())

# Jeśli brak tokenu lub nie jest ważny – logowanie przez przeglądarkę
if not creds or not creds.valid:
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    creds = flow.run_local_server(port=0)
    # Zapisanie tokenu
    with open(TOKEN_PICKLE, 'wb') as token:
        pickle.dump(creds, token)

print("Token wygenerowany i zapisany w 'token.pkl'")
