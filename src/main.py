import os.path
import joblib
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

# --- TWARDE FILTRY (SNAJPER) ---
# Słowa, które zawsze chronią maila przed usunięciem (małe litery!)
WHITELIST = ['faktura', 'rachunek', 'marszalek', 'zamówienie', 'ważne', 'rekrutacja']

# Słowa, które z automatu skazują maila na śmierć (małe litery!)
BLACKLIST = ['newsletter','oferta', 'promocja', 'wypisz się']


def main():
    print("Ładuję Mózg AI... 🧠")
    try:
        model = joblib.load('ai_model.pkl')
    except FileNotFoundError:
        print("Błąd: Nie znaleziono pliku ai_model.pkl! Zrób najpierw trening.")
        return

    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    print("Pobieram 30 najnowszych wiadomości do analizy...\n")
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=30).execute()
    messages = results.get('messages', [])

    if not messages:
        print("Skrzynka pusta!")
        return

    do_usuniecia = []

    print("--- 🎯 WYNIKI ANALIZY (SNAJPER + AI) ---")
    for msg in messages:
        try:
            details = service.users().messages().get(userId='me', id=msg['id']).execute()
            headers = details['payload']['headers']
            
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "Brak tematu")
            sender = next((h['value'] for h in headers if h['name'] == 'From'), "Brak nadawcy")
            
            # Zmieniamy wszystko na małe litery, żeby łatwiej było szukać słów kluczowych
            sender_lower = sender.lower()
            subject_lower = subject.lower()
            tekst_do_oceny = sender + " " + subject

            # 1. TEST SNAJPERA: Czy mail jest na białej liście?
            if any(slowo in sender_lower or slowo in subject_lower for slowo in WHITELIST):
                print(f"🟢 SNAJPER (Zostawiono) -> {subject[:50]}...")
                continue # Przechodzimy od razu do następnego maila

            # 2. TEST SNAJPERA: Czy mail jest na czarnej liście?
            elif any(slowo in sender_lower or slowo in subject_lower for slowo in BLACKLIST):
                print(f"🔴 SNAJPER (Kosz)       -> {subject[:50]}...")
                do_usuniecia.append(msg['id'])
                continue

            # 3. TEST AI: Jeśli Snajper nie podjął decyzji, wkracza AI
            else:
                werdykt = model.predict([tekst_do_oceny])[0]
                if werdykt == 0:
                    print(f"🟡 AI (Kosz)            -> {subject[:50]}...")
                    do_usuniecia.append(msg['id'])
                else:
                    print(f"🔵 AI (Zostawiono)      -> {subject[:50]}...")

        except Exception:
            pass

    if not do_usuniecia:
        print("\nWszystko jest czyste! Nie ma co usuwać. 😎")
        return

    print(f"\nZnaleziono {len(do_usuniecia)} śmieci.")
    potwierdzenie = input("CZY NA PEWNO CHCESZ WYRZUCIĆ JE DO KOSZA? (wpisz 'tak' i wciśnij Enter): ")

    if potwierdzenie.lower() == 'tak':
        print("Zaczynam czyszczenie...")
        for msg_id in do_usuniecia:
            service.users().messages().trash(userId='me', id=msg_id).execute()
        print("Gotowe! Śmieci wylądowały w koszu. 🗑️")
    else:
        print("Akcja anulowana. Żaden mail nie ucierpiał. 🛡️")

if __name__ == '__main__':
    main()