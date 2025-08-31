"""
Data models for resume components using Pydantic.

These models define the structure of resume data and provide validation.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import date


class ContactInfo(BaseModel):
    """Contact information for the resume."""
    name: str = Field(description="Full name")
    email: str = Field(description="Email address")
    phone: Optional[str] = Field(default=None, description="Phone number")
    location: Optional[str] = Field(default=None, description="City, State/Country")
    linkedin: Optional[str] = Field(default=None, description="LinkedIn URL")
    github: Optional[str] = Field(default=None, description="GitHub URL")
    website: Optional[str] = Field(default=None, description="Personal website URL")


class WorkExperience(BaseModel):
    """Work experience entry."""
    title: str = Field(description="Job title")
    company: str = Field(description="Company name")
    location: Optional[str] = Field(default=None, description="Work location")
    start_date: str = Field(description="Start date (YYYY-MM or 'YYYY-MM')")
    end_date: Optional[str] = Field(default=None, description="End date or 'Present'")
    description: List[str] = Field(description="List of bullet points describing responsibilities and achievements")
    skills: List[str] = Field(default=[], description="Relevant skills used in this role")


class Education(BaseModel):
    """Education entry."""
    degree: str = Field(description="Degree type and field")
    institution: str = Field(description="School/University name")
    location: Optional[str] = Field(default=None, description="School location")
    graduation_date: Optional[str] = Field(default=None, description="Graduation date")
    gpa: Optional[str] = Field(default=None, description="GPA if relevant")
    honors: List[str] = Field(default=[], description="Academic honors or achievements")


class Project(BaseModel):
    """Project entry."""
    title: str = Field(description="Project title")
    description: str = Field(description="Brief project description")
    details: List[str] = Field(description="Detailed bullet points about the project")
    technologies: List[str] = Field(description="Technologies/tools used")
    start_date: Optional[str] = Field(default=None, description="Project start date")
    end_date: Optional[str] = Field(default=None, description="Project completion date")
    url: Optional[str] = Field(default=None, description="Project URL or repository")
    relevance_score: Optional[float] = Field(default=None, description="Relevance score for JD matching")


class Certification(BaseModel):
    """Certification entry."""
    name: str = Field(description="Certification name")
    issuer: str = Field(description="Issuing organization")
    date_obtained: Optional[str] = Field(default=None, description="Date obtained")
    expiry_date: Optional[str] = Field(default=None, description="Expiry date if applicable")
    credential_id: Optional[str] = Field(default=None, description="Credential ID")


class Resume(BaseModel):
    """Complete resume structure."""
    contact_info: ContactInfo
    summary: Optional[str] = Field(default=None, description="Professional summary")
    work_experience: List[WorkExperience] = Field(default=[], description="Work experience entries")
    education: List[Education] = Field(default=[], description="Education entries")
    projects: List[Project] = Field(default=[], description="Project entries")
    skills: List[str] = Field(default=[], description="Technical and soft skills")
    certifications: List[Certification] = Field(default=[], description="Certifications")
    languages: List[str] = Field(default=[], description="Languages spoken")
    interests: List[str] = Field(default=[], description="Professional interests")


class JobDescription(BaseModel):
    """Job description structure for matching."""
    title: str = Field(description="Job title")
    company: str = Field(description="Company name")
    location: Optional[str] = Field(default=None, description="Job location")
    description: str = Field(description="Full job description")
    requirements: List[str] = Field(description="Job requirements")
    preferred_qualifications: List[str] = Field(default=[], description="Preferred qualifications")
    responsibilities: List[str] = Field(description="Job responsibilities")
    keywords: List[str] = Field(default=[], description="Important keywords for matching")


class MatchResult(BaseModel):
    """Result of matching a resume with a job description."""
    overall_score: float = Field(description="Overall matching score (0-1)")
    keyword_matches: Dict[str, bool] = Field(description="Keyword matching results")
    matching_keywords: List[str] = Field(description="Keywords that matched")
    missing_keywords: List[str] = Field(description="Important keywords not found")
    recommendations: List[str] = Field(description="Suggestions for improvement")
    ranked_projects: List[Project] = Field(description="Projects ranked by relevance")
    highlighted_resume: Optional[str] = Field(default=None, description="Resume with highlighted matching keywords")


class ResumeState(BaseModel):
    """State for the resume agent workflow."""
    current_resume: Optional[Resume] = Field(default=None, description="Current resume being worked on")
    job_description: Optional[JobDescription] = Field(default=None, description="Target job description")
    match_result: Optional[MatchResult] = Field(default=None, description="Latest matching result")
    user_input: Optional[str] = Field(default=None, description="Latest user input")
    feedback: Optional[str] = Field(default=None, description="AI feedback for improvements")
    iteration_count: int = Field(default=0, description="Number of optimization iterations")
    workflow_stage: str = Field(default="start", description="Current workflow stage")
    missing_info: List[str] = Field(default=[], description="Information still needed from user")