# 🤖 Gmail AI Terminator

A smart assistant for cleaning up your inbox. The application connects to your Gmail account, scans messages, and uses Artificial Intelligence (Machine Learning) to evaluate whether a given email is spam or something important. 

No more manual clicking through hundreds of newsletters and junk mail! 🧹✉️

## ✨ Key Features
* **Google API Integration:** Secure login to your Gmail account using the OAuth 2.0 standard.
* **AI Brain:** Uses a trained `scikit-learn` model to analyze message content.
* **Simple Interface:** Modern and eye-pleasing GUI created with `customtkinter`.
* **Local Execution:** Privacy first – the model runs locally on your computer.
* **Standalone Version:** Ability to build a ready-to-use application (e.g., for macOS) that runs without opening the terminal.

## 🛠️ Technologies
* Python 3.x
* CustomTkinter (GUI)
* Scikit-Learn / Joblib (Machine Learning)
* Google Client Library (Gmail API)
* PyInstaller (App building)

## 📁 Project Structure
We care about clean code! The directory structure looks like this:

```text
Gmail_Cleaner/
├── config/             # Holds API keys and tokens (ignored by Git!)
├── data/               # Holds the trained AI model (ai_model.pkl)
├── src/                # Source code (if you split the project into smaller files)
├── GmailTerminator.py  # Main executable file
└── README.md           # This file
```
🚀 How to use it?

Option 1: From source code (for developers)

Clone this repository.

Make sure you have the required libraries installed:

Bash
pip install customtkinter scikit-learn google-auth-oauthlib google-api-python-client joblib
Drop your credentials.json file (downloaded from Google Cloud Console) into the config/ folder.

Run the main script:

Bash
python GmailTerminator.py
Option 2: Ready-to-use Application (macOS)

Using PyInstaller, the project can be built into a single .app file. The final package lands in the dist/ folder and can be launched with a single mouse click.

⚠️ Important Security Information
Files like credentials.json (your Google key) and token.json should NEVER be pushed to a public repository. The project has a properly configured .gitignore file that ensures this data stays only on your local machine.

Created to reclaim time lost on reading spam. 🍹
