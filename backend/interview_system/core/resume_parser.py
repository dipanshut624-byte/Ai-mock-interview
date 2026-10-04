"""
Resume Parser for extracting information from PDF and text resumes.
"""

import PyPDF2
import re
from typing import Dict, List

class ResumeParser:
    """Parse and extract information from resumes."""
    
    @staticmethod
    def extract_text_from_pdf(pdf_file) -> str:
        """
        Extract text from a PDF resume.
        
        Args:
            pdf_file: PDF file object
        
        Returns:
            Extracted text from PDF
        """
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            print(f"Error extracting text from PDF: {str(e)}")
            return ""
    
    @staticmethod
    def extract_skills(resume_text: str) -> List[str]:
        """
        Extract technical skills from resume text.
        
        Args:
            resume_text: Full resume text
        
        Returns:
            List of identified skills
        """
        common_skills = [
            # Programming Languages
            'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'Go', 'Rust',
            'PHP', 'Ruby', 'Swift', 'Kotlin', 'SQL', 'R', 'MATLAB',
            
            # Web Technologies
            'React', 'Angular', 'Vue', 'Node.js', 'Express', 'Django', 'Flask',
            'FastAPI', 'Spring', 'ASP.NET', 'HTML', 'CSS', 'REST API', 'GraphQL',
            
            # Databases
            'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Elasticsearch',
            'Firebase', 'DynamoDB', 'Cassandra', 'Oracle', 'SQL Server',
            
            # Cloud & DevOps
            'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Jenkins', 'GitLab CI',
            'Terraform', 'CloudFormation', 'Heroku',
            
            # Tools & Platforms
            'Git', 'GitHub', 'GitLab', 'Bitbucket', 'Jira', 'Confluence',
            'Linux', 'Windows', 'macOS', 'Agile', 'Scrum', 'Kanban',
            
            # AI/ML
            'TensorFlow', 'PyTorch', 'Scikit-learn', 'Machine Learning', 'Deep Learning',
            'NLP', 'Computer Vision', 'Data Science', 'Pandas', 'NumPy',
        ]
        
        found_skills = []
        resume_lower = resume_text.lower()
        
        for skill in common_skills:
            if skill.lower() in resume_lower:
                found_skills.append(skill)
        
        return found_skills
    
    @staticmethod
    def extract_experience_years(resume_text: str) -> int:
        """
        Estimate years of experience from resume text.
        
        Args:
            resume_text: Full resume text
        
        Returns:
            Estimated years of experience
        """
        patterns = [
            r'(\d+)\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
            r'(\d+)\s*(?:years?|yrs?)\s+(?:in|of)',
        ]
        
        matches = []
        for pattern in patterns:
            found = re.findall(pattern, resume_text, re.IGNORECASE)
            matches.extend([int(m) for m in found])
        
        return max(matches) if matches else 0
    
    @staticmethod
    def extract_contact_info(resume_text: str) -> Dict:
        """
        Extract contact information from resume.
        
        Args:
            resume_text: Full resume text
        
        Returns:
            Dictionary with contact information
        """
        contact_info = {}
        
        # Email pattern
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        email_match = re.search(email_pattern, resume_text)
        if email_match:
            contact_info['email'] = email_match.group()
        
        # Phone pattern (basic)
        phone_pattern = r'(?:\+?1)?[-.\s]?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})'
        phone_match = re.search(phone_pattern, resume_text)
        if phone_match:
            contact_info['phone'] = phone_match.group()
        
        # LinkedIn pattern
        linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        linkedin_match = re.search(linkedin_pattern, resume_text, re.IGNORECASE)
        if linkedin_match:
            contact_info['linkedin'] = linkedin_match.group()
        
        # GitHub pattern
        github_pattern = r'github\.com/[\w-]+'
        github_match = re.search(github_pattern, resume_text, re.IGNORECASE)
        if github_match:
            contact_info['github'] = github_match.group()
        
        return contact_info
    
    @staticmethod
    def summarize_resume(resume_text: str) -> Dict:
        """
        Create a comprehensive summary of resume information.
        
        Args:
            resume_text: Full resume text
        
        Returns:
            Dictionary with resume summary
        """
        return {
            'skills': ResumeParser.extract_skills(resume_text),
            'experience_years': ResumeParser.extract_experience_years(resume_text),
            'contact_info': ResumeParser.extract_contact_info(resume_text),
            'full_text': resume_text,
            'text_length': len(resume_text),
        }
