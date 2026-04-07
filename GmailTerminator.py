import os
import sys
import threading
import joblib
import customtkinter as ctk
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class GmailApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gmail AI Terminator 🤖")
        self.geometry("700x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.do_usuniecia = []
        self.service = None
        self.WHITELIST = ['faktura', 'rachunek', 'marszalek', 'zamówienie', 'ważne', 'rekrutacja']
        self.BLACKLIST = ['newsletter', 'no-reply', 'noreply', 'oferta', 'promocja', 'wypisz się']

        self.label = ctk.CTkLabel(self, text="GMAIL AI TERMINATOR", font=("Impact", 32))
        self.label.pack(pady=20)

        self.status_label = ctk.CTkLabel(self, text="Status: Gotowy", text_color="gray")
        self.status_label.pack()

        self.scan_button = ctk.CTkButton(self, text="SKANUJ SKRZYNKĘ (50)", command=self.start_scan_thread)
        self.scan_button.pack(pady=15)

        self.result_box = ctk.CTkTextbox(self, width=640, height=350, font=("Courier New", 12))
        self.result_box.pack(pady=10)

        self.clean_button = ctk.CTkButton(self, text="DO KOSZA (0)", fg_color="red", state="disabled", command=self.delete_emails)
        self.clean_button.pack(pady=10)

    def log(self, message):
        self.result_box.insert("end", message + "\n")
        self.result_box.see("end")

    def start_scan_thread(self):
        self.scan_button.configure(state="disabled")
        self.clean_button.configure(state="disabled")
        threading.Thread(target=self.scan_emails, daemon=True).start()

    def scan_emails(self):
        self.do_usuniecia = []
        self.result_box.delete("1.0", "end")
        
        try:
            self.log("🧠 Ładowanie modelu AI...")
            model_path = resource_path('data/ai_model.pkl')
            model = joblib.load(model_path)
            
            self.log("🔑 Autoryzacja Google...")
            SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
            creds = None
            
            token_path = os.path.join(os.path.expanduser('~'), '.gmail_token.json')
            
            if os.path.exists(token_path):
                creds = Credentials.from_authorized_user_file(token_path, SCOPES)
            
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    creds_path = resource_path('config/credentials.json')
                    flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
                    creds = flow.run_local_server(port=0)
                
                with open(token_path, 'w') as token:
                    token.write(creds.to_json())

            self.service = build('gmail', 'v1', credentials=creds)
            
            self.log("📥 Pobieranie maili...")
            results = self.service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=50).execute()
            messages = results.get('messages', [])

            for msg in messages:
                details = self.service.users().messages().get(userId='me', id=msg['id']).execute()
                headers = details['payload']['headers']
                subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "Brak tematu")
                sender = next((h['value'] for h in headers if h['name'] == 'From'), "Brak nadawcy")
                
                s_lower, sub_lower = sender.lower(), subject.lower()
                tekst = f"{sender} {subject}"

                if any(w in s_lower or w in sub_lower for w in self.WHITELIST):
                    self.log(f"🟢 [SNAJPER] {subject[:45]}...")
                elif any(b in s_lower or b in sub_lower for b in self.BLACKLIST):
                    self.log(f"🔴 [SNAJPER] {subject[:45]}...")
                    self.do_usuniecia.append(msg['id'])
                else:
                    werdykt = model.predict([tekst])[0]
                    if werdykt == 0: 
                        self.log(f"🟡 [AI-KOSZ] {subject[:45]}...")
                        self.do_usuniecia.append(msg['id'])
                    else:
                        self.log(f"🔵 [AI-OK]   {subject[:45]}...")

            self.clean_button.configure(state="normal", text=f"WYWAL DO KOSZA ({len(self.do_usuniecia)})")
            self.status_label.configure(text="Status: Gotowe", text_color="green")
            
        except Exception as e:
            self.log(f"❌ BŁĄD: {str(e)}")
        
        self.scan_button.configure(state="normal")

    def delete_emails(self):
        if not self.do_usuniecia: return
        self.log(f"\n🗑️ Usuwanie {len(self.do_usuniecia)} wiadomości...")
        for msg_id in self.do_usuniecia:
            try:
                self.service.users().messages().trash(userId='me', id=msg_id).execute()
            except: pass
        self.log("✨ Gotowe! Skrzynka wyczyszczona.")
        self.clean_button.configure(state="disabled", text="DO KOSZA (0)")

if __name__ == "__main__":
    app = GmailApp()
    app.mainloop()