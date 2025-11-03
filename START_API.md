# 🚀 Démarrage Rapide de l'API

## ✅ Installation terminée !

Votre API Flask est prête à être utilisée.

## 📝 Étapes pour démarrer

### 1. Lancer l'API

```bash
cd flask_app
python app.py
```

Vous verrez:
```
╔══════════════════════════════════════════════════════════╗
║  🚀 Invoice Extraction API - Flask                      ║
╠══════════════════════════════════════════════════════════╣
║  📍 URL: http://localhost:5000                          ║
║  🏥 Health: http://localhost:5000/health                ║
║  📄 Extract: POST http://localhost:5000/api/invoice/extract ║
╚══════════════════════════════════════════════════════════╝
```

### 2. Tester l'API (dans un autre terminal)

**Test simple:**
```bash
python test_api.py facture.jpg
```

**Ou avec cURL:**
```bash
curl -X POST http://localhost:5000/api/invoice/extract -F "file=@facture.jpg"
```

## 📍 Endpoints disponibles

### Health Check
```bash
GET http://localhost:5000/health
```

### Extraction de facture
```bash
POST http://localhost:5000/api/invoice/extract
Content-Type: multipart/form-data
Body: file=<votre_facture>
```

## 📖 Documentation complète

Consultez `API_GUIDE.md` pour:
- Exemples d'intégration Spring Boot
- Tests détaillés
- Gestion des erreurs
- Configuration avancée

## 🎯 Prochaines étapes

1. ✅ L'API est prête
2. ✅ Testez avec votre facture
3. ✅ Intégrez dans Spring Boot (voir API_GUIDE.md)

Bonne utilisation ! 🎉
