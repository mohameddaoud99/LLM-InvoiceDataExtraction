"""
Script simple pour extraire les données d'une facture avec Gemini AI
"""
import os
import sys
import json

# Ajouter le dossier parent au path pour importer les modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask_app.services.gemini_service import extraire_facture as extraire_facture_service


def extraire_facture(chemin_fichier):
    """
    Extrait les données d'une facture (image ou PDF)
    
    Args:
        chemin_fichier: Chemin vers le fichier de la facture
        
    Returns:
        dict: Données extraites en JSON
    """
    print(f"📄 Traitement de: {chemin_fichier}")
    print("🤖 Envoi à Gemini AI...")
    
    # Utiliser le service centralisé
    donnees = extraire_facture_service(chemin_fichier)
    
    print("✅ Extraction réussie!")
    return donnees


def sauvegarder_json(donnees, fichier_sortie="facture_extraite.json"):
    """Sauvegarde les données dans un fichier JSON"""
    with open(fichier_sortie, 'w', encoding='utf-8') as f:
        json.dump(donnees, f, ensure_ascii=False, indent=2)
    print(f"💾 Données sauvegardées dans: {fichier_sortie}")


def afficher_resultat(donnees):
    """Affiche les données extraites de manière lisible"""
    print("\n" + "="*60)
    print("📊 DONNÉES EXTRAITES")
    print("="*60)
    print(json.dumps(donnees, ensure_ascii=False, indent=2))
    print("="*60 + "\n")


if __name__ == "__main__":
    import sys
    
    # Vérifier les arguments
    if len(sys.argv) < 2:
        print("Usage: python extract_invoice.py <chemin_facture>")
        print("Exemple: python extract_invoice.py facture.png")
        print("Formats supportés: images (PNG, JPG, JPEG, etc.) et PDF")
        sys.exit(1)
    
    chemin_facture = sys.argv[1]
    
    # Vérifier que le fichier existe
    if not os.path.exists(chemin_facture):
        print(f"❌ Erreur: Le fichier '{chemin_facture}' n'existe pas")
        sys.exit(1)
    
    try:
        # Extraire les données
        donnees = extraire_facture(chemin_facture)
        
        # Afficher le résultat
        afficher_resultat(donnees)
        
        # Sauvegarder dans un fichier JSON
        sauvegarder_json(donnees)
        
    except Exception as e:
        print(f"❌ Erreur lors de l'extraction: {e}")
        sys.exit(1)
