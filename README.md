# AI Job Search Assistant

Un système complet de 3 agents IA pour optimiser votre recherche d'emploi, utilisant l'**API Google Gemini** et la bibliothèque Agno.

## 🤖 Agents IA

### 1. Agent de Recherche d'Emploi
- Recherche sur LinkedIn, Indeed, Glassdoor, Monster, etc.
- Analyse et filtrage intelligent des offres
- Classement par pertinence
- Extraction des informations clés

### 2. Agent Générateur de CV
- Personnalisation basée sur l'offre d'emploi
- Optimisation pour les systèmes ATS
- Génération de code LaTeX pour Overleaf
- Adaptation des mots-clés stratégiques

### 3. Agent Lettre de Motivation
- Rédaction personnalisée et professionnelle
- Recherche sur l'entreprise
- Adaptation au poste et à la culture d'entreprise
- Techniques de persuasion avancées

## 🚀 Installation

1. **Cloner le repository**
\`\`\`bash
git clone <repository-url>
cd job-search-ai-agents
\`\`\`

2. **Installer les dépendances**
\`\`\`bash
pip install -r requirements.txt
\`\`\`

3. **Configuration Google Gemini API**
\`\`\`bash
cp .env.example .env
# Éditer .env avec votre clé API Google Gemini
\`\`\`

4. **Lancer l'application**
\`\`\`bash
# Version avec Agno
python app.py

# Ou version directe avec Google Gemini API
python app_gemini_direct.py
\`\`\`

5. **Accéder à l'interface**
Ouvrir http://localhost:5000 dans votre navigateur

## 🔧 Configuration

### API Google Gemini
1. Aller sur https://makersuite.google.com/app/apikey
2. Créer une nouvelle clé API
3. Ajouter la clé dans le fichier `.env` :
   \`\`\`
   GOOGLE_API_KEY=your_google_gemini_api_key_here
   \`\`\`

### Modèles Disponibles
- **gemini-1.5-pro** : Modèle le plus avancé (recommandé)
- **gemini-1.5-flash** : Plus rapide, moins de tokens
- **gemini-pro** : Version standard

## 💡 Utilisation

### Recherche d'Emploi
1. Saisir le titre du poste recherché
2. Spécifier la localisation et le niveau d'expérience
3. Ajouter les compétences clés
4. Lancer la recherche intelligente

### Génération de CV
1. Uploader votre CV original
2. Coller la description du poste ciblé
3. Ajouter des informations personnelles (optionnel)
4. Générer le CV optimisé ATS
5. Télécharger le code LaTeX pour Overleaf

### Lettre de Motivation
1. Uploader votre CV/profil
2. Coller la description du poste
3. Ajouter des informations sur l'entreprise
4. Générer la lettre personnalisée
5. Copier ou télécharger le résultat

## 🎯 Fonctionnalités

- **Interface moderne et responsive**
- **Upload par glisser-déposer**
- **Génération en temps réel**
- **Optimisation ATS automatique**
- **Export LaTeX pour Overleaf**
- **Copie en un clic**
- **Messages de statut informatifs**

## 🔍 Optimisation ATS

Le système génère des CV optimisés pour les systèmes de suivi des candidatures (ATS) :
- Format machine-readable
- Mots-clés stratégiques
- Structure standardisée
- Sections bien définies
- Évitement des éléments graphiques complexes

## 📱 Interface Responsive

L'interface s'adapte automatiquement à tous les écrans :
- Desktop
- Tablette
- Mobile

## 🛠️ Technologies

- **Backend**: Flask, Python
- **Frontend**: HTML5, CSS3, JavaScript
- **IA**: Google Gemini via Agno
- **Upload**: Drag & Drop, File API
- **Export**: LaTeX, PDF

## 📄 Structure du Projet

\`\`\`
job-search-ai-agents/
├── agents/
│   ├── job_search_agent.py
│   ├── cv_generator_agent.py
│   └── cover_letter_agent.py
├── static/
│   ├── css/style.css
│   └── js/script.js
├── templates/
│   └── index.html
├── app.py
├── app_gemini_direct.py
├── requirements.txt
├── .env.example
└── README.md
\`\`\`

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer des améliorations
- Ajouter de nouvelles fonctionnalités

## 📞 Support

Pour toute question ou problème, créez une issue sur le repository.

## 💡 Avantages de Google Gemini

- **Multimodal** : Traite texte, images, code
- **Context long** : Jusqu'à 1M tokens
- **Gratuit** : Quota généreux gratuit
- **Rapide** : Réponses ultra-rapides
- **Précis** : Excellente compréhension du contexte
"# AI-Job-Search-Assistant" 
