"""
Utility functions for the frontend application.
"""

import requests
from typing import Dict, List, Optional

class APIClient:
    """Client for interacting with the backend API."""
    
    def __init__(self, base_url: str = 'http://localhost:8000/api'):
        self.base_url = base_url
    
    def get_job_roles(self) -> Optional[List[Dict]]:
        """Fetch all available job roles."""
        try:
            response = requests.get(f"{self.base_url}/job-roles/")
            if response.status_code == 200:
                return response.json().get('results', [])
        except Exception as e:
            print(f"Error fetching job roles: {str(e)}")
        return None
    
    def upload_resume(self, file_obj) -> Optional[Dict]:
        """Upload and parse a resume."""
        try:
            files = {'file': file_obj}
            response = requests.post(f"{self.base_url}/resumes/", files=files)
            if response.status_code == 201:
                return response.json()
        except Exception as e:
            print(f"Error uploading resume: {str(e)}")
        return None
    
    def create_interview(self, job_role_id: int, resume_id: int) -> Optional[Dict]:
        """Create a new interview session."""
        try:
            data = {
                'job_role_id': job_role_id,
                'resume_id': resume_id
            }
            response = requests.post(
                f"{self.base_url}/interviews/",
                json=data
            )
            if response.status_code == 201:
                return response.json()
        except Exception as e:
            print(f"Error creating interview: {str(e)}")
        return None
    
    def start_interview(self, interview_id: int, num_questions: int = 5) -> Optional[Dict]:
        """Start an interview and generate questions."""
        try:
            data = {'num_questions': num_questions}
            response = requests.post(
                f"{self.base_url}/interviews/{interview_id}/start_interview/",
                json=data
            )
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error starting interview: {str(e)}")
        return None
    
    def get_next_question(self, interview_id: int) -> Optional[Dict]:
        """Get the next unanswered question."""
        try:
            response = requests.get(
                f"{self.base_url}/interviews/{interview_id}/get_next_question/"
            )
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error getting next question: {str(e)}")
        return None
    
    def submit_response(
        self,
        interview_id: int,
        question_id: int,
        response_text: str,
        delivery_method: str = 'text'
    ) -> Optional[Dict]:
        """Submit a response to an interview question."""
        try:
            data = {
                'question_id': question_id,
                'response_text': response_text,
                'delivery_method': delivery_method
            }
            response = requests.post(
                f"{self.base_url}/interviews/{interview_id}/submit_response/",
                json=data
            )
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error submitting response: {str(e)}")
        return None
    
    def complete_interview(self, interview_id: int) -> Optional[Dict]:
        """Complete an interview session."""
        try:
            response = requests.post(
                f"{self.base_url}/interviews/{interview_id}/complete_interview/"
            )
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error completing interview: {str(e)}")
        return None
    
    def get_interview(self, interview_id: int) -> Optional[Dict]:
        """Fetch detailed interview information."""
        try:
            response = requests.get(
                f"{self.base_url}/interviews/{interview_id}/"
            )
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error fetching interview: {str(e)}")
        return None
    
    def get_interviews(self) -> Optional[List[Dict]]:
        """Fetch user's interview history."""
        try:
            response = requests.get(f"{self.base_url}/interviews/")
            if response.status_code == 200:
                return response.json().get('results', [])
        except Exception as e:
            print(f"Error fetching interviews: {str(e)}")
        return None
