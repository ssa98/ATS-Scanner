# ATS-Scanner
ATS-Resume-Scanner

## Architecture Overview

```mermaid
graph TD
    A[Resume (PDF/DOCX/TXT)] -->|Extract Text| B[Text Extraction Module]
    B --> C[Resume Parser]
    C --> D[Extracted Resume Info (Skills, Experience, Education, Certifications)]
    E[Job Description (TXT)] -->|Extract Text| F[Job Description Parser]
    F --> G[Required Skills/Keywords]
    D --> H[Comparison Engine]
    G --> H
    H --> I[Match Score, Matched/Missing/Weak Skills]
    I --> J[Summary Report & Recommendations]
```

**Flow Description:**
- The resume (PDF, DOCX, or TXT) is processed by the Text Extraction Module.
- The Resume Parser extracts skills, experience, education, and certifications.
- The job description is parsed for required skills and keywords.
- The Comparison Engine matches resume info with job requirements, calculates a score, and identifies gaps.
- The system outputs a summary report with actionable recommendations.
