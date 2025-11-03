"""
API Flask simple pour l'extraction de données de factures
"""
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

from services.gemini_service import extraire_facture
from utils.file_handler import valider_fichier, nettoyer_fichiers_temporaires

# Charger les variables d'environnement
load_dotenv()

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

# Créer le dossier uploads s'il n'existe pas
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialiser Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Activer CORS pour permettre les requêtes depuis Spring Boot
CORS(app)


@app.route('/health', methods=['GET'])
def health():
    """Endpoint de santé pour vérifier que l'API fonctionne"""
    return jsonify({
        'status': 'ok',
        'service': 'Invoice Extraction API',
        'version': '1.0.0'
    }), 200


@app.route('/api/invoice/extract', methods=['POST'])
def extract_invoice():
    """
    Endpoint principal pour extraire les données d'une facture
    
    Request:
        - file: Fichier de facture (multipart/form-data)
        
    Response:
        - success: boolean
        - data: Données extraites de la facture
        - message: Message de succès ou d'erreur
    """
    try:
        # Vérifier qu'un fichier a été envoyé
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'Aucun fichier fourni',
                'message': 'Veuillez envoyer un fichier avec la clé "file"'
            }), 400
        
        file = request.files['file']
        
        # Vérifier que le fichier a un nom
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'Nom de fichier vide',
                'message': 'Le fichier doit avoir un nom'
            }), 400
        
        # Valider le fichier
        validation_result = valider_fichier(file, ALLOWED_EXTENSIONS)
        if not validation_result['valid']:
            return jsonify({
                'success': False,
                'error': validation_result['error'],
                'message': validation_result['message']
            }), 400
        
        # Sauvegarder le fichier temporairement
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Extraire les données avec Gemini
            donnees = extraire_facture(filepath)
            
            # Nettoyer le fichier temporaire
            nettoyer_fichiers_temporaires(filepath)
            
            return jsonify({
                'success': True,
                'data': donnees,
                'message': 'Facture extraite avec succès'
            }), 200
            
        except Exception as e:
            # Nettoyer le fichier en cas d'erreur
            nettoyer_fichiers_temporaires(filepath)
            raise e
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Erreur lors de l\'extraction de la facture'
        }), 500


@app.errorhandler(413)
def file_too_large(e):
    """Gérer les fichiers trop volumineux"""
    return jsonify({
        'success': False,
        'error': 'Fichier trop volumineux',
        'message': f'La taille maximale autorisée est {MAX_FILE_SIZE // (1024*1024)} MB'
    }), 413


@app.errorhandler(404)
def not_found(e):
    """Gérer les routes non trouvées"""
    return jsonify({
        'success': False,
        'error': 'Route non trouvée',
        'message': 'L\'endpoint demandé n\'existe pas'
    }), 404


@app.errorhandler(500)
def internal_error(e):
    """Gérer les erreurs internes"""
    return jsonify({
        'success': False,
        'error': 'Erreur interne du serveur',
        'message': str(e)
    }), 500


if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"""
    ╔══════════════════════════════════════════════════════════╗
    ║  🚀 Invoice Extraction API - Flask                      ║
    ╠══════════════════════════════════════════════════════════╣
    ║  📍 URL: http://localhost:{port}                          ║
    ║  🏥 Health: http://localhost:{port}/health                ║
    ║  📄 Extract: POST http://localhost:{port}/api/invoice/extract ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    app.run(host='0.0.0.0', port=port, debug=debug)
