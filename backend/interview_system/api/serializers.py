from rest_framework import serializers
from .models import JobRole, Resume, Interview, InterviewQuestion, InterviewResponse, InterviewFeedback
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class JobRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobRole
        fields = '__all__'


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = '__all__'


class InterviewQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewQuestion
        fields = '__all__'


class InterviewResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewResponse
        fields = '__all__'


class InterviewFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewFeedback
        fields = '__all__'


class InterviewDetailSerializer(serializers.ModelSerializer):
    questions = InterviewQuestionSerializer(many=True, read_only=True)
    responses = InterviewResponseSerializer(many=True, read_only=True)
    comprehensive_feedback = InterviewFeedbackSerializer(read_only=True)
    job_role = JobRoleSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Interview
        fields = [
            'id', 'user', 'job_role', 'resume', 'status',
            'started_at', 'completed_at', 'duration_seconds',
            'overall_score', 'feedback_report', 'created_at',
            'updated_at', 'questions', 'responses', 'comprehensive_feedback'
        ]


class InterviewListSerializer(serializers.ModelSerializer):
    job_role_name = serializers.CharField(source='job_role.name', read_only=True)
    
    class Meta:
        model = Interview
        fields = [
            'id', 'job_role_name', 'status', 'started_at',
            'completed_at', 'overall_score', 'created_at'
        ]
