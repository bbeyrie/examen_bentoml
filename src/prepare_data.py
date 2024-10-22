import pandas as pd
from sklearn.model_selection import train_test_split
import os

# Charger les données
data = pd.read_csv('data/raw/admission.csv')

# Nettoyer les données (supprimer les colonnes inutiles, si besoin)
# Par exemple, si vous jugez que 'Research' n'est pas pertinent
# data = data.drop(columns=['Research'])

# Remove the "Serial No." column (it's unnecessary for model training)
data = data.drop(columns=["Serial No."])

# Séparer les features et la cible
X = data.drop(columns=['Chance of Admit'])
y = data['Chance of Admit']

# Diviser les données en jeu d'entraînement et jeu de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Sauvegarder les données préparées
os.makedirs('data/processed', exist_ok=True)
X_train.to_csv('data/processed/X_train.csv', index=False)
X_test.to_csv('data/processed/X_test.csv', index=False)
y_train.to_csv('data/processed/y_train.csv', index=False)
y_test.to_csv('data/processed/y_test.csv', index=False)