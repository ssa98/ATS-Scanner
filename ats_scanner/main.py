import re
import os
from collections import Counter
from typing import List, Tuple, Dict
import pdfplumber
from docx import Document

# Predefined list of common IT skills (can be expanded)
IT_SKILLS = [
    'python', 'java', 'c++', 'javascript', 'sql', 'aws', 'azure', 'docker', 'kubernetes',
    'linux', 'git', 'html', 'css', 'react', 'node.js', 'agile', 'scrum', 'devops',
    'machine learning', 'data analysis', 'cloud', 'networking', 'security', 'rest api',
    'typescript', 'django', 'flask', 'spring', 'mongodb', 'postgresql', 'nosql', 'ci/cd',
    'terraform', 'ansible', 'pandas', 'numpy', 'tensorflow', 'pytorch', 'jira', 'bash',
    'shell scripting', 'php', 'ruby', 'go', 'scala', 'spark', 'hadoop', 'tableau', 'power bi'
]

def extract_skills(text: str, skills_list: List[str]) -> List[str]:
    text = text.lower()
    found = [skill for skill in skills_list if re.search(r'\\b' + re.escape(skill) + r'\\b', text)]
    return found

def extract_text_from_file(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        with pdfplumber.open(file_path) as pdf:
            return '\n'.join(page.extract_text() or '' for page in pdf.pages)
    elif ext == '.docx':
        doc = Document(file_path)
        return '\n'.join([para.text for para in doc.paragraphs])
    else:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

def extract_section(text: str, section_keywords: List[str]) -> str:
    # Simple heuristic: find section by keyword, return following lines
    lines = text.splitlines()
    for i, line in enumerate(lines):
        for keyword in section_keywords:
            if keyword.lower() in line.lower():
                return '\n'.join(lines[i:i+10])  # Return 10 lines after section header
    return ''

def extract_resume_info(text: str) -> Dict:
    skills = extract_skills(text, IT_SKILLS)
    experience = extract_section(text, ['experience', 'employment', 'work history'])
    education = extract_section(text, ['education', 'degree'])
    certifications = extract_section(text, ['certification', 'certifications'])
    return {
        'skills': skills,
        'experience': experience,
        'education': education,
        'certifications': certifications
    }

def analyze_resume(resume_text: str, job_desc_text: str) -> Dict:
    resume_info = extract_resume_info(resume_text)
    resume_skills = resume_info['skills']
    job_skills = extract_skills(job_desc_text, IT_SKILLS)
    matched_skills = list(set(resume_skills) & set(job_skills))
    missing_skills = list(set(job_skills) - set(resume_skills))
    weak_skills = [skill for skill in matched_skills if resume_text.lower().count(skill) == 1]
    score = int((len(matched_skills) / max(len(job_skills), 1)) * 100)
    recommendations = []
    if missing_skills:
        recommendations.append(f"Consider adding or emphasizing these skills: {', '.join(missing_skills)}.")
    if weak_skills:
        recommendations.append(f"Highlight these skills more: {', '.join(weak_skills)}.")
    if not resume_info['certifications']:
        recommendations.append("Add relevant certifications if you have them.")
    return {
        'match_score': score,
        'matched_skills': matched_skills,
        'missing_skills': missing_skills,
        'weak_skills': weak_skills,
        'job_skills': job_skills,
        'resume_skills': resume_skills,
        'experience': resume_info['experience'],
        'education': resume_info['education'],
        'certifications': resume_info['certifications'],
        'recommendations': recommendations
    }

def main():
    resume_path = input('Enter path to resume file (PDF, DOCX, or TXT): ')
    job_desc_path = input('Enter path to job description text file: ')
    resume_text = extract_text_from_file(resume_path)
    with open(job_desc_path, 'r', encoding='utf-8') as f:
        job_desc_text = f.read()
    result = analyze_resume(resume_text, job_desc_text)
    print(f"\n===== ATS Resume Scanner Report =====\n")
    print(f"Match Score: {result['match_score']}%\n")
    print(f"Matched Skills: {', '.join(result['matched_skills'])}")
    print(f"Missing Skills: {', '.join(result['missing_skills'])}")
    print(f"Weak Skills (appear only once): {', '.join(result['weak_skills'])}")
    print(f"\nExperience Section:\n{result['experience']}")
    print(f"\nEducation Section:\n{result['education']}")
    print(f"\nCertifications Section:\n{result['certifications']}")
    print(f"\nRecommendations:")
    for rec in result['recommendations']:
        print(f"- {rec}")

if __name__ == '__main__':
    main()
