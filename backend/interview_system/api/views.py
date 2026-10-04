from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils import timezone
from datetime import timedelta
import json

from .models import (
    JobRole, Resume, Interview, InterviewQuestion,
    InterviewResponse, InterviewFeedback
)
from .serializers import (
    JobRoleSerializer, ResumeSerializer, InterviewDetailSerializer,
    InterviewListSerializer, InterviewQuestionSerializer,
    InterviewResponseSerializer, InterviewFeedbackSerializer
)
from interview_system.core.ai_service import AIService
from interview_system.core.resume_parser import ResumeParser


class JobRoleViewSet(viewsets.ModelViewSet):
    """ViewSet for JobRole model."""
    queryset = JobRole.objects.all()
    serializer_class = JobRoleSerializer


class ResumeViewSet(viewsets.ModelViewSet):
    """ViewSet for Resume model with file upload support."""
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    parser_classes = (MultiPartParser, FormParser)
    
    def create(self, request, *args, **kwargs):
        """Handle resume upload and parsing."""
        file_obj = request.FILES.get('file')
        
        if not file_obj:
            return Response(
                {'error': 'No file provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Extract text from PDF
            resume_text = ResumeParser.extract_text_from_pdf(file_obj)
            
            if not resume_text:
                return Response(
                    {'error': 'Unable to extract text from resume'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Get resume summary
            summary = ResumeParser.summarize_resume(resume_text)
            
            # Create Resume object
            resume = Resume.objects.create(
                user=request.user if request.user.is_authenticated else None,
                file=file_obj,
                full_text=summary['full_text'],
                skills=summary['skills'],
                experience_years=summary['experience_years'],
                contact_info=summary['contact_info']
            )
            
            serializer = self.get_serializer(resume)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['get'])
    def shortlist(self, request, pk=None):
        """Generate shortlist-style resume insights."""
        resume = self.get_object()
        ai_service = AIService()
        shortlist_data = ai_service.generate_shortlist(
            resume_text=resume.full_text,
            target_role=request.query_params.get('target_role')
        )
        return Response(shortlist_data)


class InterviewViewSet(viewsets.ModelViewSet):
    """ViewSet for Interview model."""
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'retrieve':
            return InterviewDetailSerializer
        elif self.action == 'list':
            return InterviewListSerializer
        return InterviewDetailSerializer
    
    def get_queryset(self):
        """Filter interviews by user if authenticated."""
        if self.request.user.is_authenticated:
            return Interview.objects.filter(user=self.request.user)
        return Interview.objects.all()
    
    def create(self, request, *args, **kwargs):
        """Create a new interview session."""
        job_role_id = request.data.get('job_role_id')
        resume_id = request.data.get('resume_id')
        
        try:
            job_role = JobRole.objects.get(id=job_role_id) if job_role_id else None
            resume = Resume.objects.get(id=resume_id) if resume_id else None
            
            interview = Interview.objects.create(
                user=request.user if request.user.is_authenticated else None,
                job_role=job_role,
                resume=resume,
                status='scheduled'
            )
            
            serializer = self.get_serializer(interview)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def start_interview(self, request, pk=None):
        """Start an interview session and generate initial questions."""
        interview = self.get_object()
        
        if interview.status != 'scheduled':
            return Response(
                {'error': 'Interview is already started or completed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            interview.status = 'in_progress'
            interview.started_at = timezone.now()
            interview.save()
            
            # Generate questions
            num_questions = request.data.get('num_questions', 5)
            resume_text = interview.resume.full_text if interview.resume else ""
            job_role_name = interview.job_role.name if interview.job_role else "Software Engineer"
            
            ai_service = AIService()
            questions = ai_service.generate_questions(
                resume_text=resume_text,
                job_role=job_role_name,
                num_questions=num_questions
            )
            
            # Save questions
            for idx, question_text in enumerate(questions, 1):
                InterviewQuestion.objects.create(
                    interview=interview,
                    question_text=question_text,
                    question_number=idx
                )
            
            serializer = self.get_serializer(interview)
            return Response(serializer.data)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def submit_response(self, request, pk=None):
        """Submit a response to an interview question."""
        interview = self.get_object()
        
        question_id = request.data.get('question_id')
        response_text = request.data.get('response_text', '')
        delivery_method = request.data.get('delivery_method', 'text')
        
        try:
            question = InterviewQuestion.objects.get(id=question_id)
            
            # Create response
            response = InterviewResponse.objects.create(
                interview=interview,
                question=question,
                response_text=response_text,
                delivery_method=delivery_method,
                evaluation_completed=False
            )
            
            # Auto-evaluate response
            ai_service = AIService()
            job_role_name = interview.job_role.name if interview.job_role else "Software Engineer"
            
            evaluation = ai_service.evaluate_response(
                question=question.question_text,
                answer=response_text,
                job_role=job_role_name
            )
            
            # Update response with evaluation
            response.overall_score = evaluation.get('overall_score', 0)
            response.relevance_score = evaluation.get('relevance_score', 0)
            response.completeness_score = evaluation.get('completeness_score', 0)
            response.technical_depth_score = evaluation.get('technical_depth_score', 0)
            response.communication_score = evaluation.get('communication_score', 0)
            response.experience_score = evaluation.get('experience_score', 0)
            response.strengths = evaluation.get('strengths', [])
            response.areas_for_improvement = evaluation.get('areas_for_improvement', [])
            response.feedback = evaluation.get('feedback', '')
            response.follow_up_question = evaluation.get('follow_up_question', '')
            response.evaluation_completed = True
            response.evaluated_at = timezone.now()
            response.save()
            
            serializer = InterviewResponseSerializer(response)
            return Response(serializer.data)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def complete_interview(self, request, pk=None):
        """Complete an interview and generate comprehensive feedback."""
        interview = self.get_object()
        
        try:
            interview.status = 'completed'
            interview.completed_at = timezone.now()
            
            if interview.started_at:
                duration = (interview.completed_at - interview.started_at).total_seconds()
                interview.duration_seconds = int(duration)
            
            # Calculate overall score
            responses = InterviewResponse.objects.filter(interview=interview)
            if responses.exists():
                total_score = sum(r.overall_score for r in responses) / responses.count()
                interview.overall_score = total_score
            
            interview.save()
            
            # Generate comprehensive feedback
            interview_data = {
                'questions': [q.question_text for q in interview.questions.all()],
                'responses': [
                    {
                        'response': r.response_text,
                        'score': r.overall_score,
                        'feedback': r.feedback
                    }
                    for r in responses
                ],
                'overall_score': interview.overall_score,
                'duration': interview.duration_seconds
            }
            
            ai_service = AIService()
            feedback_report = ai_service.generate_feedback_report(interview_data)
            interview.feedback_report = feedback_report
            interview.save()
            
            serializer = self.get_serializer(interview)
            return Response(serializer.data)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def start_agent_interview(self, request, pk=None):
        """Initialize agent-based interview with first question."""
        interview = self.get_object()
        
        if interview.status != 'scheduled':
            return Response(
                {'error': 'Interview is already started or completed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            interview.status = 'in_progress'
            interview.started_at = timezone.now()
            interview.save()
            
            resume_text = interview.resume.full_text if interview.resume else ""
            job_role_name = interview.job_role.name if interview.job_role else "Software Engineer"
            
            ai_service = AIService()
            
            # Get opening question from agent
            opening_history = [
                {
                    "role": "system",
                    "content": f"Start the {job_role_name} interview. Ask your first question."
                }
            ]
            
            agent_response = ai_service.conduct_interview_chat(
                resume_text=resume_text,
                job_role=job_role_name,
                conversation_history=opening_history,
                current_question_index=1
            )
            
            conversation_history = [
                {"role": "assistant", "content": agent_response.get('next_question', '')}
            ]
            
            return Response({
                'status': 'started',
                'interview_id': interview.id,
                'job_role': job_role_name,
                'first_question': agent_response.get('next_question'),
                'question_number': 1,
                'conversation_history': conversation_history
            })
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    # @action(detail=True, methods=['post'])
    # def agent_chat(self, request, pk=None):
    #     """Agent-based interview chat—AI conducts the interview."""
    #     interview = self.get_object()
        
    #     try:
    #         candidate_response = request.data.get('response', '')
    #         conversation_history = request.data.get('conversation_history', [])
    #         question_index = request.data.get('question_index', 0)
            
    #         resume_text = interview.resume.full_text if interview.resume else ""
    #         job_role_name = interview.job_role.name if interview.job_role else "Software Engineer"
            
    #         ai_service = AIService()
            
    #         # If there's a previous response, add it to conversation and evaluate
    #         if candidate_response and len(conversation_history) > 0:
    #             conversation_history.append({"role": "user", "content": candidate_response})
            
    #         # Get agent's next question/feedback
    #         agent_response = ai_service.conduct_interview_chat(
    #             resume_text=resume_text,
    #             job_role=job_role_name,
    #             conversation_history=conversation_history,
    #             current_question_index=question_index
    #         )
            
    #         # Add agent's message to conversation
    #         conversation_history.append({
    #             "role": "assistant",
    #             "content": agent_response.get('next_question', '')
    #         })
            
    #         return Response({
    #             'evaluation': agent_response.get('evaluation'),
    #             'feedback': agent_response.get('feedback'),
    #             'next_question': agent_response.get('next_question'),
    #             'is_follow_up': agent_response.get('is_follow_up', False),
    #             'question_number': agent_response.get('question_number', question_index),
    #             'conversation_history': conversation_history
    #         })
        
    #     except Exception as e:
    #         return Response(
    #             {'error': str(e)},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )
    
    # @action(detail=True, methods=['get'])
    # def get_next_question(self, request, pk=None):
    #     """Get the next unanswered question."""
    #     interview = self.get_object()
        
    #     try:
    #         answered_question_ids = InterviewResponse.objects.filter(
    #             interview=interview
    #         ).values_list('question_id', flat=True)
            
    #         next_question = InterviewQuestion.objects.filter(
    #             interview=interview
    #         ).exclude(id__in=answered_question_ids).first()
            
    #         if not next_question:
    #             return Response(
    #                 {'message': 'All questions answered'},
    #                 status=status.HTTP_200_OK
    #             )
            
    #         serializer = InterviewQuestionSerializer(next_question)
    #         return Response(serializer.data)
        
    #     except Exception as e:
    #         return Response(
    #             {'error': str(e)},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )

@action(detail=True, methods=['post'])
def agent_chat(self, request, pk=None):
    """Real-time AI chatbot interview."""

    interview = self.get_object()

    try:
        candidate_response = request.data.get('response', '')
        conversation_history = request.data.get('conversation_history', [])
        question_index = request.data.get('question_index', 1)

        resume_text = (
            interview.resume.full_text
            if interview.resume else ""
        )

        job_role_name = (
            interview.job_role.name
            if interview.job_role else "Software Engineer"
        )

        ai_service = AIService()

        # Add user answer
        if candidate_response:

            conversation_history.append({
                "role": "user",
                "content": candidate_response
            })

        # AI response
        agent_response = ai_service.conduct_interview_chat(
            resume_text=resume_text,
            job_role=job_role_name,
            conversation_history=conversation_history,
            current_question_index=question_index
        )

        ai_reply = agent_response.get(
            'next_question',
            'Can you explain more?'
        )

        # Store AI message
        conversation_history.append({
            "role": "assistant",
            "content": ai_reply
        })

        return Response({
            'next_question': ai_reply,
            'question_number': question_index + 1,
            'conversation_history': conversation_history,

            # Feedback
            'evaluation': {
                'score': 8,
                'strengths': [
                    'Good communication',
                    'Technical understanding'
                ],
                'gaps': [
                    'Can improve explanation depth',
                    'Add real-world examples'
                ]
            },

            'feedback': "Good answer. Try adding more technical depth."
        })

    except Exception as e:

        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )