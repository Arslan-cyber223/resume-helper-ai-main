from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from werkzeug.utils import secure_filename
import PyPDF2
import docx
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx', 'txt'}

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY', ''))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def extract_text_from_pdf(file_path):
    """Extract text from PDF file"""
    text = ""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
    except Exception as e:
        print(f"Error extracting PDF: {e}")
    return text

def extract_text_from_docx(file_path):
    """Extract text from DOCX file"""
    text = ""
    try:
        doc = docx.Document(file_path)
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
    except Exception as e:
        print(f"Error extracting DOCX: {e}")
    return text

def extract_text_from_txt(file_path):
    """Extract text from TXT file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error extracting TXT: {e}")
        return ""

def parse_resume_to_html(text):
    """Parse resume text and convert to structured HTML format using AI"""
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"""Convert this resume text into structured HTML format suitable for editing.

Rules:
1. Identify sections: Header/Contact, Summary/Objective, Experience, Education, Skills, etc.
2. Format the header with name as <h1> and contact info with icons
3. Each section should have <h2 class="section-title"> with appropriate Font Awesome icon
4. Experience items should use <h3> for job titles, <p class="company-info"> for company/dates, and <ul> for bullet points
5. Skills should use <span class="skill-tag"> for each skill
6. Wrap sections in <div class="resume-section">
7. Make elements editable with contenteditable="true" and class="editable"
8. Preserve all original content and details
9. Use these icons: <i class="fas fa-envelope"></i>, <i class="fas fa-phone"></i>, <i class="fas fa-user"></i>, <i class="fas fa-briefcase"></i>, <i class="fas fa-graduation-cap"></i>, <i class="fas fa-cog"></i>

Resume text:
{text}

Return ONLY the HTML code without any explanations or markdown code blocks."""
        
        response = model.generate_content(prompt)
        html_content = response.text.strip()
        
        # Clean up any markdown code blocks if present
        if html_content.startswith('```html'):
            html_content = html_content[7:]
        if html_content.startswith('```'):
            html_content = html_content[3:]
        if html_content.endswith('```'):
            html_content = html_content[:-3]
        
        return html_content.strip()
    except Exception as e:
        print(f"Error parsing resume: {e}")
        # Fallback to basic formatting
        return format_text_to_basic_html(text)

def format_text_to_basic_html(text):
    """Fallback function to create basic HTML structure from text"""
    lines = text.split('\n')
    html_parts = []
    
    # Try to identify name (usually first non-empty line)
    name = ""
    contact = []
    content_lines = []
    
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        if i == 0 and len(line) < 50 and not '@' in line:
            name = line
        elif '@' in line or 'phone' in line.lower() or '+' in line:
            contact.append(line)
        else:
            content_lines.append(line)
    
    # Build header
    if name:
        html_parts.append(f'<div class="resume-section header-section">')
        html_parts.append(f'<h1 class="editable" contenteditable="true">{name}</h1>')
        if contact:
            html_parts.append(f'<p class="contact-info editable" contenteditable="true">{" | ".join(contact)}</p>')
        html_parts.append('</div>')
    
    # Add content section
    html_parts.append('<div class="resume-section">')
    html_parts.append('<h2 class="section-title editable" contenteditable="true"><i class="fas fa-file-alt"></i> Resume Content</h2>')
    html_parts.append('<div class="editable" contenteditable="true">')
    
    for line in content_lines:
        if line:
            html_parts.append(f'<p>{line}</p>')
    
    html_parts.append('</div></div>')
    
    return '\n'.join(html_parts)

@app.route('/')
def landing():
    """Landing page"""
    return render_template('landing.html')

@app.route('/app')
def index():
    """Main application page"""
    return render_template('index.html')

@app.route('/api/upload-resume', methods=['POST'])
def upload_resume():
    """Handle resume file upload"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Extract text based on file type
        file_ext = filename.rsplit('.', 1)[1].lower()
        if file_ext == 'pdf':
            text = extract_text_from_pdf(file_path)
        elif file_ext == 'docx':
            text = extract_text_from_docx(file_path)
        else:
            text = extract_text_from_txt(file_path)
        
        # Parse resume text into structured HTML
        html_content = parse_resume_to_html(text)
        
        # Clean up the file
        os.remove(file_path)
        
        return jsonify({'html': html_content, 'success': True})
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/api/get-suggestions', methods=['POST'])
def get_suggestions():
    """Get AI-powered suggestions for resume improvement"""
    data = request.json
    resume_text = data.get('text', '')
    section = data.get('section', 'general')
    
    if not resume_text:
        return jsonify({'error': 'No resume text provided'}), 400
    
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompts = {
            'general': f"""Analyze this resume and provide 5 specific, actionable suggestions to improve it. 
Focus on: content clarity, impact statements, formatting, keyword optimization, and achievements quantification.

Resume:
{resume_text}

Provide suggestions in JSON format as an array of objects with 'title' and 'description' fields.""",
            
            'summary': f"""Analyze the professional summary/objective section of this resume and suggest improvements.
Provide 3-5 suggestions to make it more compelling and targeted.

Resume:
{resume_text}

Provide suggestions in JSON format as an array of objects with 'title' and 'description' fields.""",
            
            'experience': f"""Analyze the work experience section and suggest improvements.
Focus on: action verbs, quantifiable achievements, impact statements, and relevance.

Resume:
{resume_text}

Provide suggestions in JSON format as an array of objects with 'title' and 'description' fields.""",
            
            'skills': f"""Analyze the skills section and suggest improvements.
Focus on: relevant skills, organization, technical vs soft skills balance.

Resume:
{resume_text}

Provide suggestions in JSON format as an array of objects with 'title' and 'description' fields."""
        }
        
        prompt = prompts.get(section, prompts['general'])
        response = model.generate_content(prompt)
        
        # Try to parse JSON from response
        try:
            suggestions_text = response.text.strip()
            # Remove markdown code blocks if present
            if suggestions_text.startswith('```json'):
                suggestions_text = suggestions_text[7:]
            if suggestions_text.startswith('```'):
                suggestions_text = suggestions_text[3:]
            if suggestions_text.endswith('```'):
                suggestions_text = suggestions_text[:-3]
            
            suggestions = json.loads(suggestions_text.strip())
            return jsonify({'suggestions': suggestions, 'success': True})
        except json.JSONDecodeError:
            # If JSON parsing fails, return as plain text
            return jsonify({
                'suggestions': [{'title': 'AI Suggestion', 'description': response.text}],
                'success': True
            })
    
    except Exception as e:
        return jsonify({'error': f'Failed to generate suggestions: {str(e)}'}), 500

@app.route('/api/improve-text', methods=['POST'])
def improve_text():
    """Get AI suggestion for improving a specific text section"""
    data = request.json
    text = data.get('text', '')
    context = data.get('context', 'professional experience')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"""Improve this {context} text for a resume. Make it more impactful, professional, and achievement-focused.
Use action verbs and quantify results when possible.

Original text: {text}

Provide only the improved version without explanations."""
        
        response = model.generate_content(prompt)
        improved_text = response.text.strip()
        
        return jsonify({'improved_text': improved_text, 'success': True})
    
    except Exception as e:
        return jsonify({'error': f'Failed to improve text: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
