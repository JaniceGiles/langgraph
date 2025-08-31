"""
Simplified version of matching tools for resume-JD analysis.

This module contains functions for comparing resumes with job descriptions,
highlighting keywords, and ranking project experience without external dependencies.
"""

import re
from typing import List, Dict, Tuple, Set
from resume_models_simple import Resume, JobDescription, MatchResult, Project


def extract_keywords(text: str) -> List[str]:
    """Extract keywords from text by removing common words and punctuation."""
    # Common words to filter out
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 
        'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before', 
        'after', 'above', 'below', 'between', 'among', 'across', 'against', 'since',
        'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
        'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might',
        'must', 'can', 'shall', 'this', 'that', 'these', 'those', 'i', 'you', 'he',
        'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your',
        'his', 'her', 'its', 'our', 'their'
    }
    
    # Extract words and clean them
    words = re.findall(r'\b[a-zA-Z][a-zA-Z0-9+#.-]*\b', text.lower())
    keywords = [word for word in words if word not in stop_words and len(word) > 2]
    
    # Remove duplicates while preserving order
    unique_keywords = []
    seen = set()
    for keyword in keywords:
        if keyword not in seen:
            unique_keywords.append(keyword)
            seen.add(keyword)
    
    return unique_keywords


def calculate_keyword_similarity(keyword1: str, keyword2: str) -> float:
    """Calculate similarity between two keywords using simple string matching."""
    # Direct match
    if keyword1.lower() == keyword2.lower():
        return 1.0
    
    # Substring match
    if keyword1.lower() in keyword2.lower() or keyword2.lower() in keyword1.lower():
        return 0.8
    
    # Simple edit distance approximation
    def simple_similarity(s1, s2):
        if len(s1) == 0:
            return len(s2)
        if len(s2) == 0:
            return len(s1)
        
        # Calculate character overlap
        common_chars = len(set(s1.lower()) & set(s2.lower()))
        total_chars = len(set(s1.lower()) | set(s2.lower()))
        return common_chars / total_chars if total_chars > 0 else 0.0
    
    similarity = simple_similarity(keyword1, keyword2)
    return similarity if similarity > 0.7 else 0.0


def find_matching_keywords(resume_keywords: List[str], jd_keywords: List[str], threshold: float = 0.8) -> Tuple[List[str], Dict[str, str]]:
    """
    Find matching keywords between resume and job description.
    
    Returns:
        - List of JD keywords that have matches in resume
        - Dictionary mapping JD keywords to their closest resume matches
    """
    matches = []
    match_mapping = {}
    
    for jd_keyword in jd_keywords:
        best_match = None
        best_score = 0.0
        
        for resume_keyword in resume_keywords:
            score = calculate_keyword_similarity(jd_keyword, resume_keyword)
            if score >= threshold and score > best_score:
                best_match = resume_keyword
                best_score = score
        
        if best_match:
            matches.append(jd_keyword)
            match_mapping[jd_keyword] = best_match
    
    return matches, match_mapping


def rank_projects_by_relevance(projects: List[Project], jd_keywords: List[str]) -> List[Project]:
    """Rank projects by relevance to job description keywords."""
    ranked_projects = []
    
    for project in projects:
        # Combine all project text for analysis
        project_text = f"{project.title} {project.description} {' '.join(project.details)} {' '.join(project.technologies)}"
        project_keywords = extract_keywords(project_text)
        
        # Calculate relevance score
        matching_keywords, _ = find_matching_keywords(project_keywords, jd_keywords)
        relevance_score = len(matching_keywords) / len(jd_keywords) if jd_keywords else 0.0
        
        # Create a copy of the project with the relevance score
        # Since we're using dataclasses, we need to create a new instance
        project_copy = Project(
            title=project.title,
            description=project.description,
            details=project.details.copy(),
            technologies=project.technologies.copy(),
            start_date=project.start_date,
            end_date=project.end_date,
            url=project.url,
            relevance_score=relevance_score
        )
        ranked_projects.append(project_copy)
    
    # Sort by relevance score (highest first)
    ranked_projects.sort(key=lambda x: x.relevance_score or 0.0, reverse=True)
    return ranked_projects


def highlight_keywords_in_text(text: str, keywords_to_highlight: List[str]) -> str:
    """Highlight keywords in text using markdown bold formatting."""
    highlighted_text = text
    
    # Sort keywords by length (longest first) to avoid partial replacements
    sorted_keywords = sorted(keywords_to_highlight, key=len, reverse=True)
    
    for keyword in sorted_keywords:
        # Use word boundaries to match whole words only
        pattern = r'\b' + re.escape(keyword) + r'\b'
        highlighted_text = re.sub(pattern, f"**{keyword}**", highlighted_text, flags=re.IGNORECASE)
    
    return highlighted_text


def generate_resume_text(resume: Resume) -> str:
    """Generate a text representation of the resume."""
    sections = []
    
    # Contact Info
    contact = resume.contact_info
    sections.append(f"# {contact.name}")
    contact_details = []
    if contact.email:
        contact_details.append(contact.email)
    if contact.phone:
        contact_details.append(contact.phone)
    if contact.location:
        contact_details.append(contact.location)
    if contact_details:
        sections.append(" | ".join(contact_details))
    
    if contact.linkedin:
        sections.append(f"LinkedIn: {contact.linkedin}")
    if contact.github:
        sections.append(f"GitHub: {contact.github}")
    
    # Summary
    if resume.summary:
        sections.append(f"\n## Professional Summary\n{resume.summary}")
    
    # Work Experience
    if resume.work_experience:
        sections.append("\n## Work Experience")
        for exp in resume.work_experience:
            end_date = exp.end_date or "Present"
            sections.append(f"\n### {exp.title} | {exp.company}")
            sections.append(f"{exp.start_date} - {end_date}")
            if exp.location:
                sections.append(f"Location: {exp.location}")
            for desc in exp.description:
                sections.append(f"• {desc}")
    
    # Education
    if resume.education:
        sections.append("\n## Education")
        for edu in resume.education:
            sections.append(f"\n### {edu.degree}")
            sections.append(f"{edu.institution}")
            if edu.location:
                sections.append(f"Location: {edu.location}")
            if edu.graduation_date:
                sections.append(f"Graduation: {edu.graduation_date}")
            if edu.gpa:
                sections.append(f"GPA: {edu.gpa}")
    
    # Projects
    if resume.projects:
        sections.append("\n## Projects")
        for project in resume.projects:
            sections.append(f"\n### {project.title}")
            sections.append(project.description)
            for detail in project.details:
                sections.append(f"• {detail}")
            if project.technologies:
                sections.append(f"Technologies: {', '.join(project.technologies)}")
    
    # Skills
    if resume.skills:
        sections.append(f"\n## Skills\n{', '.join(resume.skills)}")
    
    # Certifications
    if resume.certifications:
        sections.append("\n## Certifications")
        for cert in resume.certifications:
            cert_line = f"• {cert.name} - {cert.issuer}"
            if cert.date_obtained:
                cert_line += f" ({cert.date_obtained})"
            sections.append(cert_line)
    
    return "\n".join(sections)


def match_resume_with_jd(resume: Resume, job_description: JobDescription) -> MatchResult:
    """
    Comprehensive matching of resume with job description.
    
    Returns detailed match result with scores, keyword analysis, and recommendations.
    """
    # Extract keywords from resume
    resume_text = generate_resume_text(resume)
    resume_keywords = extract_keywords(resume_text)
    
    # Extract keywords from job description
    jd_text = f"{job_description.description} {' '.join(job_description.requirements)} {' '.join(job_description.preferred_qualifications)} {' '.join(job_description.responsibilities)}"
    jd_keywords = extract_keywords(jd_text)
    
    # Add explicitly provided keywords
    if job_description.keywords:
        jd_keywords.extend(job_description.keywords)
        jd_keywords = list(set(jd_keywords))  # Remove duplicates
    
    # Find matching keywords
    matching_keywords, match_mapping = find_matching_keywords(resume_keywords, jd_keywords)
    missing_keywords = [kw for kw in jd_keywords if kw not in matching_keywords]
    
    # Calculate overall score
    overall_score = len(matching_keywords) / len(jd_keywords) if jd_keywords else 0.0
    
    # Create keyword match dictionary
    keyword_matches = {kw: kw in matching_keywords for kw in jd_keywords}
    
    # Rank projects by relevance
    ranked_projects = rank_projects_by_relevance(resume.projects, jd_keywords)
    
    # Generate highlighted resume
    highlighted_resume = highlight_keywords_in_text(resume_text, matching_keywords)
    
    # Generate recommendations
    recommendations = generate_recommendations(overall_score, missing_keywords, resume, job_description)
    
    return MatchResult(
        overall_score=overall_score,
        keyword_matches=keyword_matches,
        matching_keywords=matching_keywords,
        missing_keywords=missing_keywords[:10],  # Limit to top 10 missing keywords
        recommendations=recommendations,
        ranked_projects=ranked_projects,
        highlighted_resume=highlighted_resume
    )


def generate_recommendations(score: float, missing_keywords: List[str], resume: Resume, jd: JobDescription) -> List[str]:
    """Generate recommendations for improving resume-JD match."""
    recommendations = []
    
    if score < 0.3:
        recommendations.append("Consider significant revisions to better align with the job requirements.")
    elif score < 0.6:
        recommendations.append("Good foundation, but several improvements needed for better alignment.")
    else:
        recommendations.append("Strong match! Consider minor refinements to optimize further.")
    
    # Keyword-based recommendations
    if missing_keywords:
        top_missing = missing_keywords[:5]
        recommendations.append(f"Consider incorporating these keywords: {', '.join(top_missing)}")
    
    # Section-specific recommendations
    if not resume.summary:
        recommendations.append("Add a professional summary highlighting relevant experience.")
    
    if len(resume.projects) < 2:
        recommendations.append("Consider adding more relevant projects to demonstrate practical experience.")
    
    if not resume.certifications and any(keyword in ['certified', 'certification', 'certificate'] for keyword in extract_keywords(jd.description)):
        recommendations.append("Consider obtaining relevant certifications mentioned in the job description.")
    
    return recommendations