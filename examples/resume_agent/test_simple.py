#!/usr/bin/env python3
"""
Simple test script for the Resume Agent functionality using simplified models.

This script tests the core functionality without requiring external dependencies.
"""

import sys
import os
import traceback
from dataclasses import dataclass

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_resume_models():
    """Test the resume data models."""
    print("Testing Resume Models...")
    
    try:
        from resume_models_simple import ContactInfo, Resume, WorkExperience, JobDescription
        
        # Test ContactInfo
        contact = ContactInfo(
            name="Test User",
            email="test@example.com",
            phone="123-456-7890"
        )
        assert contact.name == "Test User"
        assert contact.email == "test@example.com"
        print("✓ ContactInfo model works")
        
        # Test Resume
        resume = Resume(contact_info=contact)
        assert resume.contact_info.name == "Test User"
        print("✓ Resume model works")
        
        # Test JobDescription
        jd = JobDescription(
            title="Software Engineer",
            company="Test Company",
            description="Test job description",
            requirements=["Python", "JavaScript"],
            responsibilities=["Develop software"]
        )
        assert jd.title == "Software Engineer"
        print("✓ JobDescription model works")
        
        return True
        
    except Exception as e:
        print(f"✗ Resume models test failed: {e}")
        traceback.print_exc()
        return False


def test_matching_tools():
    """Test the matching tools functionality."""
    print("\nTesting Matching Tools...")
    
    try:
        # Import simplified matching tools
        from matching_tools_simple import extract_keywords, match_resume_with_jd, generate_resume_text
        from resume_models_simple import ContactInfo, Resume, WorkExperience, JobDescription
        
        # Test keyword extraction
        text = "Python developer with Django and Flask experience using PostgreSQL database"
        keywords = extract_keywords(text)
        assert "python" in keywords
        assert "django" in keywords
        assert "flask" in keywords
        print("✓ Keyword extraction works")
        
        # Test resume text generation
        contact = ContactInfo(name="Test User", email="test@example.com")
        resume = Resume(
            contact_info=contact,
            summary="Test summary",
            skills=["Python", "JavaScript"]
        )
        resume_text = generate_resume_text(resume)
        assert "Test User" in resume_text
        assert "Test summary" in resume_text
        print("✓ Resume text generation works")
        
        # Test matching
        jd = JobDescription(
            title="Python Developer",
            company="Test Company", 
            description="Looking for Python developer with web development experience",
            requirements=["Python programming", "Web development"],
            responsibilities=["Build web applications"],
            keywords=["python", "web", "development"]
        )
        
        match_result = match_resume_with_jd(resume, jd)
        assert match_result.overall_score >= 0.0
        assert match_result.overall_score <= 1.0
        assert isinstance(match_result.matching_keywords, list)
        assert isinstance(match_result.missing_keywords, list)
        print("✓ Resume-JD matching works")
        
        return True
        
    except Exception as e:
        print(f"✗ Matching tools test failed: {e}")
        traceback.print_exc()
        return False


def test_sample_workflow():
    """Test a sample workflow with mock data."""
    print("\nTesting Sample Workflow...")
    
    try:
        from resume_models_simple import ContactInfo, Resume, WorkExperience, Education, Project, JobDescription
        from matching_tools_simple import match_resume_with_jd, generate_resume_text
        
        # Create a more complete sample resume
        contact = ContactInfo(
            name="Jane Smith",
            email="jane.smith@email.com",
            phone="(555) 987-6543",
            location="New York, NY",
            linkedin="https://linkedin.com/in/janesmith",
            github="https://github.com/janesmith"
        )
        
        work_exp = WorkExperience(
            title="Software Developer",
            company="TechStart Inc.",
            location="New York, NY",
            start_date="2021-06",
            end_date="Present",
            description=[
                "Developed web applications using React and Node.js",
                "Implemented RESTful APIs with Express.js and MongoDB",
                "Collaborated with UX team to improve user experience",
                "Participated in code reviews and agile development processes"
            ],
            skills=["React", "Node.js", "MongoDB", "Express.js"]
        )
        
        education = Education(
            degree="Bachelor of Science in Computer Science",
            institution="State University",
            location="New York, NY",
            graduation_date="2021-05",
            gpa="3.8"
        )
        
        project = Project(
            title="E-commerce Platform",
            description="Full-stack e-commerce application with user authentication and payment processing",
            details=[
                "Built responsive frontend using React and CSS",
                "Developed backend APIs using Node.js and Express",
                "Integrated Stripe payment processing",
                "Implemented user authentication with JWT tokens"
            ],
            technologies=["React", "Node.js", "Express", "MongoDB", "Stripe", "JWT"]
        )
        
        resume = Resume(
            contact_info=contact,
            summary="Passionate software developer with 2+ years of experience building modern web applications. Skilled in full-stack development with React, Node.js, and MongoDB.",
            work_experience=[work_exp],
            education=[education],
            projects=[project],
            skills=["JavaScript", "React", "Node.js", "Express.js", "MongoDB", "HTML", "CSS", "Git", "Agile"]
        )
        
        # Create job description
        jd = JobDescription(
            title="Frontend Developer",
            company="Digital Agency",
            location="Remote",
            description="We're seeking a skilled frontend developer to join our team and create amazing user experiences.",
            requirements=[
                "3+ years experience with React",
                "Proficiency in JavaScript and modern ES6+ features",
                "Experience with responsive web design",
                "Knowledge of version control (Git)",
                "Understanding of RESTful APIs"
            ],
            preferred_qualifications=[
                "Experience with Node.js",
                "Knowledge of MongoDB or other NoSQL databases",
                "Familiarity with payment processing integration",
                "Experience with Agile development methodologies"
            ],
            responsibilities=[
                "Develop and maintain React-based web applications",
                "Collaborate with designers to implement UI/UX designs",
                "Optimize applications for maximum speed and scalability",
                "Work with backend teams to integrate APIs"
            ],
            keywords=["React", "JavaScript", "HTML", "CSS", "Git", "APIs", "responsive"]
        )
        
        # Generate resume text
        resume_text = generate_resume_text(resume)
        assert len(resume_text) > 100
        print("✓ Complete resume generated successfully")
        
        # Perform matching
        match_result = match_resume_with_jd(resume, jd)
        print(f"✓ Resume-JD matching completed (Score: {match_result.overall_score:.2%})")
        print(f"  - Matching keywords: {len(match_result.matching_keywords)}")
        print(f"  - Missing keywords: {len(match_result.missing_keywords)}")
        print(f"  - Recommendations: {len(match_result.recommendations)}")
        
        # Test project ranking
        assert len(match_result.ranked_projects) == 1
        assert match_result.ranked_projects[0].relevance_score is not None
        print("✓ Project ranking completed")
        
        # Test highlighted resume
        assert match_result.highlighted_resume is not None
        assert "**" in match_result.highlighted_resume  # Should have highlighted keywords
        print("✓ Resume highlighting completed")
        
        return True
        
    except Exception as e:
        print(f"✗ Sample workflow test failed: {e}")
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("Resume Agent Test Suite (Simplified)")
    print("=" * 50)
    
    tests = [
        test_resume_models,
        test_matching_tools,
        test_sample_workflow
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n{'=' * 50}")
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)