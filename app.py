from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
import os
import json
import tempfile
from agents.job_search_agent import JobSearchAgent
from agents.cv_generator_agent import CVGeneratorAgent
from agents.cover_letter_agent import CoverLetterAgent
import PyPDF2
import docx

app = Flask(__name__)
CORS(app)

# Configuration - Changement pour Groq Cloud API
GROQ_API_KEY = os.getenv('GROQ_API_KEY', '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')

# Initialize agents avec Groq API
job_search_agent = JobSearchAgent(GROQ_API_KEY)
cv_generator_agent = CVGeneratorAgent(GROQ_API_KEY)
cover_letter_agent = CoverLetterAgent(GROQ_API_KEY)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search-jobs', methods=['POST'])
def search_jobs():
    try:
        data = request.json
        job_title = data.get('job_title', '')
        location = data.get('location', '')
        experience_level = data.get('experience_level', '')
        skills = data.get('skills', '')
        
        result = job_search_agent.search_jobs(job_title, location, experience_level, skills)
        
        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/generate-cv', methods=['POST'])
def generate_cv():
    try:
        # Handle file upload
        if 'cv_file' in request.files:
            cv_file = request.files['cv_file']
            cv_content = extract_text_from_file(cv_file)
        else:
            cv_content = request.form.get('cv_content', '')
        
        job_description = request.form.get('job_description', '')
        personal_info = request.form.get('personal_info', '')
        
        result = cv_generator_agent.generate_cv(cv_content, job_description, personal_info)
        
        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/generate-cover-letter', methods=['POST'])
def generate_cover_letter():
    try:
        # Handle file upload
        if 'cv_file' in request.files:
            cv_file = request.files['cv_file']
            cv_content = extract_text_from_file(cv_file)
        else:
            cv_content = request.form.get('cv_content', '')
        
        job_description = request.form.get('job_description', '')
        company_info = request.form.get('company_info', '')
        
        result = cover_letter_agent.generate_cover_letter(cv_content, job_description, company_info)
        
        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/download-latex', methods=['POST'])
def download_latex():
    try:
        data = request.json
        latex_content = data.get('latex_content', '')
        filename = data.get('filename', 'cv.tex')
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False) as f:
            f.write(latex_content)
            temp_path = f.name
        
        return send_file(temp_path, as_attachment=True, download_name=filename)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def extract_text_from_file(file):
    """Extract text from uploaded PDF or DOCX file"""
    filename = file.filename.lower()
    
    if filename.endswith('.pdf'):
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    
    elif filename.endswith('.docx'):
        doc = docx.Document(file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    
    elif filename.endswith('.txt'):
        return file.read().decode('utf-8')
    
    else:
        raise ValueError("Format de fichier non supporté. Utilisez PDF, DOCX ou TXT.")

if __name__ == '__main__':
    app.run(debug=True, port=5000)