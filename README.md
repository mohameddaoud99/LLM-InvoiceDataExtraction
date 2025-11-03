# Extracteur de Factures avec Gemini AI

Script Python simple pour extraire automatiquement les données d'une facture (image ou PDF) en utilisant Google Gemini AI.

## 📋 Prérequis

- Python 3.8 ou supérieur
- Une clé API Google Gemini ([Obtenir une clé](https://makersuite.google.com/app/apikey))

## 🚀 Installation

1. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

2. **Configurer la clé API**

Éditer le fichier `.env` et ajouter votre clé API:
```
GEMINI_API_KEY=votre_cle_api_ici
```

## 💻 Utilisation

### Méthode simple

```bash
python extract_invoice.py facture.png
```

ou

```bash
python extract_invoice.py facture.pdf
```

### Utilisation dans votre code

```python
from extract_invoice import extraire_facture

# Extraire les données
donnees = extraire_facture("ma_facture.png")

# Utiliser les données
print(f"Numéro: {donnees['numero_facture']}")
print(f"Montant TTC: {donnees['montant_ttc']} {donnees['devise']}")
```

## 📤 Format de sortie

Le script génère un fichier `facture_extraite.json` avec cette structure:

```json
{
  "numero_facture": "INV-2024-001",
  "date_facture": "2024-01-15",
  "date_echeance": "2024-02-15",
  "fournisseur": {
    "nom": "Entreprise ABC",
    "adresse": "123 Rue Example, 75001 Paris",
    "siret": "12345678900012",
    "email": "contact@abc.fr",
    "telephone": "01 23 45 67 89"
  },
  "client": {
    "nom": "Client XYZ",
    "adresse": "456 Avenue Client, 69001 Lyon",
    "siret": "98765432100098"
  },
  "lignes": [
    {
      "description": "Produit A",
      "quantite": 2,
      "prix_unitaire": 100.0,
      "total": 200.0,
      "tva": 20.0
    }
  ],
  "montant_ht": 200.0,
  "montant_tva": 40.0,
  "montant_ttc": 240.0,
  "devise": "EUR",
  "conditions_paiement": "30 jours",
  "notes": "Merci pour votre confiance"
}
```

## 📝 Formats supportés

- **Images**: PNG, JPG, JPEG
- **PDF**: Fichiers PDF (première page)

## 🔧 Personnalisation

Pour modifier les champs extraits, éditez la variable `PROMPT` dans `extract_invoice.py`.

## ⚠️ Notes

- Le script utilise le modèle `gemini-1.5-flash` (rapide et économique)
- Pour des factures complexes, vous pouvez utiliser `gemini-1.5-pro`
- Les champs manquants sont retournés comme `null`

## 🐛 Dépannage

**Erreur "GEMINI_API_KEY non trouvée"**
- Vérifiez que le fichier `.env` existe et contient votre clé API

**Erreur lors du parsing JSON**
- Le modèle peut parfois retourner du texte supplémentaire
- Le script nettoie automatiquement les blocs markdown

**Fichier non trouvé**
- Vérifiez le chemin du fichier
- Utilisez des chemins absolus si nécessaire

## 📄 Licence

MIT
