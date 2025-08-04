"""
Version personnalisée de DuckDuckGoTools sans les warnings
"""

import json
from typing import List, Dict, Any, Optional
import warnings

# Supprimer les warnings de duckduckgo_search
warnings.filterwarnings("ignore", message="This package.*has been renamed.*ddgs")

try:
    from ddgs import DDGS
except ImportError:
    try:
        from duckduckgo_search import DDGS
    except ImportError:
        print("❌ Impossible d'importer DDGS. Installez ddgs: pip install ddgs")
        DDGS = None

class CustomDuckDuckGoTools:
    """Version personnalisée de DuckDuckGoTools sans warnings"""
    
    def __init__(self):
        self.name = "duckduckgo_search"
        self.description = "Search the web using DuckDuckGo"
        
    def search_web(self, query: str, max_results: int = 5, region: str = "wt-wt") -> List[Dict[str, Any]]:
        """
        Recherche web avec DuckDuckGo
        
        Args:
            query: Terme de recherche
            max_results: Nombre maximum de résultats
            region: Région de recherche (wt-wt pour mondial)
        
        Returns:
            Liste des résultats de recherche
        """
        if DDGS is None:
            return [{"error": "DDGS not available. Install with: pip install ddgs"}]
        
        try:
            with DDGS() as ddgs:
                results = []
                search_results = ddgs.text(
                    keywords=query,
                    region=region,
                    max_results=max_results,
                    safesearch="moderate"
                )
                
                for result in search_results:
                    results.append({
                        "title": result.get("title", ""),
                        "url": result.get("href", ""),
                        "snippet": result.get("body", ""),
                        "source": "DuckDuckGo"
                    })
                
                return results
                
        except Exception as e:
            return [{"error": f"Erreur lors de la recherche: {str(e)}"}]
    
    def search_news(self, query: str, max_results: int = 5, region: str = "wt-wt") -> List[Dict[str, Any]]:
        """
        Recherche d'actualités avec DuckDuckGo
        """
        if DDGS is None:
            return [{"error": "DDGS not available. Install with: pip install ddgs"}]
        
        try:
            with DDGS() as ddgs:
                results = []
                news_results = ddgs.news(
                    keywords=query,
                    region=region,
                    max_results=max_results,
                    safesearch="moderate"
                )
                
                for result in news_results:
                    results.append({
                        "title": result.get("title", ""),
                        "url": result.get("url", ""),
                        "snippet": result.get("body", ""),
                        "date": result.get("date", ""),
                        "source": result.get("source", "DuckDuckGo News")
                    })
                
                return results
                
        except Exception as e:
            return [{"error": f"Erreur lors de la recherche d'actualités: {str(e)}"}]

# Votre code modifié pour utiliser CustomDuckDuckGoTools
from textwrap import dedent
from agno.agent import Agent
from agno.models.google import Gemini
import requests
from bs4 import BeautifulSoup
import json
import time

class JobSearchAgent:
    def __init__(self, api_key):
        # Utiliser notre version personnalisée au lieu de DuckDuckGoTools()
        custom_tools = CustomDuckDuckGoTools()
        
        self.agent = Agent(
            name="Job Search Agent",
            model=Gemini(id="gemini-2.0-flash", api_key=api_key),
            tools=[],  # On va gérer la recherche manuellement
            show_tool_calls=True,
            instructions=dedent("""\
                🔍 Vous êtes un expert en recherche d'emploi spécialisé dans la collecte d'offres d'emploi !
                
                Votre mission :
                1. 📊 Recherche Multi-Plateforme
                   - LinkedIn Jobs
                   - Indeed
                   - Glassdoor
                   - Monster
                   - StepStone
                   - Apec (France)
                   - Pôle Emploi (France)
                   - Sites d'entreprises
                
                2. 🎯 Analyse des Offres
                   - Titre du poste
                   - Entreprise
                   - Localisation
                   - Salaire (si disponible)
                   - Type de contrat
                   - Compétences requises
                   - Description complète
                   - Date de publication
                   - Lien vers l'offre
                
                3. 📋 Filtrage Intelligent
                   - Correspondance avec le profil
                   - Niveau d'expérience requis
                   - Technologies demandées
                   - Secteur d'activité
                
                4. 📈 Classement par Pertinence
                   - Score de compatibilité
                   - Priorité selon critères
                   - Recommandations personnalisées
                
                Format de sortie :
                - JSON structuré avec toutes les informations
                - Résumé exécutif des meilleures opportunités
                - Conseils pour optimiser les candidatures
                
                Style de recherche :
                - Exhaustif et méthodique
                - Mise à jour en temps réel
                - Analyse comparative
                - Alertes sur nouvelles offres
            """),
            add_datetime_to_instructions=True,
            markdown=True,
        )
        
        self.search_tools = custom_tools
    
    def search_jobs_manual(self, job_title, location="", experience_level="", skills=""):
        """Recherche manuelle d'emplois"""
        search_queries = [
            f"{job_title} jobs {location}",
            f"{job_title} emploi {location}",
            f"{job_title} offre {location}",
            f"site:linkedin.com/jobs {job_title} {location}",
            f"site:indeed.com {job_title} {location}"
        ]
        
        all_results = []
        
        for query in search_queries:
            print(f"🔍 Recherche: {query}")
            results = self.search_tools.search_web(query, max_results=10)
            all_results.extend(results)
            time.sleep(1)  # Éviter le rate limiting
        
        return all_results
    
    def search_jobs(self, job_title, location="", experience_level="", skills=""):
        # D'abord faire une recherche manuelle
        search_results = self.search_jobs_manual(job_title, location, experience_level, skills)
        
        # Ensuite analyser avec l'agent
        query = f"""
        Analysez ces résultats de recherche d'emploi pour :
        - Poste : {job_title}
        - Localisation : {location}
        - Niveau d'expérience : {experience_level}
        - Compétences : {skills}
        
        Résultats de recherche :
        {json.dumps(search_results, indent=2, ensure_ascii=False)}
        
        Fournissez un rapport détaillé et structuré.
        """
        
        return self.agent.run(query)

# Test de l'outil personnalisé
def test_custom_tools():
    print("🧪 Test des outils personnalisés...")
    tools = CustomDuckDuckGoTools()
    
    # Test de recherche web
    results = tools.search_web("développeur python paris", max_results=3)
    print("📊 Résultats de recherche web:")
    for i, result in enumerate(results, 1):
        print(f"{i}. {result.get('title', 'N/A')}")
        print(f"   URL: {result.get('url', 'N/A')}")
        print(f"   Snippet: {result.get('snippet', 'N/A')[:100]}...")
        print()

if __name__ == "__main__":
    # Test des outils
    test_custom_tools()
    
    # Utilisation de l'agent
    api_key = "VOTRE_API_KEY_GEMINI"
    agent = JobSearchAgent(api_key)
    
    result = agent.search_jobs(
        job_title="Développeur Python",
        location="Paris",
        experience_level="Junior",
        skills="Python, Django, Flask"
    )
    print(result)