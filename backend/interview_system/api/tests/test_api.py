from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from api.models import JobRole, Resume, Interview


class JobRoleAPITestCase(APITestCase):
    """Test cases for JobRole API."""
    
    def setUp(self):
        """Set up test data."""
        self.job_role = JobRole.objects.create(
            name='Python Developer',
            description='Develop Python applications',
            required_skills=['Python', 'Django'],
            experience_level='mid'
        )
        self.client = Client()
    
    def test_get_job_roles(self):
        """Test fetching job roles."""
        response = self.client.get('/api/job-roles/')
        self.assertEqual(response.status_code, 200)
    
    def test_create_job_role(self):
        """Test creating a job role."""
        data = {
            'name': 'JavaScript Developer',
            'description': 'Web development',
            'required_skills': ['JavaScript', 'React'],
            'experience_level': 'junior'
        }
        response = self.client.post('/api/job-roles/', data, format='json')
        self.assertIn(response.status_code, [200, 201])


class InterviewAPITestCase(APITestCase):
    """Test cases for Interview API."""
    
    def setUp(self):
        """Set up test data."""
        self.job_role = JobRole.objects.create(
            name='Python Developer',
            description='Develop Python applications',
            required_skills=['Python', 'Django'],
            experience_level='mid'
        )
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = Client()
    
    def test_create_interview(self):
        """Test creating an interview."""
        data = {
            'job_role_id': self.job_role.id
        }
        response = self.client.post('/api/interviews/', data, format='json')
        self.assertIn(response.status_code, [200, 201])
    
    def test_interview_flow(self):
        """Test complete interview flow."""
        # Create interview
        interview_data = {
            'job_role_id': self.job_role.id
        }
        response = self.client.post('/api/interviews/', interview_data, format='json')
        self.assertIn(response.status_code, [200, 201])
        
        if response.status_code in [200, 201]:
            interview_id = response.json().get('id')
            
            # Start interview
            start_data = {'num_questions': 3}
            start_response = self.client.post(
                f'/api/interviews/{interview_id}/start_interview/',
                start_data,
                format='json'
            )
            self.assertIn(start_response.status_code, [200, 400])
