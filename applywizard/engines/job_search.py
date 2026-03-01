"""
Job Search Engine: Find jobs, match compatibility, apply filters
Helps discover opportunities aligned with career goals and preferences.
"""

from datetime import datetime
import json


class JobSearchEngine:
    """Finds and matches job opportunities with user preferences."""

    # Mock job database (2026)
    MOCK_JOBS = [
        {
            "id": "JOB001",
            "title": "Senior Python Engineer",
            "company": "Stripe",
            "location": "Remote",
            "salary_min": 160000,
            "salary_max": 220000,
            "career_level": "Senior",
            "tech_stack": ["Python", "FastAPI", "AWS", "Kubernetes"],
            "remote": True,
            "posted_date": "2026-02-15"
        },
        {
            "id": "JOB002",
            "title": "Remote Python Engineer",
            "company": "Monzo",
            "location": "Remote (UK)",
            "salary_min": 120000,
            "salary_max": 160000,
            "career_level": "Mid-Level",
            "tech_stack": ["Python", "Django", "PostgreSQL", "Docker"],
            "remote": True,
            "posted_date": "2026-02-20"
        },
        {
            "id": "JOB003",
            "title": "AI/ML Engineer",
            "company": "Google",
            "location": "Mountain View, CA",
            "salary_min": 200000,
            "salary_max": 280000,
            "career_level": "Senior",
            "tech_stack": ["Python", "TensorFlow", "PyTorch", "Cloud ML"],
            "remote": False,
            "posted_date": "2026-02-18"
        },
        {
            "id": "JOB004",
            "title": "Full-Stack Python Developer",
            "company": "Notion",
            "location": "Remote",
            "salary_min": 140000,
            "salary_max": 180000,
            "career_level": "Mid-Level",
            "tech_stack": ["Python", "React", "Node.js", "PostgreSQL"],
            "remote": True,
            "posted_date": "2026-02-22"
        },
        {
            "id": "JOB005",
            "title": "Data Engineer",
            "company": "Databricks",
            "location": "Remote/SF",
            "salary_min": 180000,
            "salary_max": 240000,
            "career_level": "Senior",
            "tech_stack": ["Python", "Spark", "Scala", "Delta Lake"],
            "remote": True,
            "posted_date": "2026-02-21"
        },
    ]

    def __init__(self, db=None):
        self.db = db

    def find_jobs(self, query=None, min_salary=None, max_salary=None, remote_only=False, tech_stack=None):
        """Search for jobs matching criteria."""
        results = []

        for job in self.MOCK_JOBS:
            # Text search in title and company
            if query:
                query_lower = query.lower()
                title_match = query_lower in job["title"].lower()
                company_match = query_lower in job["company"].lower()
                if not (title_match or company_match):
                    continue

            # Salary filter
            if min_salary and job["salary_max"] < min_salary:
                continue
            if max_salary and job["salary_min"] > max_salary:
                continue

            # Remote filter
            if remote_only and not job["remote"]:
                continue

            # Tech stack filter
            if tech_stack:
                tech_lower = [t.lower() for t in tech_stack]
                job_tech_lower = [t.lower() for t in job["tech_stack"]]
                if not any(t in job_tech_lower for t in tech_lower):
                    continue

            results.append(job)

        return sorted(results, key=lambda x: x["salary_max"], reverse=True)

    def score_job_match(self, job_id, user_skills, user_career_level):
        """Score how well a job matches user profile."""
        job = next((j for j in self.MOCK_JOBS if j["id"] == job_id), None)
        if not job:
            return None

        score = 0

        # Career level match
        level_map = {
            "Junior": 1,
            "Mid-Level": 2,
            "Senior": 3,
            "Staff": 4,
            "Principal": 5
        }
        user_level = level_map.get(user_career_level, 2)
        job_level = level_map.get(job["career_level"], 2)
        level_diff = abs(user_level - job_level)
        if level_diff <= 1:
            score += 40
        elif level_diff == 2:
            score += 20

        # Tech stack match
        user_skills_lower = [s.lower() for s in user_skills]
        job_tech_lower = [t.lower() for t in job["tech_stack"]]
        matching_skills = sum(1 for skill in user_skills_lower if skill in job_tech_lower)
        tech_score = (matching_skills / len(job["tech_stack"])) * 60 if job["tech_stack"] else 0
        score += tech_score

        return {
            "job_id": job_id,
            "job_title": job["title"],
            "company": job["company"],
            "match_score": min(100, int(score)),
            "career_level_fit": "Perfect" if level_diff == 0 else "Good" if level_diff <= 1 else "Stretch",
            "skills_match": f"{matching_skills}/{len(job['tech_stack'])} skills match"
        }

    def get_job_details(self, job_id):
        """Get full details for a specific job."""
        job = next((j for j in self.MOCK_JOBS if j["id"] == job_id), None)
        if not job:
            return None

        return {
            "id": job["id"],
            "title": job["title"],
            "company": job["company"],
            "location": job["location"],
            "remote": job["remote"],
            "salary_range": f"${job['salary_min']:,} - ${job['salary_max']:,}",
            "career_level": job["career_level"],
            "tech_stack": job["tech_stack"],
            "posted_date": job["posted_date"],
            "days_posted": (datetime.strptime("2026-02-28", "%Y-%m-%d") - datetime.strptime(job["posted_date"], "%Y-%m-%d")).days
        }

    def export_search_results(self, results, format="json"):
        """Export search results in different formats."""
        if format == "json":
            return json.dumps(results, indent=2)
        elif format == "csv":
            csv_lines = ["ID,Title,Company,Location,Salary Min,Salary Max,Remote,Career Level"]
            for job in results:
                csv_lines.append(
                    f"{job['id']},{job['title']},{job['company']},{job['location']},"
                    f"${job['salary_min']},${job['salary_max']},{job['remote']},{job['career_level']}"
                )
            return "\n".join(csv_lines)
        else:
            return results
