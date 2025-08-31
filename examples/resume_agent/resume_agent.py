"""
Interactive Resume Agent using LangGraph.

This agent helps users create, review, and optimize resumes through interactive workflows.
It uses human-in-the-loop patterns for gathering information and evaluator-optimizer 
patterns for resume improvement.
"""

from typing import Dict, Any, List, Optional, TypedDict, Annotated
from langgraph.graph import StateGraph, END, START
from langgraph.types import interrupt
from langgraph.prebuilt import ToolNode
from resume_models import Resume, ResumeState, JobDescription, MatchResult, ContactInfo, WorkExperience, Education, Project
from matching_tools import match_resume_with_jd, extract_keywords, generate_resume_text
import json


class ResumeAgentState(TypedDict):
    """State for the resume agent workflow."""
    current_resume: Optional[Resume]
    job_description: Optional[JobDescription] 
    match_result: Optional[MatchResult]
    user_input: Optional[str]
    feedback: Optional[str]
    iteration_count: int
    workflow_stage: str
    missing_info: List[str]
    messages: List[Dict[str, Any]]


class ResumeAgent:
    """Interactive Resume Agent for creating, reviewing, and matching resumes."""
    
    def __init__(self):
        """Initialize the resume agent with workflow graph."""
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow for resume operations."""
        
        workflow = StateGraph(ResumeAgentState)
        
        # Add nodes for different operations
        workflow.add_node("start_session", self._start_session)
        workflow.add_node("gather_contact_info", self._gather_contact_info)
        workflow.add_node("gather_experience", self._gather_experience)
        workflow.add_node("gather_education", self._gather_education)
        workflow.add_node("gather_projects", self._gather_projects)
        workflow.add_node("gather_skills", self._gather_skills)
        workflow.add_node("review_resume", self._review_resume)
        workflow.add_node("optimize_resume", self._optimize_resume)
        workflow.add_node("match_with_jd", self._match_with_jd)
        workflow.add_node("provide_recommendations", self._provide_recommendations)
        workflow.add_node("human_feedback", self._human_feedback)
        
        # Set entry point
        workflow.set_entry_point("start_session")
        
        # Add conditional edges for workflow routing
        workflow.add_conditional_edges(
            "start_session",
            self._route_from_start,
            {
                "create_new": "gather_contact_info",
                "review_existing": "review_resume", 
                "match_jd": "match_with_jd",
                "end": END
            }
        )
        
        # Resume creation flow
        workflow.add_edge("gather_contact_info", "gather_experience")
        workflow.add_edge("gather_experience", "gather_education")
        workflow.add_edge("gather_education", "gather_projects")
        workflow.add_edge("gather_projects", "gather_skills")
        workflow.add_edge("gather_skills", "review_resume")
        
        # Review and optimization flow
        workflow.add_conditional_edges(
            "review_resume",
            self._route_from_review,
            {
                "optimize": "optimize_resume",
                "match": "match_with_jd",
                "complete": END,
                "gather_more": "human_feedback"
            }
        )
        
        workflow.add_conditional_edges(
            "optimize_resume", 
            self._route_from_optimize,
            {
                "review_again": "review_resume",
                "match": "match_with_jd", 
                "complete": END
            }
        )
        
        workflow.add_edge("match_with_jd", "provide_recommendations")
        workflow.add_conditional_edges(
            "provide_recommendations",
            self._route_from_recommendations,
            {
                "optimize_more": "optimize_resume",
                "complete": END,
                "new_jd": "match_with_jd"
            }
        )
        
        workflow.add_conditional_edges(
            "human_feedback",
            self._route_from_feedback,
            {
                "continue_creation": "gather_contact_info",
                "review": "review_resume",
                "match": "match_with_jd",
                "complete": END
            }
        )
        
        return workflow.compile()
    
    def _start_session(self, state: ResumeAgentState) -> ResumeAgentState:
        """Start a new resume session and determine user intent."""
        
        welcome_message = """
        Welcome to the Interactive Resume Agent! 🎯
        
        I can help you:
        1. Create a new resume from scratch
        2. Review and optimize an existing resume
        3. Match your resume with a job description
        
        What would you like to do today?
        """
        
        user_choice = interrupt({
            "message": welcome_message,
            "options": ["create_new", "review_existing", "match_jd", "exit"]
        })
        
        return {
            **state,
            "workflow_stage": "start",
            "user_input": user_choice.get("choice", "create_new"),
            "messages": [{"role": "assistant", "content": welcome_message}]
        }
    
    def _gather_contact_info(self, state: ResumeAgentState) -> ResumeAgentState:
        """Gather contact information from user."""
        
        contact_prompt = """
        Let's start with your contact information. Please provide:
        
        1. Full Name: (required)
        2. Email: (required) 
        3. Phone: (optional)
        4. Location: (City, State/Country)
        5. LinkedIn URL: (optional)
        6. GitHub URL: (optional)
        7. Personal Website: (optional)
        
        You can provide this information in any format.
        """
        
        user_response = interrupt({
            "message": contact_prompt,
            "type": "contact_info"
        })
        
        # Parse contact information (simplified parsing)
        contact_data = self._parse_contact_info(user_response.get("data", ""))
        
        contact_info = ContactInfo(**contact_data)
        
        resume = Resume(contact_info=contact_info)
        
        return {
            **state,
            "current_resume": resume,
            "workflow_stage": "contact_gathered",
            "user_input": user_response.get("data"),
            "messages": state["messages"] + [
                {"role": "assistant", "content": contact_prompt},
                {"role": "user", "content": user_response.get("data", "")}
            ]
        }
    
    def _gather_experience(self, state: ResumeAgentState) -> ResumeAgentState:
        """Gather work experience information."""
        
        experience_prompt = """
        Now let's add your work experience. For each job, please provide:
        
        1. Job Title
        2. Company Name
        3. Location (optional)
        4. Start Date (YYYY-MM format)
        5. End Date (YYYY-MM or "Present")
        6. Job Description (bullet points of achievements and responsibilities)
        7. Relevant Skills Used
        
        Start with your most recent position. Type "done" when finished.
        """
        
        experiences = []
        while True:
            user_response = interrupt({
                "message": experience_prompt,
                "type": "work_experience"
            })
            
            if user_response.get("data", "").lower().strip() == "done":
                break
                
            # Parse work experience (simplified)
            exp_data = self._parse_work_experience(user_response.get("data", ""))
            if exp_data:
                experiences.append(WorkExperience(**exp_data))
            
            experience_prompt = "Add another work experience or type 'done' to continue:"
        
        # Update resume with work experience
        resume = state["current_resume"]
        if resume:
            resume.work_experience = experiences
        
        return {
            **state,
            "current_resume": resume,
            "workflow_stage": "experience_gathered"
        }
    
    def _gather_education(self, state: ResumeAgentState) -> ResumeAgentState:
        """Gather education information."""
        
        education_prompt = """
        Let's add your education. For each degree, provide:
        
        1. Degree (e.g., "Bachelor of Science in Computer Science")
        2. Institution Name
        3. Location (optional)
        4. Graduation Date (optional)
        5. GPA (if relevant)
        6. Honors or achievements (optional)
        
        Type "done" when finished.
        """
        
        education_list = []
        while True:
            user_response = interrupt({
                "message": education_prompt,
                "type": "education"
            })
            
            if user_response.get("data", "").lower().strip() == "done":
                break
            
            # Parse education (simplified)
            edu_data = self._parse_education(user_response.get("data", ""))
            if edu_data:
                education_list.append(Education(**edu_data))
                
            education_prompt = "Add another education entry or type 'done' to continue:"
        
        # Update resume
        resume = state["current_resume"]
        if resume:
            resume.education = education_list
        
        return {
            **state,
            "current_resume": resume,
            "workflow_stage": "education_gathered"
        }
    
    def _gather_projects(self, state: ResumeAgentState) -> ResumeAgentState:
        """Gather project information."""
        
        projects_prompt = """
        Let's add your projects. For each project, provide:
        
        1. Project Title
        2. Brief Description
        3. Detailed bullet points about what you accomplished
        4. Technologies/tools used
        5. Start/End dates (optional)
        6. Project URL or repository (optional)
        
        Type "done" when finished.
        """
        
        projects = []
        while True:
            user_response = interrupt({
                "message": projects_prompt,
                "type": "projects"
            })
            
            if user_response.get("data", "").lower().strip() == "done":
                break
            
            # Parse project (simplified)
            project_data = self._parse_project(user_response.get("data", ""))
            if project_data:
                projects.append(Project(**project_data))
                
            projects_prompt = "Add another project or type 'done' to continue:"
        
        # Update resume
        resume = state["current_resume"]
        if resume:
            resume.projects = projects
        
        return {
            **state,
            "current_resume": resume,
            "workflow_stage": "projects_gathered"
        }
    
    def _gather_skills(self, state: ResumeAgentState) -> ResumeAgentState:
        """Gather skills information."""
        
        skills_prompt = """
        Finally, let's add your skills. Please list:
        
        1. Technical skills (programming languages, tools, frameworks)
        2. Soft skills (communication, leadership, etc.)
        3. Languages spoken (optional)
        4. Certifications (optional)
        
        Separate skills with commas.
        """
        
        user_response = interrupt({
            "message": skills_prompt,
            "type": "skills"
        })
        
        # Parse skills
        skills_data = self._parse_skills(user_response.get("data", ""))
        
        # Update resume
        resume = state["current_resume"]
        if resume:
            resume.skills = skills_data.get("skills", [])
            resume.languages = skills_data.get("languages", [])
            # Note: certifications would be parsed and added here
        
        return {
            **state,
            "current_resume": resume,
            "workflow_stage": "skills_gathered"
        }
    
    def _review_resume(self, state: ResumeAgentState) -> ResumeAgentState:
        """Review the current resume and provide feedback."""
        
        resume = state["current_resume"]
        if not resume:
            return {**state, "feedback": "No resume found to review."}
        
        # Generate resume text for review
        resume_text = generate_resume_text(resume)
        
        review_message = f"""
        Here's your current resume:
        
        {resume_text}
        
        Would you like to:
        1. Optimize this resume
        2. Match it with a job description
        3. Make manual edits
        4. Complete and finish
        """
        
        user_choice = interrupt({
            "message": review_message,
            "options": ["optimize", "match", "edit", "complete"]
        })
        
        return {
            **state,
            "workflow_stage": "review_complete",
            "user_input": user_choice.get("choice", "complete"),
            "feedback": "Resume reviewed successfully."
        }
    
    def _optimize_resume(self, state: ResumeAgentState) -> ResumeAgentState:
        """Optimize resume using AI feedback (evaluator-optimizer pattern)."""
        
        resume = state["current_resume"]
        if not resume:
            return {**state, "feedback": "No resume to optimize."}
        
        # Generate optimization feedback
        feedback = self._generate_optimization_feedback(resume)
        
        optimization_message = f"""
        Here's my analysis and suggestions for improving your resume:
        
        {feedback}
        
        Would you like to:
        1. Apply these suggestions automatically
        2. Review suggestions manually
        3. See the updated resume
        4. Match with job description
        """
        
        user_choice = interrupt({
            "message": optimization_message,
            "options": ["auto_apply", "manual_review", "show_updated", "match"]
        })
        
        return {
            **state,
            "workflow_stage": "optimization_complete",
            "feedback": feedback,
            "user_input": user_choice.get("choice", "manual_review"),
            "iteration_count": state["iteration_count"] + 1
        }
    
    def _match_with_jd(self, state: ResumeAgentState) -> ResumeAgentState:
        """Match resume with job description."""
        
        if not state["job_description"]:
            jd_prompt = """
            Please provide the job description you'd like to match your resume against.
            Include the full job posting with requirements, responsibilities, and qualifications.
            """
            
            user_response = interrupt({
                "message": jd_prompt,
                "type": "job_description"
            })
            
            jd_data = self._parse_job_description(user_response.get("data", ""))
            job_description = JobDescription(**jd_data)
        else:
            job_description = state["job_description"]
        
        # Perform matching
        resume = state["current_resume"]
        if resume and job_description:
            match_result = match_resume_with_jd(resume, job_description)
        else:
            match_result = None
        
        return {
            **state,
            "job_description": job_description,
            "match_result": match_result,
            "workflow_stage": "matching_complete"
        }
    
    def _provide_recommendations(self, state: ResumeAgentState) -> ResumeAgentState:
        """Provide recommendations based on matching results."""
        
        match_result = state["match_result"]
        if not match_result:
            return {**state, "feedback": "No matching results available."}
        
        recommendations_message = f"""
        Resume-Job Description Match Results:
        
        Overall Match Score: {match_result.overall_score:.2%}
        
        Matching Keywords: {', '.join(match_result.matching_keywords[:10])}
        
        Missing Keywords: {', '.join(match_result.missing_keywords[:10])}
        
        Recommendations:
        {chr(10).join(f"• {rec}" for rec in match_result.recommendations)}
        
        Top Ranked Projects:
        {chr(10).join(f"• {p.title} (Score: {p.relevance_score:.2f})" for p in match_result.ranked_projects[:3])}
        
        Would you like to:
        1. Optimize resume based on these insights
        2. Try a different job description
        3. See the highlighted resume
        4. Complete the session
        """
        
        user_choice = interrupt({
            "message": recommendations_message,
            "options": ["optimize", "new_jd", "highlight", "complete"]
        })
        
        return {
            **state,
            "workflow_stage": "recommendations_provided",
            "user_input": user_choice.get("choice", "complete"),
            "feedback": recommendations_message
        }
    
    def _human_feedback(self, state: ResumeAgentState) -> ResumeAgentState:
        """Handle human feedback and determine next steps."""
        
        feedback_prompt = """
        I need more information from you. What would you like to do?
        
        1. Continue building the resume
        2. Review what we have so far
        3. Match with a job description
        4. Provide additional information
        """
        
        user_response = interrupt({
            "message": feedback_prompt,
            "type": "feedback"
        })
        
        return {
            **state,
            "user_input": user_response.get("choice", "continue"),
            "workflow_stage": "feedback_received"
        }
    
    # Routing functions
    def _route_from_start(self, state: ResumeAgentState) -> str:
        """Route based on initial user choice."""
        choice = state.get("user_input", "").lower()
        if "create" in choice or "new" in choice:
            return "create_new"
        elif "review" in choice or "existing" in choice:
            return "review_existing"
        elif "match" in choice or "jd" in choice:
            return "match_jd"
        else:
            return "end"
    
    def _route_from_review(self, state: ResumeAgentState) -> str:
        """Route from review based on user choice."""
        choice = state.get("user_input", "").lower()
        if "optimize" in choice:
            return "optimize"
        elif "match" in choice:
            return "match"
        elif "edit" in choice:
            return "gather_more"
        else:
            return "complete"
    
    def _route_from_optimize(self, state: ResumeAgentState) -> str:
        """Route from optimization based on iteration count and user choice."""
        choice = state.get("user_input", "").lower()
        if "match" in choice:
            return "match"
        elif state["iteration_count"] < 3 and "review" in choice:
            return "review_again"
        else:
            return "complete"
    
    def _route_from_recommendations(self, state: ResumeAgentState) -> str:
        """Route from recommendations based on user choice."""
        choice = state.get("user_input", "").lower()
        if "optimize" in choice:
            return "optimize_more"
        elif "new" in choice or "jd" in choice:
            return "new_jd"
        else:
            return "complete"
    
    def _route_from_feedback(self, state: ResumeAgentState) -> str:
        """Route from human feedback."""
        choice = state.get("user_input", "").lower()
        if "continue" in choice:
            return "continue_creation"
        elif "review" in choice:
            return "review"
        elif "match" in choice:
            return "match"
        else:
            return "complete"
    
    # Helper parsing functions (simplified implementations)
    def _parse_contact_info(self, text: str) -> Dict[str, Any]:
        """Parse contact information from user text."""
        # Simplified parsing - in production, use more sophisticated NLP
        lines = text.strip().split('\n')
        contact_data = {"name": "User", "email": "user@example.com"}
        
        for line in lines:
            line = line.strip()
            if '@' in line and 'email' not in contact_data:
                contact_data["email"] = line
            elif line and not contact_data.get("name"):
                contact_data["name"] = line
                
        return contact_data
    
    def _parse_work_experience(self, text: str) -> Optional[Dict[str, Any]]:
        """Parse work experience from user text."""
        if not text.strip():
            return None
            
        return {
            "title": "Software Engineer",
            "company": "Tech Company",
            "start_date": "2022-01",
            "end_date": "Present",
            "description": [text.strip()],
            "skills": []
        }
    
    def _parse_education(self, text: str) -> Optional[Dict[str, Any]]:
        """Parse education from user text."""
        if not text.strip():
            return None
            
        return {
            "degree": text.strip(),
            "institution": "University",
            "honors": []
        }
    
    def _parse_project(self, text: str) -> Optional[Dict[str, Any]]:
        """Parse project from user text."""
        if not text.strip():
            return None
            
        return {
            "title": "Project",
            "description": text.strip(),
            "details": [text.strip()],
            "technologies": []
        }
    
    def _parse_skills(self, text: str) -> Dict[str, List[str]]:
        """Parse skills from user text."""
        skills = [skill.strip() for skill in text.split(',') if skill.strip()]
        return {"skills": skills, "languages": []}
    
    def _parse_job_description(self, text: str) -> Dict[str, Any]:
        """Parse job description from user text."""
        return {
            "title": "Software Engineer",
            "company": "Company",
            "description": text,
            "requirements": [text],
            "responsibilities": [text],
            "keywords": extract_keywords(text)
        }
    
    def _generate_optimization_feedback(self, resume: Resume) -> str:
        """Generate feedback for resume optimization."""
        feedback_points = []
        
        if not resume.summary:
            feedback_points.append("Consider adding a professional summary to highlight your key qualifications.")
        
        if len(resume.work_experience) == 0:
            feedback_points.append("Add work experience to demonstrate your professional background.")
        
        if len(resume.projects) < 2:
            feedback_points.append("Include more projects to showcase your practical skills.")
        
        if len(resume.skills) < 5:
            feedback_points.append("Expand your skills section with relevant technical and soft skills.")
        
        return "\n".join(f"• {point}" for point in feedback_points) if feedback_points else "Your resume looks good! Consider matching it with a job description for targeted improvements."


# Example usage function
def create_resume_agent_example():
    """Example of how to use the Resume Agent."""
    agent = ResumeAgent()
    
    # Start the interactive session
    initial_state = ResumeAgentState(
        current_resume=None,
        job_description=None,
        match_result=None,
        user_input=None,
        feedback=None,
        iteration_count=0,
        workflow_stage="start",
        missing_info=[],
        messages=[]
    )
    
    # Run the agent
    result = agent.graph.invoke(initial_state)
    return result


if __name__ == "__main__":
    # Example usage
    print("Resume Agent Example")
    print("This would start an interactive resume building session.")
    print("In a real implementation, this would use the LangGraph workflow.")