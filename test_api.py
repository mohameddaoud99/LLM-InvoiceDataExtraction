"""
Script de test pour l'API Flask
"""
import requests
import sys
import os


def test_health():
    """Test du endpoint health"""
    print("🏥 Test Health Check...")
    try:
        response = requests.get('http://localhost:5000/health')
        if response.status_code == 200:
            print("✅ Health check OK")
            print(f"   Réponse: {response.json()}")
            return True
        else:
            print(f"❌ Health check échoué: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        print("   Assurez-vous que l'API est démarrée (python flask_app/app.py)")
        return False


def test_extract_invoice(filepath):
    """Test du endpoint d'extraction"""
    print(f"\n📄 Test Extraction de facture: {filepath}")
    
    if not os.path.exists(filepath):
        print(f"❌ Fichier non trouvé: {filepath}")
        return False
    
    try:
        url = 'http://localhost:5000/api/invoice/extract'
        files = {'file': open(filepath, 'rb')}
        
        print("   Envoi de la requête...")
        response = requests.post(url, files=files)
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print("✅ Extraction réussie!")
                print(f"\n📊 Données extraites:")
                print(f"   - Numéro: {data['data'].get('numero_facture')}")
                print(f"   - Date: {data['data'].get('date_facture')}")
                print(f"   - Montant TTC: {data['data'].get('montant_ttc')} {data['data'].get('devise')}")
                print(f"   - Fournisseur: {data['data'].get('fournisseur', {}).get('nom')}")
                print(f"   - Client: {data['data'].get('client', {}).get('nom')}")
                print(f"   - Nombre de lignes: {len(data['data'].get('lignes', []))}")
                return True
            else:
                print(f"❌ Extraction échouée: {data.get('message')}")
                return False
        else:
            print(f"❌ Erreur HTTP {response.status_code}")
            print(f"   Réponse: {response.json()}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def main():
    """Fonction principale"""
    print("="*60)
    print("🧪 Tests de l'API Flask - Invoice Extraction")
    print("="*60)
    
    # Test 1: Health check
    if not test_health():
        print("\n⚠️  L'API n'est pas accessible. Arrêt des tests.")
        sys.exit(1)
    
    # Test 2: Extraction
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        test_extract_invoice(filepath)
    else:
        print("\n⚠️  Aucun fichier spécifié pour le test d'extraction")
        print("   Usage: python test_api.py <chemin_facture>")
        print("   Exemple: python test_api.py facture.jpg")
    
    print("\n" + "="*60)
    print("✅ Tests terminés")
    print("="*60)


if __name__ == "__main__":
    main()
