from django.db import models
from django.contrib.auth.models import User
import json

class JobRole(models.Model):
    """Model for job roles."""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    required_skills = models.JSONField(default=list)
    experience_level = models.CharField(
        max_length=50,
        choices=[
            ('junior', 'Junior'),
            ('mid', 'Mid-Level'),
            ('senior', 'Senior'),
            ('lead', 'Lead'),
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class Resume(models.Model):
    """Model for storing user resumes."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(upload_to='resumes/')
    full_text = models.TextField()
    skills = models.JSONField(default=list)
    experience_years = models.IntegerField(default=0)
    contact_info = models.JSONField(default=dict)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Resume - {self.user.username if self.user else 'Anonymous'}"


class Interview(models.Model):
    """Model for interview sessions."""
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('paused', 'Paused'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interviews', null=True, blank=True)
    job_role = models.ForeignKey(JobRole, on_delete=models.SET_NULL, null=True, blank=True)
    resume = models.ForeignKey(Resume, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.IntegerField(default=0)
    
    overall_score = models.FloatField(default=0.0)
    feedback_report = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Interview {self.id} - {self.job_role.name if self.job_role else 'Unknown'}"


class InterviewQuestion(models.Model):
    """Model for questions in an interview."""
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_number = models.IntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('interview', 'question_number')
    
    def __str__(self):
        return f"Q{self.question_number} - {self.interview.id}"


class InterviewResponse(models.Model):
    """Model for candidate responses to interview questions."""
    DELIVERY_CHOICES = [
        ('text', 'Text'),
        ('audio', 'Audio'),
        ('video', 'Video'),
    ]
    
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, related_name='responses')
    question = models.ForeignKey(InterviewQuestion, on_delete=models.CASCADE, related_name='responses')
    response_text = models.TextField(blank=True)
    response_audio = models.FileField(upload_to='responses/audio/', blank=True, null=True)
    response_video = models.FileField(upload_to='responses/video/', blank=True, null=True)
    delivery_method = models.CharField(max_length=20, choices=DELIVERY_CHOICES, default='text')
    
    overall_score = models.FloatField(default=0.0)
    relevance_score = models.FloatField(default=0.0)
    completeness_score = models.FloatField(default=0.0)
    technical_depth_score = models.FloatField(default=0.0)
    communication_score = models.FloatField(default=0.0)
    experience_score = models.FloatField(default=0.0)
    
    strengths = models.JSONField(default=list)
    areas_for_improvement = models.JSONField(default=list)
    feedback = models.TextField(blank=True)
    follow_up_question = models.TextField(blank=True)
    
    evaluation_completed = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)
    evaluated_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Response to Q{self.question.question_number} - Interview {self.interview.id}"


class InterviewFeedback(models.Model):
    """Model for comprehensive interview feedback."""
    interview = models.OneToOneField(Interview, on_delete=models.CASCADE, related_name='comprehensive_feedback')
    overall_performance_summary = models.TextField()
    key_strengths = models.JSONField(default=list)
    areas_for_improvement = models.JSONField(default=list)
    technical_competency_assessment = models.TextField()
    behavioral_assessment = models.TextField()
    recommendations = models.JSONField(default=list)
    next_steps = models.TextField()
    
    generated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Feedback for Interview {self.interview.id}"
