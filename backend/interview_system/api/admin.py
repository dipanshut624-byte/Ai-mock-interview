from django.contrib import admin
from .models import JobRole, Resume, Interview, InterviewQuestion, InterviewResponse, InterviewFeedback

@admin.register(JobRole)
class JobRoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'experience_level', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('experience_level', 'created_at')


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'experience_years', 'uploaded_at')
    search_fields = ('user__username', 'full_text')
    list_filter = ('uploaded_at', 'experience_years')


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'job_role', 'status', 'overall_score', 'created_at')
    search_fields = ('user__username', 'job_role__name')
    list_filter = ('status', 'created_at', 'job_role')


@admin.register(InterviewQuestion)
class InterviewQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'interview', 'question_number', 'created_at')
    search_fields = ('interview__id', 'question_text')
    list_filter = ('created_at',)


@admin.register(InterviewResponse)
class InterviewResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'interview', 'question', 'overall_score', 'evaluation_completed', 'submitted_at')
    search_fields = ('interview__id', 'question__id', 'response_text')
    list_filter = ('delivery_method', 'evaluation_completed', 'submitted_at')


@admin.register(InterviewFeedback)
class InterviewFeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'interview', 'generated_at')
    search_fields = ('interview__id',)
    list_filter = ('generated_at',)
