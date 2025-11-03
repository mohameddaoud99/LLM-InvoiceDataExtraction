# 📘 Guide d'Utilisation de l'API Flask

## 🚀 Démarrage Rapide

### 1. Installation des dépendances

```bash
pip install -r requirements.txt
```

### 2. Configuration

Assurez-vous que votre fichier `.env` contient:
```
GEMINI_API_KEY=AIzaSyD0ua3Qidnv-uzmg9ZT3jsrB-CH46QeVz4
FLASK_PORT=5000
FLASK_DEBUG=True
```

### 3. Lancer l'API

```bash
cd flask_app
python app.py
```

L'API sera disponible sur: `http://localhost:5000`

---

## 📍 Endpoints Disponibles

### 1. Health Check

**GET** `/health`

Vérifie que l'API fonctionne correctement.

**Exemple:**
```bash
curl http://localhost:5000/health
```

**Réponse:**
```json
{
  "status": "ok",
  "service": "Invoice Extraction API",
  "version": "1.0.0"
}
```

---

### 2. Extraction de Facture

**POST** `/api/invoice/extract`

Extrait les données d'une facture (image ou PDF).

**Headers:**
- `Content-Type: multipart/form-data`

**Body:**
- `file`: Fichier de la facture (PNG, JPG, JPEG, PDF)

**Exemple avec cURL:**
```bash
curl -X POST http://localhost:5000/api/invoice/extract \
  -F "file=@facture.jpg"
```

**Exemple avec Python:**
```python
import requests

url = "http://localhost:5000/api/invoice/extract"
files = {'file': open('facture.jpg', 'rb')}
response = requests.post(url, files=files)
print(response.json())
```

**Réponse (Succès - 200):**
```json
{
  "success": true,
  "message": "Facture extraite avec succès",
  "data": {
    "numero_facture": "005449",
    "date_facture": "2023-07-12",
    "date_echeance": "2023-08-12",
    "fournisseur": {
      "nom": "Éditions Mirada",
      "adresse": "3230, avenue Ducharme\nLongueuil (Québec) J4J 5G6",
      "siret": null,
      "email": "mirada@mirada.qc.ca",
      "telephone": "123 456-7890"
    },
    "client": {
      "nom": "Librairie Richelieu",
      "adresse": "275, rue du Faubourg, RC\nLongueuil (Québec) J4G 5T9",
      "siret": null
    },
    "lignes": [
      {
        "description": "La cuisine de tous les jours",
        "quantite": 12,
        "prix_unitaire": 15.95,
        "total": 191.4,
        "tva": null
      }
    ],
    "montant_ht": 344.65,
    "montant_tva": 17.23,
    "montant_ttc": 361.88,
    "devise": "$",
    "conditions_paiement": "Pour éviter les frais...",
    "notes": null
  }
}
```

**Réponse (Erreur - 400):**
```json
{
  "success": false,
  "error": "Extension non autorisée",
  "message": "Extensions autorisées: png, jpg, jpeg, pdf"
}
```

**Réponse (Erreur - 500):**
```json
{
  "success": false,
  "error": "Erreur lors de l'extraction",
  "message": "Erreur lors de l'extraction de la facture"
}
```

---

## 🔌 Intégration avec Spring Boot

### Option 1: RestTemplate

```java
@Service
public class InvoiceService {
    
    private final RestTemplate restTemplate;
    private final String apiUrl = "http://localhost:5000";
    
    public InvoiceService(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }
    
    public InvoiceData extractInvoice(MultipartFile file) throws IOException {
        // Préparer la requête
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.MULTIPART_FORM_DATA);
        
        MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
        body.add("file", file.getResource());
        
        HttpEntity<MultiValueMap<String, Object>> requestEntity = 
            new HttpEntity<>(body, headers);
        
        // Envoyer la requête
        ResponseEntity<InvoiceResponse> response = restTemplate.postForEntity(
            apiUrl + "/api/invoice/extract",
            requestEntity,
            InvoiceResponse.class
        );
        
        if (response.getBody() != null && response.getBody().isSuccess()) {
            return response.getBody().getData();
        }
        
        throw new RuntimeException("Échec de l'extraction");
    }
}

// Classes de modèle
@Data
public class InvoiceResponse {
    private boolean success;
    private String message;
    private InvoiceData data;
}

@Data
public class InvoiceData {
    private String numeroFacture;
    private String dateFacture;
    private String dateEcheance;
    private Fournisseur fournisseur;
    private Client client;
    private List<LigneFacture> lignes;
    private Double montantHt;
    private Double montantTva;
    private Double montantTtc;
    private String devise;
    private String conditionsPaiement;
    private String notes;
}
```

### Option 2: WebClient (Reactive)

```java
@Service
public class InvoiceService {
    
    private final WebClient webClient;
    
    public InvoiceService(WebClient.Builder webClientBuilder) {
        this.webClient = webClientBuilder
            .baseUrl("http://localhost:5000")
            .build();
    }
    
    public Mono<InvoiceData> extractInvoice(FilePart filePart) {
        return webClient.post()
            .uri("/api/invoice/extract")
            .contentType(MediaType.MULTIPART_FORM_DATA)
            .body(BodyInserters.fromMultipartData("file", filePart))
            .retrieve()
            .bodyToMono(InvoiceResponse.class)
            .map(response -> {
                if (response.isSuccess()) {
                    return response.getData();
                }
                throw new RuntimeException(response.getMessage());
            });
    }
}
```

### Option 3: Feign Client

```java
@FeignClient(name = "invoice-api", url = "http://localhost:5000")
public interface InvoiceApiClient {
    
    @PostMapping(value = "/api/invoice/extract", 
                 consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    InvoiceResponse extractInvoice(@RequestPart("file") MultipartFile file);
}

// Utilisation
@Service
public class InvoiceService {
    
    @Autowired
    private InvoiceApiClient invoiceApiClient;
    
    public InvoiceData extractInvoice(MultipartFile file) {
        InvoiceResponse response = invoiceApiClient.extractInvoice(file);
        if (response.isSuccess()) {
            return response.getData();
        }
        throw new RuntimeException(response.getMessage());
    }
}
```

---

## 🧪 Tests

### Test avec cURL

```bash
# Health check
curl http://localhost:5000/health

# Extraction
curl -X POST http://localhost:5000/api/invoice/extract \
  -F "file=@facture.jpg" \
  -H "Accept: application/json"
```

### Test avec Postman

1. Créer une nouvelle requête POST
2. URL: `http://localhost:5000/api/invoice/extract`
3. Body → form-data
4. Ajouter une clé `file` de type File
5. Sélectionner votre fichier
6. Envoyer

### Test avec Python

```python
import requests

# Test health
response = requests.get('http://localhost:5000/health')
print(response.json())

# Test extraction
url = 'http://localhost:5000/api/invoice/extract'
files = {'file': open('facture.jpg', 'rb')}
response = requests.post(url, files=files)

if response.json()['success']:
    print("✅ Extraction réussie!")
    print(response.json()['data'])
else:
    print("❌ Erreur:", response.json()['message'])
```

---

## ⚙️ Configuration

### Variables d'environnement (.env)

```bash
# API Gemini
GEMINI_API_KEY=votre_cle_api

# Flask
FLASK_PORT=5000
FLASK_DEBUG=True

# Limites
MAX_FILE_SIZE_MB=10
```

### Limites par défaut

- **Taille max fichier:** 10 MB
- **Extensions autorisées:** PNG, JPG, JPEG, PDF
- **Timeout:** 30 secondes

---

## 🐛 Dépannage

### Erreur: "GEMINI_API_KEY non trouvée"
- Vérifiez que le fichier `.env` existe dans le dossier racine
- Vérifiez que la clé API est correcte

### Erreur: "Fichier trop volumineux"
- La taille maximale est de 10 MB
- Compressez votre image ou PDF

### Erreur: "Extension non autorisée"
- Formats acceptés: PNG, JPG, JPEG, PDF
- Vérifiez l'extension de votre fichier

### Erreur 500: "Erreur lors de l'extraction"
- Vérifiez que la facture est lisible
- Vérifiez votre connexion internet (pour Gemini API)
- Consultez les logs de l'application

---

## 📊 Structure du Projet

```
flask_app/
├── app.py                      # Application principale
├── services/
│   ├── __init__.py
│   └── gemini_service.py       # Service d'extraction Gemini
├── utils/
│   ├── __init__.py
│   └── file_handler.py         # Gestion des fichiers
└── uploads/                    # Fichiers temporaires
```

---

## 🔒 Sécurité

**Recommandations pour la production:**

1. ✅ Ajouter une authentification (API Key, JWT)
2. ✅ Implémenter le rate limiting
3. ✅ Valider rigoureusement les fichiers
4. ✅ Utiliser HTTPS
5. ✅ Ajouter des logs détaillés
6. ✅ Configurer CORS correctement

---

## 📈 Améliorations Futures

- [ ] Authentification par API Key
- [ ] Rate limiting
- [ ] Stockage des résultats en base de données
- [ ] Traitement asynchrone pour gros fichiers
- [ ] Webhooks pour notifications
- [ ] Export en CSV/Excel
- [ ] Interface web de test

---

## 📞 Support

Pour toute question ou problème, consultez les logs de l'application ou ouvrez une issue.
