"""
Gmail Invoice Downloader
------------------------
Automatyczne pobieranie faktur PDF z Gmaila przy użyciu OAuth2 (XOAUTH2),
zapisywanie ich w folderach klientów oraz logowanie do CSV.

Autor: Marcin
Technologie: Python, Gmail IMAP, OAuth2, pyzmail
"""

# ===============================
# Imports
# ===============================
import imaplib
import os
import pickle
import csv
import pyzmail
from google.auth.transport.requests import Request


# ===============================
# Configuration
# ===============================
EMAIL = "<YOUR EMAIL>"
TOKEN_PICKLE = "token.pkl"

BASE_DIR = os.path.dirname(__file__)
INVOICES_DIR = os.path.join(BASE_DIR, "invoices")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

PROCESSED_UIDS_FILE = os.path.join(LOGS_DIR, "processed_uids.txt")
CSV_LOG_FILE = os.path.join(LOGS_DIR, "invoice_log.csv")


# ===============================
# Environment preparation
# ===============================
os.makedirs(INVOICES_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)


# ===============================
# Load OAuth credentials
# ===============================
with open(TOKEN_PICKLE, "rb") as token_file:
    creds = pickle.load(token_file)

# Refresh token if expired
if creds.expired and creds.refresh_token:
    creds.refresh(Request())


# ===============================
# IMAP XOAUTH2 authentication
# ===============================
auth_string = (
    f"user={EMAIL}\1auth=Bearer {creds.token}\1\1"
).encode("utf-8")

imap = imaplib.IMAP4_SSL("imap.gmail.com")
imap.authenticate("XOAUTH2", lambda _: auth_string)
imap.select("INBOX")


# ===============================
# Fetch mail UIDs
# ===============================
status, response = imap.search(None, "ALL")
all_uids = response[0].split()

print(f"Total emails in inbox: {len(all_uids)}")


# ===============================
# Load already processed UIDs
# ===============================
if os.path.exists(PROCESSED_UIDS_FILE):
    with open(PROCESSED_UIDS_FILE, "r") as file:
        processed_uids = set(file.read().splitlines())
else:
    processed_uids = set()

new_uids = [uid for uid in all_uids if uid.decode() not in processed_uids]
print(f"New emails to process: {len(new_uids)}")


# ===============================
# Prepare CSV log
# ===============================
if not os.path.exists(CSV_LOG_FILE):
    with open(CSV_LOG_FILE, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["UID", "Sender", "Subject", "Filename"])


# ===============================
# Process emails
# ===============================
for uid in new_uids:
    uid_str = uid.decode()

    status, data = imap.fetch(uid_str, "(RFC822)")
    raw_email = data[0][1]

    message = pyzmail.PyzMessage.factory(raw_email)

    subject = message.get_subject()
    sender_email = message.get_addresses("from")[0][1]

    # Create client-specific directory
    client_dir = os.path.join(INVOICES_DIR, sender_email)
    os.makedirs(client_dir, exist_ok=True)

    # Extract PDF attachments
    for part in message.mailparts:
        if part.filename and part.filename.lower().endswith(".pdf"):
            file_path = os.path.join(client_dir, part.filename)

            with open(file_path, "wb") as file:
                file.write(part.get_payload())

            # Log invoice
            with open(CSV_LOG_FILE, "a", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([uid_str, sender_email, subject, part.filename])

            print(f"Saved invoice: {part.filename} from {sender_email}")

    # Mark UID as processed
    with open(PROCESSED_UIDS_FILE, "a") as file:
        file.write(uid_str + "\n")


# ===============================
# Cleanup
# ===============================
imap.logout()
print("Invoice processing completed successfully.")
