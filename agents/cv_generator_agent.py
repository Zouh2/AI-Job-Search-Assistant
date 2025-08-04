import requests
import json
from datetime import datetime

class CVGeneratorAgent:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        self.instructions = """
📄 Vous êtes un expert en création de CV optimisés pour les systèmes ATS !

Votre expertise :
1. 🎯 Personnalisation Intelligente
   - Adaptation au poste ciblé
   - Mise en avant des compétences pertinentes
   - Optimisation des mots-clés ATS
   - Structure adaptée au secteur

2. 🔧 Optimisation ATS
   - Format machine-readable
   - Mots-clés stratégiques
   - Structure standardisée
   - Éviter les éléments graphiques complexes

3. 📐 Templates LaTeX Overleaf
   - Code LaTeX professionnel
   - Design moderne et épuré
   - Sections bien structurées
   - Compatible ATS

4. 💼 Sections Optimisées
   - Profil professionnel accrocheur
   - Expériences avec résultats quantifiés
   - Compétences techniques et soft skills
   - Formation et certifications
   - Projets pertinents

Processus de création :
1. Analyse de l'offre d'emploi
2. Extraction des mots-clés importants
3. Adaptation du CV original
4. Génération du code LaTeX
5. Optimisation finale

Format de sortie :
- Code LaTeX complet pour Overleaf
- Conseils de personnalisation
- Score d'optimisation ATS
- Recommandations d'amélioration
"""

    def _call_groq_api(self, messages, model="mixtral-8x7b-32768", max_tokens=40096, temperature=0.7):
        """
        Appel à l'API Groq
        """
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content']
        
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erreur API Groq: {str(e)}")
        except KeyError as e:
            raise Exception(f"Format de réponse inattendu: {str(e)}")

    def generate_cv(self, original_cv, job_description, personal_info=None):
        """
        Génère un CV personnalisé optimisé ATS
        """
        try:
            # Ajouter la date actuelle aux instructions
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            instructions_with_date = f"{self.instructions}\n\nDate et heure actuelles: {current_datetime}"
            
            # Construire le prompt
            query = f"""
            Créez un CV personnalisé optimisé ATS basé sur :
           
            CV ORIGINAL :
            {original_cv}
           
            OFFRE D'EMPLOI :
            {job_description}
           
            INFORMATIONS PERSONNELLES :
            {personal_info if personal_info else "Utiliser les informations du CV original"}
           
            Générez un code LaTeX complet pour Overleaf, optimisé pour les systèmes ATS.
            
            INSTRUCTIONS IMPORTANTES :
            1. Commencez directement par le code LaTeX complet
            2. Incluez tous les packages nécessaires
            3. Utilisez une structure moderne et professionnelle
            4. Optimisez pour les mots-clés de l'offre d'emploi
            5. Assurez-vous que le CV soit lisible par les systèmes ATS
            6. Utilisez des sections claires : Contact, Profil, Expérience, Formation, Compétences
            7. Quantifiez les réalisations quand possible
            8. Adaptez le vocabulaire au secteur ciblé
            
            Après le code LaTeX, ajoutez :
            - Un score d'optimisation ATS estimé (/100)
            - 3-5 conseils de personnalisation
            - Les mots-clés importants identifiés
            """
            
            # Préparer les messages pour l'API
            messages = [
                {
                    "role": "system",
                    "content": instructions_with_date
                },
                {
                    "role": "user",
                    "content": query
                }
            ]
            
            # Appel à l'API Groq
            response = self._call_groq_api(
                messages=messages,
                model="mixtral-8x7b-32768",  # Modèle recommandé pour la génération de texte
                max_tokens=4096,
                temperature=0.7
            )
            
            return response
            
        except Exception as e:
            raise Exception(f"Erreur lors de la génération du CV: {str(e)}")

    def analyze_job_keywords(self, job_description):
        """
        Analyse les mots-clés importants d'une offre d'emploi
        """
        try:
            messages = [
                {
                    "role": "system",
                    "content": "Tu es un expert en analyse d'offres d'emploi. Identifie les mots-clés les plus importants pour l'optimisation ATS."
                },
                {
                    "role": "user",
                    "content": f"""
                    Analyse cette offre d'emploi et extrais :
                    1. Les 10 mots-clés techniques les plus importants
                    2. Les 5 compétences soft skills mentionnées
                    3. Les exigences de formation/certification
                    4. Le niveau d'expérience requis
                    5. Les responsabilités clés
                    
                    OFFRE D'EMPLOI :
                    {job_description}
                    
                    Format de réponse : JSON structuré
                    """
                }
            ]
            
            response = self._call_groq_api(messages, temperature=0.3)
            return response
            
        except Exception as e:
            raise Exception(f"Erreur lors de l'analyse des mots-clés: {str(e)}")

    def optimize_cv_section(self, section_content, job_keywords, section_type):
        """
        Optimise une section spécifique du CV
        """
        try:
            messages = [
                {
                    "role": "system",
                    "content": f"Tu es un expert en optimisation de CV. Optimise la section '{section_type}' pour inclure les mots-clés pertinents."
                },
                {
                    "role": "user",
                    "content": f"""
                    Optimise cette section de CV :
                    
                    SECTION ACTUELLE ({section_type}) :
                    {section_content}
                    
                    MOTS-CLÉS À INTÉGRER :
                    {job_keywords}
                    
                    Réécrire la section pour :
                    1. Intégrer naturellement les mots-clés
                    2. Quantifier les résultats
                    3. Utiliser des verbes d'action
                    4. Maintenir la vérité des informations
                    5. Optimiser pour les systèmes ATS
                    """
                }
            ]
            
            response = self._call_groq_api(messages, temperature=0.5)
            return response
            
        except Exception as e:
            raise Exception(f"Erreur lors de l'optimisation de la section: {str(e)}")

    def get_cv_feedback(self, cv_latex, job_description):
        """
        Fournit un feedback détaillé sur le CV généré
        """
        try:
            messages = [
                {
                    "role": "system",
                    "content": "Tu es un recruteur expert qui évalue les CV. Fournis un feedback constructif et un score ATS."
                },
                {
                    "role": "user",
                    "content": f"""
                    Évalue ce CV LaTeX par rapport à cette offre d'emploi :
                    
                    CV LATEX :
                    {cv_latex}
                    
                    OFFRE D'EMPLOI :
                    {job_description}
                    
                    Fournis :
                    1. Score ATS estimé (/100) avec justification
                    2. Points forts du CV
                    3. Points à améliorer
                    4. Mots-clés manquants importants
                    5. Suggestions de reformulation
                    6. Note globale et recommandations
                    """
                }
            ]
            
            response = self._call_groq_api(messages, temperature=0.3)
            return response
            
        except Exception as e:
            raise Exception(f"Erreur lors de l'évaluation du CV: {str(e)}")