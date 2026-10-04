"""
AI Service for generating questions and evaluating responses using OpenAI API.
"""

import openai
import json
from decouple import config
from typing import List, Dict, Tuple

class AIService:
    """Service for AI-powered interview operations."""
    
    def __init__(self):
        """Initialize OpenAI client."""
        self.api_key = config('OPENAI_API_KEY', default='')
        if self.api_key:
            openai.api_key = self.api_key
    
    def generate_questions(self, resume_text: str, job_role: str, num_questions: int = 5) -> List[str]:
        """
        Generate interview questions based on resume and job role.
        
        Args:
            resume_text: Extracted text from resume
            job_role: Target job role
            num_questions: Number of questions to generate
        
        Returns:
            List of generated interview questions
        """
        prompt = f"""You are an experienced technical interviewer. Based on the following resume and job role, 
generate {num_questions} challenging but fair interview questions that would help assess the candidate's fit for the role.

Resume:
{resume_text}

Job Role: {job_role}

Generate questions that:
1. Are specific to skills mentioned in the resume
2. Are relevant to the job role requirements
3. Include both technical and behavioral aspects
4. Progress from easier to harder difficulty
5. Are open-ended to encourage detailed responses

Format your response as a JSON array of strings, like: ["Question 1", "Question 2", ...]
Only return the JSON array, no additional text."""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert interviewer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content
            questions = json.loads(content)
            return questions if isinstance(questions, list) else [questions]
        
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            return self._parse_questions_fallback(content)
        except Exception as e:
            print(f"Error generating questions: {str(e)}")
            return self._default_questions(job_role)
    
    def evaluate_response(self, question: str, answer: str, job_role: str) -> Dict:
        """
        Evaluate a candidate's response to an interview question.
        
        Args:
            question: The interview question
            answer: The candidate's answer
            job_role: The target job role
        
        Returns:
            Dictionary with evaluation metrics
        """
        prompt = f"""You are an expert interviewer evaluating a candidate's response. Provide a detailed evaluation.

Job Role: {job_role}
Question: {question}
Candidate's Answer: {answer}

Evaluate the response on the following aspects:
1. Relevance: How well does the answer address the question?
2. Completeness: Are key points covered?
3. Technical Depth: Does it show technical knowledge?
4. Communication: Is the answer clear and well-structured?
5. Experience Demonstration: Does it demonstrate relevant experience?

Provide your evaluation in the following JSON format:
{{
    "overall_score": <number 0-100>,
    "relevance_score": <number 0-10>,
    "completeness_score": <number 0-10>,
    "technical_depth_score": <number 0-10>,
    "communication_score": <number 0-10>,
    "experience_score": <number 0-10>,
    "strengths": ["strength 1", "strength 2", ...],
    "areas_for_improvement": ["area 1", "area 2", ...],
    "feedback": "Detailed constructive feedback",
    "follow_up_question": "Suggested follow-up question"
}}

Only return the JSON, no additional text."""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert technical interviewer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            content = response.choices[0].message.content
            evaluation = json.loads(content)
            return evaluation
        
        except json.JSONDecodeError:
            print("Error parsing evaluation JSON")
            return self._default_evaluation()
        except Exception as e:
            print(f"Error evaluating response: {str(e)}")
            return self._default_evaluation()
    
    def generate_feedback_report(self, interview_data: Dict) -> str:
        """
        Generate a comprehensive feedback report for an interview.
        
        Args:
            interview_data: Dictionary containing interview responses and evaluations
        
        Returns:
            Comprehensive feedback report
        """
        prompt = f"""Based on the following interview data, generate a comprehensive feedback report 
for the candidate that includes overall performance, key strengths, areas for improvement, and actionable recommendations.

Interview Data:
{json.dumps(interview_data, indent=2)}

Structure your response with clear sections:
1. Overall Performance Summary
2. Key Strengths
3. Areas for Improvement
4. Technical Competency Assessment
5. Behavioral Assessment
6. Recommendations for Improvement
7. Next Steps

Make the feedback constructive, specific, and actionable."""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert career coach and interviewer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2500
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            print(f"Error generating feedback report: {str(e)}")
            return "Unable to generate feedback report at this time."
    
    def generate_shortlist(self, resume_text: str, target_role: str = None) -> Dict:
        """
        Generate shortlist-style resume insights and role recommendations.
        
        Args:
            resume_text: Extracted text from the resume
            target_role: Optional target job role for more specific matching
        
        Returns:
            Dictionary with recommended roles, strengths, gaps, and summary
        """
        role_prompt = f" for the target role {target_role}" if target_role else ""
        prompt = f"""You are a career matching AI agent. Based on the following resume, provide a concise shortlist-style analysis{role_prompt}.

Resume:
{resume_text}

Return a JSON object with these keys:
- recommended_roles: [list of top 3 job titles]
- fit_summary: short paragraph summarizing why the candidate is a good match
- key_strengths: [list of 3-5 strengths]
- skill_gaps: [list of top 3 gaps or missing areas]
- recommended_next_steps: [list of concrete next actions]
- suggested_interview_focus: [list of 2-3 focus areas for interview preparation]

Only return valid JSON, no extra text."""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a career coach and hiring advisor."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1200
            )

            content = response.choices[0].message.content
            shortlist = json.loads(content)
            return shortlist if isinstance(shortlist, dict) else {
                'recommended_roles': [],
                'fit_summary': str(shortlist),
                'key_strengths': [],
                'skill_gaps': [],
                'recommended_next_steps': [],
                'suggested_interview_focus': []
            }

        except json.JSONDecodeError:
            print("Error parsing shortlist JSON")
            return {
                'recommended_roles': [],
                'fit_summary': 'Unable to generate shortlist insights at this time.',
                'key_strengths': [],
                'skill_gaps': [],
                'recommended_next_steps': [],
                'suggested_interview_focus': []
            }
        except Exception as e:
            print(f"Error generating shortlist: {str(e)}")
            return {
                'recommended_roles': [],
                'fit_summary': 'Unable to generate shortlist insights at this time.',
                'key_strengths': [],
                'skill_gaps': [],
                'recommended_next_steps': [],
                'suggested_interview_focus': []
            }

    def _parse_questions_fallback(self, text: str) -> List[str]:
        """Fallback parsing for questions if JSON parsing fails."""
        questions = []
        for line in text.split('\n'):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-')):
                clean_line = line.lstrip('0123456789.-) ')
                if clean_line:
                    questions.append(clean_line)
        return questions if questions else self._default_questions("")
    
    def _default_questions(self, job_role: str) -> List[str]:
        """Return default questions if generation fails."""
        return [
            f"Tell me about your experience with the key technologies required for this {job_role} role.",
            "Describe a challenging project you worked on and how you overcame the obstacles.",
            "How do you stay updated with the latest developments in your field?",
            f"Why are you interested in this {job_role} position?",
            "What are your long-term career goals?"
        ]
    
    def _default_evaluation(self) -> Dict:
        """Return default evaluation structure if evaluation fails."""
        return {
            "overall_score": 0,
            "relevance_score": 0,
            "completeness_score": 0,
            "technical_depth_score": 0,
            "communication_score": 0,
            "experience_score": 0,
            "strengths": [],
            "areas_for_improvement": [],
            "feedback": "Unable to evaluate at this time. Please try again.",
            "follow_up_question": ""
        }
    
    def conduct_interview_chat(self, resume_text: str, job_role: str, 
                               conversation_history: List[Dict], current_question_index: int = 0) -> Dict:
        """
        AI agent conducts interview conversation with follow-ups and adaptive questioning.
        
        Args:
            resume_text: Candidate's resume text
            job_role: Target job role
            conversation_history: List of {"role": "user|assistant", "content": "..."}
            current_question_index: Which question we're on
        
        Returns:
            Dictionary with agent's next question/response and evaluation
        """
        system_prompt = f"""You are an expert technical interviewer conducting a {job_role} interview.

Candidate Resume Summary:
{resume_text[:1000]}...

Your role:
1. Ask one focused question at a time
2. Listen to responses and evaluate them in real-time
3. Follow up on weak answers or unclear statements
4. Adapt your questioning based on the candidate's responses
5. Be conversational and professional
6. Progress from foundational to advanced topics

After the candidate responds, provide:
- Your evaluation of their answer (score 0-10, strengths, gaps)
- Your next question or follow-up
- Whether to move to the next topic

Always respond in JSON format with:
{{
    "evaluation": {{
        "score": <0-10>,
        "strengths": ["..."],
        "gaps": ["..."]
    }},
    "feedback": "Your brief feedback on their answer",
    "next_question": "Your next question",
    "is_follow_up": true/false,
    "question_number": <current_number>
}}

"""
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                system_prompt=system_prompt,
                messages=conversation_history,
                temperature=0.7,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content
            result = json.loads(content)
            return result
        
        except json.JSONDecodeError:
            return {
                "evaluation": {"score": 5, "strengths": [], "gaps": []},
                "feedback": "Thank you for that response.",
                "next_question": "Can you tell me more about your experience with this?",
                "is_follow_up": True,
                "question_number": current_question_index
            }
        except Exception as e:
            print(f"Error in interview chat: {str(e)}")
            return {
                "evaluation": {"score": 5, "strengths": [], "gaps": []},
                "feedback": "Thank you for your response.",
                "next_question": "Let's move to the next topic. Can you describe a recent project?",
                "is_follow_up": False,
                "question_number": current_question_index + 1
            }