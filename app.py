from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import docx
import mammoth
from googlesearch import search
from PyPDF2 import PdfReader
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import nltk
 
nltk.download('punkt')
 
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx', 'html'}
 
skills_list = [
    "Communication", "Teamwork", "Problem Solving", "Leadership", "Time Management",
    "Adaptability", "Creativity", "Work Ethic", "Critical Thinking", "Conflict Resolution",
    "Python", "Java", "C++", "JavaScript", "HTML", "CSS", "React", "Angular", "SQL", "Tableau",
    "TensorFlow", "Keras", "Scikit-learn", "MongoDB", "Oracle", "Firewalls", "VPN", "AWS", "Azure",
    "Google Cloud", "Linux", "Windows Server", "iOS", "Android", "React Native",
    "Financial Modeling", "Investment Analysis", "Risk Management", "Auditing", "Budgeting",
    "Forecasting", "Accounting", "Strategic Planning", "Market Analysis", "Sales Strategy",
    "Customer Relationship Management (CRM)", "Project Management", "Negotiation", "Recruitment",
    "Payroll", "Employee Relations", "SEO", "SEM", "Digital Marketing", "Content Marketing",
    "Lead Generation", "Brand Management", "Market Research", "Email Marketing",
    "Social Media Marketing", "Sales Forecasting", "Sales Presentations", "Medical Terminology",
    "Patient Care", "Clinical Research", "Electronic Health Records (EHR)",
    "Electronic Medical Records (EMR)", "Healthcare Administration", "Nursing", "AutoCAD",
    "SolidWorks", "Quality Assurance", "Product Development", "Systems Engineering",
    "Mechanical Engineering", "Electrical Engineering", "Chemical Engineering",
    "Curriculum Development", "Classroom Management", "Educational Technology",
    "Special Education", "Teaching Strategies", "Legal Research", "Contract Law", "Litigation",
    "Compliance", "Intellectual Property Law", "Corporate Law", "Talent Acquisition",
    "Employee Engagement", "Performance Management", "HR Compliance", "Benefits Administration",
    "Network Security", "Database Management", "System Administration", "IT Support",
    "Software Development Lifecycle (SDLC)", "Cybersecurity", "Supply Chain Management",
    "Logistics", "Inventory Management", "Operational Efficiency", "Machine Learning",
    "Data Analysis", "Data Visualization", "Artificial Intelligence", "Deep Learning",
    "Big Data Technologies", "Graphic Design", "UX/UI Design", "Video Editing", "Animation",
    "Photography", "Customer Support", "Client Relations", "Service Level Agreement (SLA) Management",
    "Project Planning", "Site Management", "Real Estate Law", "Property Management",
    "Lean Manufacturing", "Six Sigma", "Production Planning", "Supply Chain Optimization",
    "Media Relations", "Press Release Writing", "Public Speaking", "Event Planning",
    "Merchandising", "Sales Reporting", "Customer Experience Management", "Event Coordination",
    "Guest Services", "Travel Planning", "Sustainability Practices", "Environmental Impact Assessment",
    "Conservation Planning", "Agronomy", "Animal Nutrition", "Farm Management",
    "Hydrogeology", "Sustainability Consulting", "Veterinary Skills", "Acting", "Artistry", "Camera Operation",
    "Composing", "Dancing", "Entertainment Management", "Bulk Earthworks", "Carpentry", "Civil Engineering",
    "Concrete Work", "Construction Management", "Crane Operation", "Masonry", "Plumbing", "Educational Consulting",
    "Teaching", "School Administration", "University Lecturing", "Energy Engineering",
    "Environmental Technology", "Solar Consultancy", "Urban Planning", "Wind Turbine Technology",
    "Accessory Design", "Fashion Design", "Fashion Wholesaling", "Footwear Design", "Textile Design",
    "Certified Public Accounting (CPA)", "Financial Analysis", "Financial Planning",
    "Investment Banking", "Private Equity", "Personal Training", "Group Fitness Instruction",
    "Sports Coaching", "Fitness Technology", "Hotel Management", "Housekeeping",
    "Restaurant Management", "Sommelier Skills", "Tour Guiding", "Travel Planning",
    "Application Development", "Information Security Analysis", "Software Engineering",
    "Web Development", "Aerodynamics", "Robotics", "Nanotechnology", "Biomedical Engineering",
    "Astronautics", "Marine Engineering", "Aerospace Engineering", "Civil Drafting",
    "Structural Analysis", "HVAC Systems", "Hydraulics", "Pneumatics", "Project Coordination",
    "Proposal Writing", "Risk Assessment", "Technical Writing", "Systems Architecture",
    "Agile Methodologies", "Scrum Master", "Lean Six Sigma", "Lean Start-up", "Bioinformatics",
    "Biostatistics", "Molecular Biology", "Genomics", "Proteomics", "Clinical Trials",
    "Pharmaceutical Research", "Pharmacovigilance", "Regulatory Affairs", "Medical Imaging",
    "Health Informatics", "Telemedicine", "Patient Advocacy", "Health Policy", "Epidemiology",
    "Veterinary Medicine", "Dentistry", "Optometry", "Chiropractic", "Occupational Therapy",
    "Physical Therapy", "Radiology", "Surgery", "Pediatrics", "Geriatrics", "Dermatology",
    "Psychiatry", "Neurology", "Oncology", "Cardiology", "Anesthesiology", "Internal Medicine",
    "Family Medicine", "Emergency Medicine", "Obstetrics and Gynecology", "Pathology",
    "Hotel Operations", "Hospitality Management", "Event Management", "Catering", "Bar Management",
    "Wine Tasting", "Food and Beverage Management", "Hospitality Marketing", "Revenue Management",
    "Guest Satisfaction", "Front Desk Operations", "Lodging Management", "Tourism Management",
    "Resort Management", "Club Management", "Travel and Tourism", "Business Strategy",
    "Business Development", "Change Management", "Organizational Development",
    "Performance Improvement", "Business Process Reengineering", "Corporate Communications",
    "Corporate Governance", "Corporate Social Responsibility", "Executive Leadership",
    "Leadership Development", "Market Development", "Operational Excellence", "Organizational Design",
    "Organizational Leadership", "Performance Management", "Process Improvement",
    "Professional Development", "Strategic Communications", "Talent Management", "Technology Integration", "Workforce Development",
    "Business Analysis", "Business Intelligence", "Business Planning", "Customer Insight", "Data Mining",
    "Data Science", "Data Warehousing", "Decision Support", "Financial Management", "Human Resources", "Information Management",
    "Knowledge Management", "Management Consulting", "Operations Management", "Organizational Culture", "Organizational Effectiveness",
    "Quality Management", "Sales Management", "Service Management", "Supply Chain Analysis", "Workforce Planning"
]
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
 
def convert_to_text(filepath):
    text = ''
    if filepath.endswith('.pdf'):
        reader = PdfReader(filepath)
        for page in reader.pages:
            text += page.extract_text()
    elif filepath.endswith('.docx'):
        doc = docx.Document(filepath)
        for paragraph in doc.paragraphs:
            text += paragraph.text
    elif filepath.endswith('.html'):
        with open(filepath, 'rb') as file:
            result = mammoth.convert_to_text(file)
            text = result.value
    return text
 
def extract_skills(text, skills_list):
    extracted_skills = []
    for skill in skills_list:
        if skill.lower() in text.lower():
            extracted_skills.append(skill)
    return extracted_skills
 
def summarize_text(text):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, 3)
    return " ".join([str(sentence) for sentence in summary])
 
def search_courses(skill):
    articles = []
    videos = []
    try:
        for url in search(f"free {skill} online articles", num_results=3):
            articles.append(url)
        for url in search(f"free {skill} online videos", num_results=3):
            videos.append(url)
    except Exception as e:
        print(f"Error fetching resources for {skill}: {e}")
    return {"articles": articles, "videos": videos}
 
@app.route('/', methods=['GET'])
def landing():
    return render_template('landing.html')
 
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'resume' not in request.files:
            return redirect(request.url)
        resume = request.files['resume']
        job_description = request.form['job_description']
        if resume.filename == '':
            return redirect(request.url)
        if resume and allowed_file(resume.filename):
            filename = secure_filename(resume.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            resume.save(filepath)
 
            resume_text = convert_to_text(filepath)
            resume_summary = summarize_text(resume_text)
            job_description_text = job_description
 
            resume_skills = extract_skills(resume_text, skills_list)
            job_description_skills = extract_skills(job_description_text, skills_list)
 
            matching_skills = list(set(resume_skills) & set(job_description_skills))
            missing_skills = list(set(job_description_skills) - set(resume_skills))
 
            recommended_courses = {}
            for skill in missing_skills:
                recommended_courses[skill] = search_courses(skill)
 
            return render_template('results.html', show_results=True, resume_skills=resume_skills, job_description_skills=job_description_skills,
                                   matching_skills=matching_skills, missing_skills=missing_skills, recommended_courses=recommended_courses,
                                   resume_text=resume_summary, job_description_text=job_description_text)
    return render_template('analyze.html', show_form=True)
 
 
 
if __name__ == '__main__':
    app.run(debug=True, port=5002)