🤖 Gmail AI Terminator
Inteligentny asystent do sprzątania skrzynki pocztowej. Aplikacja łączy się z Twoim kontem Gmail, skanuje wiadomości i przy pomocy sztucznej inteligencji (Machine Learning) ocenia, czy dany mail to śmieć, czy coś ważnego.

Koniec z ręcznym przeklikiwaniem setek newsletterów i spamu! 🧹✉️

✨ Główne funkcje
Integracja z Google API: Bezpieczne logowanie do konta Gmail przy użyciu standardu OAuth 2.0.

Mózg AI: Wykorzystanie wytrenowanego modelu scikit-learn do analizy treści wiadomości.

Prosty interfejs: Nowoczesne i przyjemne dla oka GUI stworzone w customtkinter.

Lokalne działanie: Prywatność przede wszystkim – model działa lokalnie na Twoim komputerze.

Wersja Standalone: Możliwość zbudowania gotowej aplikacji (np. na macOS), która działa bez odpalania terminala.

🛠️ Technologie
Python 3.x

CustomTkinter (GUI)

Scikit-Learn / Joblib (Machine Learning)

Google Client Library (Gmail API)

PyInstaller (Budowanie aplikacji)

📁 Struktura projektu
Dbamy o porządek w kodzie! Struktura katalogów wygląda następująco:

Plaintext
Gmail_Cleaner/
├── config/             # Tutaj trzymane są klucze API i tokeny (ignorowane przez Git!)
├── data/               # Tutaj znajduje się wytrenowany model AI (ai_model.pkl)
├── src/                # Kod źródłowy (jeśli rozbijasz projekt na mniejsze pliki)
├── GmailTerminator.py  # Główny plik uruchomieniowy
└── README.md           # Ten plik
🚀 Jak tego używać?
Opcja 1: Z poziomu kodu (dla deweloperów)

Sklonuj to repozytorium.

Upewnij się, że masz zainstalowane wymagane biblioteki:
pip install customtkinter scikit-learn google-auth-oauthlib google-api-python-client joblib

Wrzuć swój plik credentials.json (pobrany z Google Cloud Console) do folderu config/.

Odpal główny plik:
python GmailTerminator.py

Opcja 2: Gotowa Aplikacja (macOS)

Używając PyInstallera, projekt można zbudować do pojedynczego pliku .app. Gotowa paczka ląduje w folderze dist/ i można ją odpalać jednym kliknięciem myszy.

⚠️ Ważne informacje o bezpieczeństwie
Pliki takie jak credentials.json (Twój klucz do Google) oraz token.json NIGDY nie powinny znaleźć się w publicznym repozytorium. Projekt ma odpowiednio skonfigurowany plik .gitignore, który dba o to, by te dane pozostały tylko na Twoim komputerze.

Stworzone po to, by odzyskać czas stracony na czytanie spamu. 🍹
