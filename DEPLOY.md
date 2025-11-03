# 🚀 Guide de Déploiement sur Render

## Backend Flask (API)

### Commandes Render

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
gunicorn --bind 0.0.0.0:$PORT flask_app.app:app
```

### Variables d'Environnement à Configurer

Dans le Dashboard Render, ajoutez ces variables :

| Variable | Valeur | Description |
|----------|--------|-------------|
| `GOOGLE_API_KEY` | `votre_clé_api` | Clé API Google Gemini |
| `FLASK_DEBUG` | `False` | Mode debug (False en production) |

### Étapes de Déploiement

1. **Créer un nouveau Web Service sur Render**
   - Connectez votre repository GitHub
   - Sélectionnez la branche `main`
   - Root Directory: `/` (racine du projet)

2. **Configuration**
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn --bind 0.0.0.0:$PORT flask_app.app:app`

3. **Variables d'Environnement**
   - Ajoutez `GOOGLE_API_KEY` avec votre clé API
   - Ajoutez `FLASK_DEBUG` = `False`

4. **Déployer**
   - Cliquez sur "Create Web Service"
   - Attendez le déploiement (2-3 minutes)
   - Notez l'URL de votre API (ex: `https://invoice-extraction-api.onrender.com`)

## Frontend Angular (Static Site)

### Option 1 : Déployer sur Render Static Site

**Build Command:**
```bash
cd frontend/invoice-extraction && npm install && npm run build
```

**Publish Directory:**
```
frontend/invoice-extraction/dist/invoice-extraction/browser
```

### Option 2 : Déployer sur Netlify/Vercel

Plus simple pour les applications Angular.

### Configuration Frontend

Avant de déployer, mettez à jour l'URL de l'API dans :
`frontend/invoice-extraction/src/environments/environment.prod.ts`

```typescript
export const environment = {
  production: true,
  apiUrl: 'https://VOTRE-BACKEND.onrender.com/api/invoice'
};
```

Remplacez `VOTRE-BACKEND` par l'URL de votre backend Render.

## 🔧 Vérification Post-Déploiement

### Tester l'API

```bash
# Health check
curl https://VOTRE-BACKEND.onrender.com/health

# Test extraction (avec un fichier)
curl -X POST https://VOTRE-BACKEND.onrender.com/api/invoice/extract \
  -F "file=@facture.pdf"
```

### Endpoints Disponibles

- `GET /health` - Vérification de l'état
- `POST /api/invoice/extract` - Extraction de facture

## 📝 Notes Importantes

1. **Render Free Tier** : Le service s'endort après 15 minutes d'inactivité
2. **Premier démarrage** : Peut prendre 30-60 secondes
3. **CORS** : Déjà configuré dans l'application Flask
4. **Taille fichiers** : Maximum 10 MB

## 🐛 Dépannage

### L'API ne répond pas
- Vérifiez les logs dans Render Dashboard
- Assurez-vous que `GOOGLE_API_KEY` est configurée
- Vérifiez que gunicorn est bien installé

### Erreur CORS
- Vérifiez que l'URL du frontend est autorisée
- Le CORS est configuré pour accepter toutes les origines en développement

### Erreur 500
- Vérifiez les logs Render
- Assurez-vous que toutes les dépendances sont installées
- Vérifiez la clé API Google Gemini
