"""
Simplified data models for resume components without external dependencies.

This version uses plain Python classes for demonstration when pydantic is not available.
"""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field


@dataclass
class ContactInfo:
    """Contact information for the resume."""
    name: str
    email: str
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    website: Optional[str] = None


@dataclass
class WorkExperience:
    """Work experience entry."""
    title: str
    company: str
    start_date: str
    description: List[str]
    location: Optional[str] = None
    end_date: Optional[str] = None
    skills: List[str] = field(default_factory=list)


@dataclass
class Education:
    """Education entry."""
    degree: str
    institution: str
    location: Optional[str] = None
    graduation_date: Optional[str] = None
    gpa: Optional[str] = None
    honors: List[str] = field(default_factory=list)


@dataclass
class Project:
    """Project entry."""
    title: str
    description: str
    details: List[str]
    technologies: List[str]
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    url: Optional[str] = None
    relevance_score: Optional[float] = None


@dataclass
class Certification:
    """Certification entry."""
    name: str
    issuer: str
    date_obtained: Optional[str] = None
    expiry_date: Optional[str] = None
    credential_id: Optional[str] = None


@dataclass
class Resume:
    """Complete resume structure."""
    contact_info: ContactInfo
    summary: Optional[str] = None
    work_experience: List[WorkExperience] = field(default_factory=list)
    education: List[Education] = field(default_factory=list)
    projects: List[Project] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    certifications: List[Certification] = field(default_factory=list)
    languages: List[str] = field(default_factory=list)
    interests: List[str] = field(default_factory=list)


@dataclass
class JobDescription:
    """Job description structure for matching."""
    title: str
    company: str
    description: str
    requirements: List[str]
    responsibilities: List[str]
    location: Optional[str] = None
    preferred_qualifications: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)


@dataclass
class MatchResult:
    """Result of matching a resume with a job description."""
    overall_score: float
    keyword_matches: Dict[str, bool]
    matching_keywords: List[str]
    missing_keywords: List[str]
    recommendations: List[str]
    ranked_projects: List[Project]
    highlighted_resume: Optional[str] = None


@dataclass
class ResumeState:
    """State for the resume agent workflow."""
    current_resume: Optional[Resume] = None
    job_description: Optional[JobDescription] = None
    match_result: Optional[MatchResult] = None
    user_input: Optional[str] = None
    feedback: Optional[str] = None
    iteration_count: int = 0
    workflow_stage: str = "start"
    missing_info: List[str] = field(default_factory=list)