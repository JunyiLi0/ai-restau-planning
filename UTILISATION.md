# Guide d'Utilisation - AI Restaurant Planning

## Démarrage Rapide

### 1. Lancer le Backend

```bash
cd backend

# Créer l'environnement virtuel (première fois uniquement)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou: venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Configurer la clé API OpenAI
cp .env.example .env
# Éditer .env et ajouter votre clé: OPENAI_API_KEY=sk-...

# Lancer le serveur
uvicorn app.main:app --reload
```

Le serveur sera disponible sur `http://localhost:8000`

### 2. Lancer le Frontend

```bash
cd frontend

# Installer les dépendances (première fois uniquement)
npm install

# Lancer l'application
npm run dev
```

L'application sera disponible sur `http://localhost:5173`

---

## Fonctionnalités

### Créer un Planning via le Chat

Dans l'interface de chat, vous pouvez demander à l'IA de créer un planning :

**Exemples de commandes :**

```
Crée un planning pour la semaine 5 avec les employés suivants :
- Jean Dupont : lundi au vendredi midi (11:30-14:30)
- Marie Martin : mardi au samedi soir (18:30-22:30)
- Pierre Bernard : weekend complet
```

```
Ajoute Sophie Laurent qui travaille mercredi et jeudi, midi et soir
```

```
Modifie les horaires de Jean pour qu'il travaille aussi le samedi soir
```

### Importer un Planning Existant

1. Cliquez sur l'onglet **"Upload File"**
2. Glissez-déposez votre fichier ou cliquez pour parcourir
3. Formats acceptés : **PDF** ou **Excel (.xlsx)**

Pour les fichiers Excel, le format attendu est :
- Colonne A : Nom de l'employé
- Pour chaque jour : Horaires Midi | Repas | Horaires Soir | Repas
- Format horaires : `11:30 - 14:30`

### Modifier un Planning avec l'IA

Une fois un planning chargé, vous pouvez le modifier via le chat :

```
Ajoute 1 heure au service du soir de Marie le vendredi
```

```
Supprime le service de Pierre le dimanche midi
```

```
Change les horaires du soir de Jean le mardi à 19:00 - 23:00
```

### Exporter le Planning

Cliquez sur les boutons en haut du planning :
- **Export PDF** : Génère un PDF formaté pour impression
- **Export Excel** : Télécharge le fichier Excel modifiable

---

## Structure du Planning

| Colonne | Description |
|---------|-------------|
| Employé | Nom de l'employé |
| Midi | Horaires du service midi (ex: 11:30 - 14:30) |
| Repas | Nombre de repas pour le service midi |
| Soir | Horaires du service soir (ex: 18:30 - 22:30) |
| Repas | Nombre de repas pour le service soir |
| Total Heures | Total des heures travaillées dans la semaine |
| Total Repas | Total des repas pris dans la semaine |

---

## API (pour développeurs)

### Endpoints principaux

| Méthode | URL | Description |
|---------|-----|-------------|
| `POST` | `/api/upload/pdf` | Importer un PDF |
| `POST` | `/api/upload/excel` | Importer un Excel |
| `GET` | `/api/planning/current` | Obtenir le planning actuel |
| `POST` | `/api/planning/generate` | Générer un nouveau planning |
| `PUT` | `/api/planning/ai-update` | Modifier avec l'IA |
| `POST` | `/api/chat/message` | Envoyer un message au chat |
| `GET` | `/api/export/pdf` | Télécharger en PDF |
| `GET` | `/api/export/excel` | Télécharger en Excel |

### Exemple d'utilisation de l'API

```bash
# Générer un planning
curl -X POST http://localhost:8000/api/planning/generate \
  -H "Content-Type: application/json" \
  -d '{"instructions": "Crée un planning avec Jean et Marie pour la semaine 5"}'

# Modifier un planning existant
curl -X PUT http://localhost:8000/api/planning/ai-update \
  -H "Content-Type: application/json" \
  -d '{"instructions": "Ajoute Sophie le lundi midi"}'

# Télécharger le PDF
curl -O http://localhost:8000/api/export/pdf
```

---

## Dépannage

### Le serveur ne démarre pas

- Vérifiez que Python 3.11+ est installé : `python3 --version`
- Vérifiez que l'environnement virtuel est activé
- Vérifiez que toutes les dépendances sont installées

### Erreur "OPENAI_API_KEY"

- Créez le fichier `.env` dans le dossier `backend/`
- Ajoutez votre clé : `OPENAI_API_KEY=sk-votre-clé-ici`

### Le frontend ne se connecte pas au backend

- Vérifiez que le backend est lancé sur le port 8000
- Vérifiez la configuration proxy dans `frontend/vite.config.ts`

---

## Fichier d'exemple

Un fichier Excel d'exemple est disponible dans :
```
backend/data/templates/sample_planning.xlsx
```

Vous pouvez l'utiliser comme modèle pour créer vos propres plannings.
