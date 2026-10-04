from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import (
    JobRoleViewSet,
    ResumeViewSet,
    InterviewViewSet
)

router = DefaultRouter()

router.register(
    r'jobroles',
    JobRoleViewSet,
    basename='jobroles'
)

router.register(
    r'resumes',
    ResumeViewSet,
    basename='resumes'
)

router.register(
    r'interviews',
    InterviewViewSet,
    basename='interviews'
)

urlpatterns = [
    path('', include(router.urls)),
]