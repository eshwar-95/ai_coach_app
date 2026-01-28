"""Utility functions for data processing and formatting."""
import pandas as pd
from typing import List, Dict


def format_job_openings_for_prompt(jobs_df: pd.DataFrame) -> str:
    """
    Format job openings DataFrame into readable text for prompts.

    Args:
        jobs_df: DataFrame containing job openings

    Returns:
        Formatted string representation of jobs
    """
    if jobs_df.empty:
        return "No job openings currently available."

    formatted_text = "AVAILABLE JOB OPENINGS:\n" + "=" * 50 + "\n\n"

    for idx, job in jobs_df.iterrows():
        formatted_text += f"Job #{idx + 1}\n"
        formatted_text += f"Title: {job.get('title', 'N/A')}\n"
        formatted_text += f"Company: {job.get('company', 'N/A')}\n"
        formatted_text += f"Description: {job.get('description', 'N/A')}\n"
        formatted_text += f"Required Skills: {job.get('required_skills', 'N/A')}\n"
        formatted_text += f"Experience Level: {job.get('experience_level', 'N/A')}\n"
        formatted_text += f"Location: {job.get('location', 'N/A')}\n"

        if "salary" in job and pd.notna(job["salary"]):
            formatted_text += f"Salary: {job['salary']}\n"

        if "job_url" in job and pd.notna(job["job_url"]):
            formatted_text += f"Apply: {job['job_url']}\n"

        formatted_text += "\n" + "-" * 50 + "\n\n"

    return formatted_text


def calculate_skill_match_percentage(
    mentee_skills: List[str], required_skills: str
) -> float:
    """
    Calculate match percentage between mentee skills and job requirements.

    Args:
        mentee_skills: List of mentee skills
        required_skills: String of required skills (comma-separated)

    Returns:
        Match percentage (0-100)
    """
    if not mentee_skills or not required_skills:
        return 0.0

    required_list = [
        skill.strip().lower() for skill in str(required_skills).split(",")
    ]
    mentee_list = [skill.strip().lower() for skill in mentee_skills]

    if not required_list:
        return 0.0

    matches = sum(1 for req in required_list if req in mentee_list)
    return (matches / len(required_list)) * 100


def rank_jobs_by_skill_match(
    jobs_df: pd.DataFrame, mentee_skills: List[str]
) -> pd.DataFrame:
    """
    Rank job openings based on skill match with mentee profile.

    Args:
        jobs_df: DataFrame containing job openings
        mentee_skills: List of mentee skills

    Returns:
        Ranked DataFrame with match percentages
    """
    jobs_df = jobs_df.copy()
    jobs_df["skill_match_percentage"] = jobs_df["required_skills"].apply(
        lambda x: calculate_skill_match_percentage(mentee_skills, x)
    )
    return jobs_df.sort_values("skill_match_percentage", ascending=False)


def filter_jobs_by_experience_level(
    jobs_df: pd.DataFrame, mentee_age: int
) -> pd.DataFrame:
    """
    Filter jobs based on mentee experience level inferred from age.

    Args:
        jobs_df: DataFrame containing job openings
        mentee_age: Mentee's age

    Returns:
        Filtered DataFrame
    """
    # Infer experience level from age (basic heuristic)
    if mentee_age < 25:
        experience_levels = ["entry-level", "junior"]
    elif mentee_age < 35:
        experience_levels = ["junior", "mid-level"]
    else:
        experience_levels = ["mid-level", "senior", "lead"]

    filtered_df = jobs_df[
        jobs_df["experience_level"]
        .str.lower()
        .isin([level.lower() for level in experience_levels])
    ]
    return filtered_df if not filtered_df.empty else jobs_df


def get_mentee_info_dict(
    name: str,
    age: int,
    skills: List[str],
    resume_text: str = None,
    interests: str = None,
) -> Dict:
    """
    Create a standardized mentee information dictionary.

    Args:
        name: Mentee's name
        age: Mentee's age
        skills: List of skills
        resume_text: Optional resume content
        interests: Optional career interests

    Returns:
        Formatted dictionary with all mentee information
    """
    return {
        "name": name,
        "age": age,
        "skills": skills,
        "resume": resume_text,
        "interests": interests,
        "skill_count": len(skills),
        "has_resume": bool(resume_text),
    }
