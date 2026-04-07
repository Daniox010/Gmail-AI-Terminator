import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib

def main():
    print("1. Wczytuję dane z pliku CSV...")
    df = pd.read_csv('maile_do_treningu.csv', sep=';')

    df = df.dropna(subset=['Oceń: 1=Spam, 0=Zostaw'])

    print(f"Znaleziono {len(df)} ocenionych maili. Przygotowuję materiał...")

    df['Tekst'] = df['Nadawca'] + " " + df['Temat']

    X = df['Tekst']
    y = df['Oceń: 1=Spam, 0=Zostaw'].astype(int)

    print("2. Rozpoczynam trening AI (Algorytm Naive Bayes)...")
    
    model = Pipeline([
        ('vectorizer', CountVectorizer()),
        ('classifier', MultinomialNB())
    ])

    model.fit(X, y)

    print("3. Zapisuję wytrenowany mózg na dysk...")
    joblib.dump(model, 'ai_model.pkl')

    print("\nGotowe! 🧠 Twój Mózg (ai_model.pkl) jest stworzony i gotowy do akcji.")

if __name__ == '__main__':
    main()