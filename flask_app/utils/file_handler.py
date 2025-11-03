"""
Utilitaires pour la gestion des fichiers
"""
import os


def valider_fichier(file, allowed_extensions):
    """
    Valide un fichier uploadé
    
    Args:
        file: Fichier Flask
        allowed_extensions: Set des extensions autorisées
        
    Returns:
        dict: Résultat de la validation
    """
    # Vérifier l'extension
    if '.' not in file.filename:
        return {
            'valid': False,
            'error': 'Extension manquante',
            'message': 'Le fichier doit avoir une extension'
        }
    
    extension = file.filename.rsplit('.', 1)[1].lower()
    
    if extension not in allowed_extensions:
        return {
            'valid': False,
            'error': 'Extension non autorisée',
            'message': f'Extensions autorisées: {", ".join(allowed_extensions)}'
        }
    
    return {
        'valid': True,
        'extension': extension
    }


def nettoyer_fichiers_temporaires(filepath):
    """
    Supprime un fichier temporaire
    
    Args:
        filepath: Chemin du fichier à supprimer
    """
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
    except Exception as e:
        print(f"Erreur lors de la suppression du fichier {filepath}: {e}")
