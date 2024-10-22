import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error, r2_score
import bentoml

# Charger les données préparées
X_train = pd.read_csv('data/processed/X_train.csv')
X_test = pd.read_csv('data/processed/X_test.csv')
y_train = pd.read_csv('data/processed/y_train.csv')
y_test = pd.read_csv('data/processed/y_test.csv')

# Créer et entraîner le modèle
model = LinearRegression()
model.fit(X_train, y_train)

# Évaluer les performances
y_pred = model.predict(X_test)
rmse = root_mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'RMSE: {rmse}')
print(f'R2: {r2}')

# Sauvegarder le modèle dans le Model Store de BentoML
bento_model = bentoml.sklearn.save_model("admissions_model", model)