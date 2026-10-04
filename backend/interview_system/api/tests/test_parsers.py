from django.test import TestCase
from interview_system.core.resume_parser import ResumeParser


class ResumeParserTestCase(TestCase):
    """Test cases for ResumeParser."""
    
    def test_extract_skills(self):
        """Test skill extraction."""
        resume_text = """
        Skills:
        - Python
        - JavaScript
        - Django
        - React
        - PostgreSQL
        """
        
        skills = ResumeParser.extract_skills(resume_text)
        
        self.assertIn('Python', skills)
        self.assertIn('JavaScript', skills)
        self.assertIn('Django', skills)
        self.assertIn('React', skills)
        self.assertIn('PostgreSQL', skills)
    
    def test_extract_experience_years(self):
        """Test experience extraction."""
        resume_text = """
        Professional Experience:
        - 5 years of software development experience
        - Worked as Senior Developer for 3 years
        """
        
        years = ResumeParser.extract_experience_years(resume_text)
        
        self.assertGreaterEqual(years, 3)
    
    def test_extract_contact_info(self):
        """Test contact information extraction."""
        resume_text = """
        Contact Information:
        Email: john.doe@example.com
        Phone: (123) 456-7890
        LinkedIn: linkedin.com/in/johndoe
        GitHub: github.com/johndoe
        """
        
        contact = ResumeParser.extract_contact_info(resume_text)
        
        self.assertIn('email', contact)
        self.assertIn('phone', contact)
        self.assertIn('linkedin', contact)
        self.assertIn('github', contact)
