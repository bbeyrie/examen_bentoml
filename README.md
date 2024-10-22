# Examen BentoML

Ce repertoire contient l'architecture basique afin de rendre l'évaluation pour l'examen BentoML.

Vous êtes libres d'ajouter d'autres dossiers ou fichiers si vous jugez utile de le faire.

Voici comment est construit le dossier de rendu de l'examen:

```bash       
├── examen_bentoml          
│   ├── data       
│   │   ├── processed      
│   │   ├── raw
│   │   └── sample_data.json  
│   ├── models      
│   ├── src       
│   ├── README.md
│   └── bentofile.yaml
```


## Prérequis
- **Python 3.8 ou supérieur**
- **Docker installé sur votre machine**
- **BentoML installé**

## Étapes du Projet

### 1. Préparation de l'Environnement de Travail

```bash  
git clone https://github.com/votre_utilisateur/examen_bentoml.git
cd examen_bentoml
```

```bash  
python -m venv env
source env/bin/activate  # Sur Windows: env\Scripts\activate
```

```bash  
pip install -r requirements.txt
```


### 2. Exécution des scripts

```python  
python src/prepare_data.py
python src/train_model.py
```

Vérifiez que le modèle a bien été sauvegardé :
```bash
bentoml models list
```

### 3. Mise en place de l'API de Prédiction

Exemple de commande pour démarrer le service :
```bash
bentoml serve src.service:svc --reload
```

Testez l'API avec `curl` ou Postman en envoyant des requêtes POST contenant les données d'un étudiant.

```bash
curl -X POST http://0.0.0.0:3000/predict -H "Content-Type: application/json" -d '{
    "GRE_Score": 320,
    "TOEFL_Score": 110,
    "University_Rating": 4,
    "SOP": 4.5,
    "LOR": 4.5,
    "CGPA": 8.5,
    "Research": 1
}'
```

### 4. Création d'un Bento & Conteneurisation avec Docker

Créez un fichier `bentofile.yaml` à la racine du projet.

Ensuite, construisez le Bento :
```bash
bentoml build
```

Créez une image Docker à partir de votre Bento :
```bash
bentoml containerize admissions_prediction_service:latest
```

Testez l'image Docker en lançant un conteneur :
```bash
docker run -p 3000:3000 admissions_prediction_service:latest
```



