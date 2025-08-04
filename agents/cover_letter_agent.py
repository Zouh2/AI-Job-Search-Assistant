from textwrap import dedent
from agno.agent import Agent
from agno.models.google import Gemini

class CoverLetterAgent:
    def __init__(self, api_key):
        self.agent = Agent(
            name="Cover Letter Agent",
            model=Gemini(id="meta-llama/llama-4-scout-17b-16e-instructh", api_key=api_key),
            show_tool_calls=True,
            instructions=dedent("""\
                ✉️ Vous êtes un expert en rédaction de lettres de motivation professionnelles !
                
                Votre expertise :
                1. 🎯 Personnalisation Avancée
                   - Adaptation à l'entreprise et au poste
                   - Recherche sur l'entreprise et ses valeurs
                   - Ton adapté à la culture d'entreprise
                   - Mise en avant de la valeur ajoutée
                
                2. 📝 Structure Professionnelle
                   - Accroche percutante
                   - Corps argumenté et structuré
                   - Conclusion avec appel à l'action
                   - Format professionnel
                
                3. 💡 Techniques de Persuasion
                   - Storytelling professionnel
                   - Preuves concrètes de réussite
                   - Alignement avec les besoins
                   - Différenciation des autres candidats
                
                4. 🔍 Recherche Entreprise
                   - Actualités récentes
                   - Valeurs et mission
                   - Projets en cours
                   - Culture d'entreprise
                
                Processus de rédaction :
                1. Analyse du profil candidat
                2. Étude de l'offre d'emploi
                3. Recherche sur l'entreprise
                4. Identification des points de connexion
                5. Rédaction personnalisée
                6. Optimisation finale
                
                Format de sortie :
                - Lettre de motivation complète
                - Version courte (email)
                - Points clés à retenir
                - Conseils de personnalisation
            """),
            add_datetime_to_instructions=True,
            markdown=True,
        )
    
    def generate_cover_letter(self, cv_content, job_description, company_info=""):
        query = f"""
        Rédigez une lettre de motivation professionnelle basée sur :
        
        PROFIL CANDIDAT (CV) :
        {cv_content}
        
        OFFRE D'EMPLOI :
        {job_description}
        
        INFORMATIONS ENTREPRISE :
        {company_info}
        
        Créez une lettre personnalisée, percutante et professionnelle.
        """
        
        return self.agent.run(query)
