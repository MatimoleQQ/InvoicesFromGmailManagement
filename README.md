Gmail Invoice Downloader

Automatyczny skrypt w Pythonie do pobierania załączników PDF (faktur) z Gmaila i organizowania ich w folderach według nadawcy. Projekt wykorzystuje OAuth 2.0 do bezpiecznej autoryzacji bez użycia hasła wprost.

Funkcjonalności

  Pobiera wszystkie wiadomości z Gmaila w skrzynce INBOX.
  
  Filtruje już pobrane wiadomości, aby nie duplikować plików.
  
  Tworzy foldery dla każdego nadawcy i zapisuje załączniki PDF.
  
  Loguje pobrane faktury w CSV (logs/invoice_log.csv) oraz UID-y w logs/processed_uids.txt.
  
  Wykorzystuje OAuth 2.0 i tokeny, aby bezpiecznie logować się do Gmail.

Wymagania

  Python 3.12+
  
  Pakiety Python:

  pip install google-auth google-auth-oauthlib pyzmail36

Konfiguracja

  Utwórz projekt w Google Cloud Console
  .

  Skonfiguruj OAuth 2.0 Client ID dla aplikacji typu "Desktop".
  
  Pobierz plik JSON z poświadczeniami i nazwij go:
  
  clientSecretFile/client_secret.json


WAŻNE: Nie wrzucaj tego pliku do repozytorium! Zamiast tego możesz przechowywać client_secret.example.json z pustymi wartościami i dodać do .gitignore.

Skopiuj swoje konto Gmail do zmiennej EMAIL w pliku main.py.

Po pierwszym uruchomieniu skrypt poprosi o autoryzację w przeglądarce. Token zostanie zapisany w token.pkl.

Struktura projektu
Invoice/
│
├── main.py                 # Główny skrypt
├── gmail_oauth.py          # Skrypt obsługujący OAuth (jeśli osobno)
├── clientSecretFile/
│   └── client_secret.json  # Plik z OAuth 2.0 (NIE wrzucać do repo!)
├── invoices/               # Folder docelowy na pobrane PDF-y
├── logs/
│   ├── processed_uids.txt  # UID-y przetworzonych maili
│   └── invoice_log.csv     # Log pobranych faktur
├── requirements.txt        # Lista zależności
└── README.md

Uruchomienie
  python main.py


Skrypt automatycznie pobierze wszystkie nowe maile z PDF-ami i zapisze je w invoices/.

  Zaktualizuje logi w CSV i UID-y w processed_uids.txt.

Bezpieczeństwo

  Nigdy nie wrzucaj client_secret.json ani token.pkl do repo.

Dodaj do .gitignore:

  clientSecretFile/
  token.pkl


W repo możesz przechowywać plik client_secret.example.json jako przykład konfiguracji.

Dalszy rozwój:

  Możliwość pobierania tylko maili od wybranych nadawców.
  
  Obsługa innych typów załączników (np. XML, CSV).
  
  Integracja z bazą danych do zaawansowanego raportowania faktur.
