from django.core.management.base import BaseCommand
from api.models import JobRole


class Command(BaseCommand):
    help = 'Load sample job roles into the database'
    
    def handle(self, *args, **options):
        """Load sample job roles."""
        
        job_roles = [
            {
                'name': 'Senior Python Developer',
                'description': 'Looking for an experienced Python developer with expertise in web applications, APIs, and data processing.',
                'required_skills': ['Python', 'Django', 'REST API', 'PostgreSQL', 'Docker'],
                'experience_level': 'senior'
            },
            {
                'name': 'Frontend Engineer',
                'description': 'Join our team to build amazing user interfaces using modern JavaScript frameworks.',
                'required_skills': ['JavaScript', 'React', 'HTML', 'CSS', 'REST API', 'Git'],
                'experience_level': 'mid'
            },
            {
                'name': 'Full Stack Developer',
                'description': 'Develop end-to-end solutions with proficiency in both frontend and backend technologies.',
                'required_skills': ['JavaScript', 'React', 'Node.js', 'MongoDB', 'REST API'],
                'experience_level': 'mid'
            },
            {
                'name': 'Data Scientist',
                'description': 'Build machine learning models and analyze complex data to drive business insights.',
                'required_skills': ['Python', 'Machine Learning', 'Data Analysis', 'SQL', 'TensorFlow', 'Pandas'],
                'experience_level': 'senior'
            },
            {
                'name': 'DevOps Engineer',
                'description': 'Design and maintain cloud infrastructure and deployment pipelines.',
                'required_skills': ['Docker', 'Kubernetes', 'AWS', 'Linux', 'CI/CD', 'Terraform'],
                'experience_level': 'mid'
            },
            {
                'name': 'Mobile App Developer',
                'description': 'Create engaging mobile applications for iOS and Android platforms.',
                'required_skills': ['Swift', 'Kotlin', 'React Native', 'Git', 'REST API'],
                'experience_level': 'mid'
            },
            {
                'name': 'Junior Web Developer',
                'description': 'Start your career as a web developer with guidance and mentorship.',
                'required_skills': ['HTML', 'CSS', 'JavaScript', 'Git', 'Basics of Database'],
                'experience_level': 'junior'
            },
            {
                'name': 'Database Administrator',
                'description': 'Manage and optimize database systems for performance and reliability.',
                'required_skills': ['SQL', 'PostgreSQL', 'MySQL', 'Database Design', 'Backup & Recovery'],
                'experience_level': 'mid'
            },
            {
                'name': 'Cloud Architect',
                'description': 'Design scalable cloud solutions on AWS, Azure, or GCP.',
                'required_skills': ['AWS', 'Azure', 'GCP', 'Microservices', 'Kubernetes', 'Security'],
                'experience_level': 'senior'
            },
            {
                'name': 'Software Architect',
                'description': 'Lead technical design and architecture decisions for enterprise applications.',
                'required_skills': ['System Design', 'Microservices', 'Design Patterns', 'Leadership'],
                'experience_level': 'lead'
            },
        ]
        
        for role_data in job_roles:
            job_role, created = JobRole.objects.get_or_create(
                name=role_data['name'],
                defaults={
                    'description': role_data['description'],
                    'required_skills': role_data['required_skills'],
                    'experience_level': role_data['experience_level'],
                }
            )
            
            status = "Created" if created else "Already exists"
            self.stdout.write(
                self.style.SUCCESS(f'{status}: {job_role.name}')
            )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully loaded sample job roles!')
        )
