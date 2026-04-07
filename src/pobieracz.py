import os.path
import csv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
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

    print("Łączę się z Gmailem... Pobieram 200 ostatnich wiadomości.")
    
    results = service.users().messages().list(userId='me', maxResults=200).execute()
    messages = results.get('messages', [])

    if not messages:
        print("Pusto! Nie znaleziono żadnych maili.")
        return

    with open('maile_do_treningu.csv', mode='w', encoding='utf-8-sig', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        
        writer.writerow(['Oceń: 1=Spam, 0=Zostaw', 'Nadawca', 'Temat'])
        
        print("Trwa wyciąganie szczegółów i zapisywanie do pliku (to może potrwać kilka sekund)...")
        
        for msg in messages:
            try:
                details = service.users().messages().get(userId='me', id=msg['id']).execute()
                headers = details['payload']['headers']
                
                subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "Brak tematu")
                sender = next((h['value'] for h in headers if h['name'] == 'From'), "Nieznany nadawca")
                
                writer.writerow(['', sender, subject])
            except Exception:
                pass

    print("\nGotowe! Plik 'maile_do_treningu.csv' wygenerowany. 😎")

if __name__ == '__main__':
    main()