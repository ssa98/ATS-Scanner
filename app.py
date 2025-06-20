import streamlit as st
import os
import tempfile
from ats_scanner.main import extract_text_from_file, analyze_resume

def save_uploaded_file(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
        tmp.write(uploaded_file.read())
        return tmp.name

def main():
    st.title("ATS Resume Scanner for IT Jobs")
    st.write("Upload your resume (PDF, DOCX, or TXT) and the target job description (TXT). Get a match score and improvement suggestions!")

    resume_file = st.file_uploader("Upload Resume (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"])
    job_desc_file = st.file_uploader("Upload Job Description (TXT)", type=["txt"])

    if st.button("Analyze") and resume_file and job_desc_file:
        resume_path = save_uploaded_file(resume_file)
        job_desc_path = save_uploaded_file(job_desc_file)
        resume_text = extract_text_from_file(resume_path)
        with open(job_desc_path, 'r', encoding='utf-8') as f:
            job_desc_text = f.read()
        result = analyze_resume(resume_text, job_desc_text)
        st.subheader("Match Score")
        st.progress(result['match_score'])
        st.write(f"**{result['match_score']}%**")
        st.subheader("Matched Skills")
        st.write(", ".join(result['matched_skills']) or "None")
        st.subheader("Missing Skills")
        st.write(", ".join(result['missing_skills']) or "None")
        st.subheader("Weak Skills (appear only once)")
        st.write(", ".join(result['weak_skills']) or "None")
        st.subheader("Experience Section")
        st.code(result['experience'] or "Not found", language="text")
        st.subheader("Education Section")
        st.code(result['education'] or "Not found", language="text")
        st.subheader("Certifications Section")
        st.code(result['certifications'] or "Not found", language="text")
        st.subheader("Recommendations")
        for rec in result['recommendations']:
            st.info(rec)
        os.remove(resume_path)
        os.remove(job_desc_path)

if __name__ == "__main__":
    main()
