"""
Service d'extraction de factures avec Gemini AI
"""
import os
import json
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
from pathlib import Path

# Charger les variables d'environnement
load_dotenv()

# Configuration Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY non trouvée dans le fichier .env")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# Prompt pour l'extraction
PROMPT = """
You are a specialist in comprehending receipts.
Input images in the form of receipts will be provided to you,
and your task is to respond to questions based on the content of the input image.

Extract ALL information from this receipt/invoice and return it in JSON format.

Return ONLY a valid JSON object with this exact structure:
{
  "numero_facture": "string ou null",
  "date_facture": "YYYY-MM-DD ou null",
  "date_echeance": "YYYY-MM-DD ou null",
  "fournisseur": {
    "nom": "string ou null",
    "adresse": "string ou null",
    "siret": "string ou null",
    "email": "string ou null",
    "telephone": "string ou null"
  },
  "client": {
    "nom": "string ou null",
    "adresse": "string ou null",
    "siret": "string ou null"
  },
  "lignes": [
    {
      "description": "string",
      "quantite": number,
      "prix_unitaire": number,
      "total": number,
      "tva": number ou null
    }
  ],
  "montant_ht": number ou null,
  "montant_tva": number ou null,
  "montant_ttc": number ou null,
  "devise": "string ou null",
  "conditions_paiement": "string ou null",
  "notes": "string ou null"
}

Important:
- Use null for missing information
- Convert dates to YYYY-MM-DD format
- Use numbers (not strings) for numeric values
- Return ONLY the JSON, no additional text
"""


def extraire_facture(chemin_fichier):
    """
    Extrait les données d'une facture (image ou PDF)
    
    Args:
        chemin_fichier: Chemin vers le fichier de la facture
        
    Returns:
        dict: Données extraites en JSON
        
    Raises:
        Exception: Si l'extraction échoue
    """
    try:
        # Déterminer le type de fichier
        extension = Path(chemin_fichier).suffix.lower()
        
        # Envoyer à Gemini selon le type de fichier
        if extension == '.pdf':
            # Pour les PDF, uploader directement le fichier
            uploaded_file = genai.upload_file(chemin_fichier)
            response = model.generate_content([PROMPT, uploaded_file])
        else:
            # Pour les images, utiliser PIL
            image = Image.open(chemin_fichier)
            response = model.generate_content([PROMPT, image])
        
        # Extraire le JSON de la réponse
        texte = response.text.strip()
        
        # Nettoyer la réponse (enlever les blocs markdown si présents)
        if "```json" in texte:
            texte = texte.split("```json")[1].split("```")[0]
        elif "```" in texte:
            texte = texte.split("```")[1].split("```")[0]
        
        # Parser le JSON
        donnees = json.loads(texte.strip())
        
        return donnees
        
    except json.JSONDecodeError as e:
        raise Exception(f"Erreur de parsing JSON: {str(e)}")
    except Exception as e:
        raise Exception(f"Erreur lors de l'extraction: {str(e)}")
