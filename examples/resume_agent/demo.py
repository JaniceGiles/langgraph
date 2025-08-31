#!/usr/bin/env python3
"""
Resume Agent Demo

This script demonstrates the full functionality of the Resume Agent including:
- Resume creation and formatting
- Job description matching
- Keyword highlighting
- Project ranking
- Optimization recommendations
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from resume_models_simple import ContactInfo, Resume, WorkExperience, Education, Project, JobDescription
from matching_tools_simple import match_resume_with_jd, generate_resume_text, extract_keywords


def create_sample_resume():
    """Create a comprehensive sample resume."""
    contact = ContactInfo(
        name="Sarah Chen",
        email="sarah.chen@email.com",
        phone="(555) 123-4567",
        location="Seattle, WA",
        linkedin="https://linkedin.com/in/sarahchen",
        github="https://github.com/sarahchen"
    )
    
    # Work experience
    work_experience = [
        WorkExperience(
            title="Senior Full Stack Engineer",
            company="CloudTech Solutions",
            location="Seattle, WA",
            start_date="2022-01",
            end_date="Present",
            description=[
                "Led development of microservices architecture serving 1M+ users daily",
                "Implemented React.js frontend and Node.js backend with TypeScript",
                "Optimized PostgreSQL queries reducing response time by 40%",
                "Mentored 3 junior developers and conducted code reviews",
                "Deployed applications using Docker containers and Kubernetes orchestration"
            ],
            skills=["React", "Node.js", "TypeScript", "PostgreSQL", "Docker", "Kubernetes"]
        ),
        WorkExperience(
            title="Software Developer",
            company="StartupXYZ",
            location="San Francisco, CA",
            start_date="2020-06",
            end_date="2021-12",
            description=[
                "Built RESTful APIs using Python Flask and SQLAlchemy ORM",
                "Developed responsive web interfaces with React and Material-UI",
                "Integrated third-party payment systems including Stripe and PayPal",
                "Implemented automated testing with pytest and Jest frameworks",
                "Collaborated in agile development environment with daily standups"
            ],
            skills=["Python", "Flask", "React", "SQLAlchemy", "Stripe", "Jest", "pytest"]
        )
    ]
    
    # Education
    education = [
        Education(
            degree="Master of Science in Computer Science",
            institution="University of Washington",
            location="Seattle, WA",
            graduation_date="2020-05",
            gpa="3.8"
        )
    ]
    
    # Projects
    projects = [
        Project(
            title="E-Commerce Platform",
            description="Full-stack e-commerce application with real-time inventory management",
            details=[
                "Built scalable backend using Node.js, Express, and MongoDB",
                "Developed responsive React frontend with Redux state management",
                "Integrated Stripe payment processing and automated email notifications",
                "Implemented real-time chat support using Socket.io",
                "Deployed on AWS with CI/CD pipeline using GitHub Actions"
            ],
            technologies=["React", "Node.js", "MongoDB", "Redux", "Stripe", "Socket.io", "AWS"]
        ),
        Project(
            title="Machine Learning Recommender System",
            description="Collaborative filtering system for personalized product recommendations",
            details=[
                "Developed recommendation algorithms using Python and scikit-learn",
                "Processed large datasets with pandas and NumPy for feature engineering",
                "Built REST API using FastAPI with automated documentation",
                "Achieved 85% accuracy improvement over baseline random recommendations",
                "Deployed model using Docker containers on Google Cloud Platform"
            ],
            technologies=["Python", "scikit-learn", "FastAPI", "pandas", "NumPy", "Docker", "GCP"]
        ),
        Project(
            title="Real-time Analytics Dashboard",
            description="Interactive dashboard for monitoring key business metrics",
            details=[
                "Created data visualization dashboard using React and D3.js",
                "Built real-time data pipeline with Apache Kafka and Redis",
                "Implemented backend services using Python and PostgreSQL",
                "Added user authentication and role-based access control",
                "Optimized for mobile devices with responsive design"
            ],
            technologies=["React", "D3.js", "Python", "Kafka", "Redis", "PostgreSQL"]
        )
    ]
    
    resume = Resume(
        contact_info=contact,
        summary="Passionate full-stack engineer with 4+ years of experience building scalable web applications and microservices. Expertise in React, Node.js, Python, and cloud technologies. Proven track record of leading technical projects and mentoring junior developers.",
        work_experience=work_experience,
        education=education,
        projects=projects,
        skills=[
            "JavaScript", "TypeScript", "Python", "React", "Node.js", "Express.js",
            "Flask", "FastAPI", "PostgreSQL", "MongoDB", "Redis", "Docker", 
            "Kubernetes", "AWS", "GCP", "Git", "Jest", "pytest", "Agile"
        ]
    )
    
    return resume


def create_sample_job_description():
    """Create a sample job description for matching."""
    return JobDescription(
        title="Senior Software Engineer",
        company="InnovateTech Corp",
        location="San Francisco, CA / Remote",
        description="""
        We are seeking a Senior Software Engineer to join our growing engineering team. 
        You will be responsible for designing and implementing scalable web applications 
        and contributing to our microservices architecture. The ideal candidate has 
        strong experience with modern web technologies and cloud platforms.
        """,
        requirements=[
            "5+ years of software development experience",
            "Strong proficiency in JavaScript/TypeScript and Python",
            "Experience with React.js and modern frontend frameworks",
            "Backend development experience with Node.js or Python frameworks",
            "Knowledge of database systems (PostgreSQL, MongoDB, Redis)",
            "Experience with containerization (Docker) and orchestration (Kubernetes)",
            "Familiarity with cloud platforms (AWS, GCP, Azure)",
            "Understanding of microservices architecture patterns",
            "Experience with automated testing and CI/CD pipelines"
        ],
        preferred_qualifications=[
            "Experience with machine learning and data science",
            "Knowledge of message queues (Kafka, RabbitMQ)",
            "Leadership and mentoring experience",
            "Contributions to open source projects",
            "Experience with agile development methodologies"
        ],
        responsibilities=[
            "Design and develop scalable web applications and APIs",
            "Collaborate with cross-functional teams to deliver features",
            "Mentor junior developers and conduct code reviews",
            "Participate in architecture decisions and technical planning",
            "Optimize application performance and scalability",
            "Implement automated testing and deployment processes"
        ],
        keywords=[
            "JavaScript", "TypeScript", "Python", "React", "Node.js", "PostgreSQL",
            "MongoDB", "Docker", "Kubernetes", "AWS", "microservices", "APIs",
            "testing", "mentoring", "scalability"
        ]
    )


def demo_resume_creation():
    """Demonstrate resume creation and formatting."""
    print("🎯 RESUME AGENT DEMO")
    print("=" * 60)
    
    print("\n📋 Step 1: Creating Sample Resume")
    print("-" * 40)
    
    resume = create_sample_resume()
    print(f"✓ Created resume for: {resume.contact_info.name}")
    print(f"✓ Work Experience: {len(resume.work_experience)} positions")
    print(f"✓ Education: {len(resume.education)} degrees")
    print(f"✓ Projects: {len(resume.projects)} projects")
    print(f"✓ Skills: {len(resume.skills)} skills")
    
    return resume


def demo_resume_formatting(resume):
    """Demonstrate resume text generation."""
    print("\n📝 Step 2: Generating Formatted Resume")
    print("-" * 40)
    
    resume_text = generate_resume_text(resume)
    print("Generated resume text:")
    print("\n" + "="*50)
    print(resume_text)
    print("="*50)
    
    return resume_text


def demo_job_description():
    """Demonstrate job description creation."""
    print("\n💼 Step 3: Creating Job Description")
    print("-" * 40)
    
    jd = create_sample_job_description()
    print(f"✓ Job Title: {jd.title}")
    print(f"✓ Company: {jd.company}")
    print(f"✓ Requirements: {len(jd.requirements)} items")
    print(f"✓ Preferred Qualifications: {len(jd.preferred_qualifications)} items")
    print(f"✓ Keywords: {len(jd.keywords)} keywords")
    
    return jd


def demo_keyword_extraction(resume_text, jd):
    """Demonstrate keyword extraction."""
    print("\n🔍 Step 4: Keyword Extraction")
    print("-" * 40)
    
    resume_keywords = extract_keywords(resume_text)
    jd_text = f"{jd.description} {' '.join(jd.requirements)}"
    jd_keywords = extract_keywords(jd_text)
    
    print(f"✓ Resume keywords extracted: {len(resume_keywords)}")
    print(f"  Top 10: {', '.join(resume_keywords[:10])}")
    
    print(f"\n✓ Job description keywords extracted: {len(jd_keywords)}")
    print(f"  Top 10: {', '.join(jd_keywords[:10])}")
    
    return resume_keywords, jd_keywords


def demo_matching(resume, jd):
    """Demonstrate resume-JD matching."""
    print("\n🎯 Step 5: Resume-JD Matching Analysis")
    print("-" * 40)
    
    match_result = match_resume_with_jd(resume, jd)
    
    print(f"📊 Overall Match Score: {match_result.overall_score:.2%}")
    print(f"   ({'Strong' if match_result.overall_score > 0.7 else 'Good' if match_result.overall_score > 0.5 else 'Needs Improvement'} match)")
    
    print(f"\n✅ Matching Keywords ({len(match_result.matching_keywords)}):")
    print(f"   {', '.join(match_result.matching_keywords[:15])}...")
    
    print(f"\n❌ Missing Keywords ({len(match_result.missing_keywords)}):")
    print(f"   {', '.join(match_result.missing_keywords[:10])}...")
    
    print(f"\n💡 Recommendations ({len(match_result.recommendations)}):")
    for i, rec in enumerate(match_result.recommendations, 1):
        print(f"   {i}. {rec}")
    
    return match_result


def demo_project_ranking(match_result):
    """Demonstrate project ranking by relevance."""
    print("\n🚀 Step 6: Project Ranking by Relevance")
    print("-" * 40)
    
    for i, project in enumerate(match_result.ranked_projects, 1):
        score = project.relevance_score or 0.0
        print(f"{i}. {project.title}")
        print(f"   Relevance Score: {score:.2%}")
        print(f"   Technologies: {', '.join(project.technologies[:5])}...")
        print()


def demo_highlighting(match_result):
    """Demonstrate keyword highlighting."""
    print("\n✨ Step 7: Resume with Highlighted Keywords")
    print("-" * 40)
    
    # Show a portion of the highlighted resume
    highlighted = match_result.highlighted_resume
    lines = highlighted.split('\n')
    
    print("Resume with matching keywords highlighted in **bold**:")
    print("\n" + "="*50)
    
    # Show first 30 lines to keep output manageable
    for line in lines[:30]:
        if line.strip():
            print(line)
    
    if len(lines) > 30:
        print("... (truncated for demo)")
    
    print("="*50)


def demo_workflow_summary():
    """Show a summary of the workflow capabilities."""
    print("\n🔄 Step 8: Workflow Summary")
    print("-" * 40)
    
    print("The Resume Agent provides the following capabilities:")
    print("\n🎯 Interactive Resume Creation:")
    print("   • Human-in-the-loop workflow for gathering information")
    print("   • Guided prompts for contact info, experience, education, projects")
    print("   • Iterative refinement with user feedback")
    
    print("\n🔄 Resume Optimization:")
    print("   • Evaluator-optimizer pattern for continuous improvement")
    print("   • AI-powered feedback and suggestions")
    print("   • Multiple optimization iterations")
    
    print("\n🎯 Resume-JD Matching:")
    print("   • Comprehensive keyword analysis")
    print("   • Similarity scoring and gap identification")
    print("   • Project ranking by relevance")
    
    print("\n✨ Smart Features:")
    print("   • Keyword highlighting for visual feedback")
    print("   • Actionable recommendations")
    print("   • Integration with lightrag for enhanced information gathering")
    
    print("\n🔧 Technical Implementation:")
    print("   • Built with LangGraph StateGraph for workflow management")
    print("   • Pydantic models for data validation")
    print("   • Modular design for easy extension")


def main():
    """Run the complete demo."""
    try:
        # Step 1: Create sample resume
        resume = demo_resume_creation()
        
        # Step 2: Generate formatted resume
        resume_text = demo_resume_formatting(resume)
        
        # Step 3: Create job description
        jd = demo_job_description()
        
        # Step 4: Extract keywords
        resume_keywords, jd_keywords = demo_keyword_extraction(resume_text, jd)
        
        # Step 5: Perform matching
        match_result = demo_matching(resume, jd)
        
        # Step 6: Show project ranking
        demo_project_ranking(match_result)
        
        # Step 7: Show highlighting
        demo_highlighting(match_result)
        
        # Step 8: Workflow summary
        demo_workflow_summary()
        
        print("\n🎉 Demo completed successfully!")
        print("This demonstrates the core functionality of the Resume Agent.")
        print("In a full implementation, this would include:")
        print("• Interactive user prompts")
        print("• LangGraph workflow execution")
        print("• Integration with LLM models")
        print("• Persistent state management")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)