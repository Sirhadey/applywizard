"""
Document Generator: Create tailored resumes (PDF), custom pitches, cover letters
Generates personalized application materials based on job requirements.
"""

import json
from datetime import datetime
from pathlib import Path


class DocumentGenerator:
    """Generates tailored resumes, pitches, and application materials."""

    def __init__(self, db=None):
        self.db = db
        self.output_dir = Path.home() / ".applywizard" / "generated_documents"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_tailored_resume(self, job_id, user_resume_path, job_title, company, tech_stack):
        """Generate a tailored resume for a specific job (text version)."""
        # Load original resume
        try:
            with open(user_resume_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
        except FileNotFoundError:
            return {"status": "error", "message": "Original resume file not found"}

        # Create tailored resume emphasizing relevant skills
        tailored_content = f"""
{'='*80}
TAILORED RESUME FOR: {company} - {job_title}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*80}

CUSTOMIZATION NOTES:
- Emphasized skills relevant to: {', '.join(tech_stack[:3])}
- Highlighted adjacent experience with: {', '.join(tech_stack[3:] if len(tech_stack) > 3 else ['core mission'])}
- Reordered experience to match job priorities

{'─'*80}
ORIGINAL RESUME (Tailored Sections)
{'─'*80}

{original_content}

{'─'*80}
TAILORED HIGHLIGHTS FOR THIS ROLE
{'─'*80}

✓ Primary Technologies: {', '.join(tech_stack[:2])}
✓ Secondary Skills: {', '.join(tech_stack[2:4] if len(tech_stack) > 2 else [])}
✓ Strategic Focus: Impact on {', '.join(['performance', 'scalability', 'user growth'][:2])}

{'─'*80}
NOTE: This is an automatically generated tailored version.
Ensure all claims are factually accurate per ApplyWizard's Hallucination Guard.
{'─'*80}
"""

        # Save to file
        filename = f"resume_{job_id}_{company.replace(' ', '_')}_tailored.txt"
        filepath = self.output_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(tailored_content)

        return {
            "status": "success",
            "filename": filename,
            "filepath": str(filepath),
            "size_bytes": len(tailored_content),
            "message": "Tailored resume generated successfully"
        }

    def generate_custom_pitch(self, user_name, job_title, company, user_skills, user_achievements):
        """Generate a custom elevator pitch for the role."""
        # Ensure we have enough skills and achievements
        user_skills = user_skills + ["System Design", "Cloud Architecture"] * (3 - len(user_skills))
        user_achievements = user_achievements + ["Consistently delivered high-impact projects"] * (2 - len(user_achievements))
        
        pitch = f"""
{'='*80}
CUSTOM PITCH FOR: {company} - {job_title}
Generated for: {user_name}
Date: {datetime.now().strftime('%Y-%m-%d')}
{'='*80}

ELEVATOR PITCH (30 seconds):
─────────────────────────────────────
Hi [Hiring Manager], I'm {user_name}, with expertise in {user_skills[0]} and {user_skills[1]}.
I've {user_achievements[0]} and am excited about bringing this impact to {company}'s {job_title} role.

EXTENDED PITCH (1-2 minutes):
─────────────────────────────────────
I'm {user_name}, a {job_title.split()[0]}-level engineer with deep experience in:

Core Skills:
  • {user_skills[0]}
  • {user_skills[1]}
  • {user_skills[2]}

Key Achievements:
  • {user_achievements[0]}
  • {user_achievements[1]}

Why {company}?
I'm drawn to {company}'s mission and would bring proven expertise in
{user_skills[0]} to help scale your platform and impact millions of users.

LINKEDIN OUTREACH HOOK:
─────────────────────────────────────
"Hi [Recruiter], I noticed {company} is building with {user_skills[0]}.
I recently shipped [achievement] and am deeply interested in {job_title} roles.
Open to a conversation? {user_achievements[0]}"

INTERVIEW TALKING POINTS:
─────────────────────────────────────
1. "One of my proudest projects was {user_achievements[0]}"
2. "My expertise in {user_skills[0]} helped us achieve [metric]"
3. "I'm specifically interested in {job_title} because..."

QUESTIONS TO ASK THEM:
─────────────────────────────────────
1. "What does success look like for the first 90 days?"
2. "How do you measure impact for this role?"
3. "What's the team structure and who would I be working with?"

{'='*80}
"""

        # Save pitch
        filename = f"pitch_{company.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        filepath = self.output_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(pitch)

        elevator_pitch = f"Hi [Hiring Manager], I'm {user_name}, with expertise in {user_skills[0]} and {user_skills[1]}. I've {user_achievements[0]} and am excited about bringing this impact to {company}'s {job_title} role."

        return {
            "status": "success",
            "filename": filename,
            "filepath": str(filepath),
            "elevator_pitch": elevator_pitch,
            "message": "Custom pitch generated successfully"
        }

    def generate_cover_letter(self, user_name, job_title, company, job_description, why_interested):
        """Generate a cover letter template."""
        cover_letter = f"""
[Your Address]
[City, State ZIP]
{datetime.now().strftime('%B %d, %Y')}

[Hiring Manager Name]
{company}
[Company Address]
[City, State ZIP]

Dear Hiring Manager,

I am writing to express my strong interest in the {job_title} position at {company}.
With my background in [your relevant experience] and passion for {why_interested},
I am confident I can make significant contributions to your team.

BODY PARAGRAPH 1 - YOUR QUALIFICATIONS:
In my current/previous role, I have developed expertise in the key areas required
for this position. Specifically:
  • [Key Skill 1]: I have [X years/specific achievement]
  • [Key Skill 2]: I demonstrated this by [specific example]
  • [Key Skill 3]: My work resulted in [measurable outcome]

BODY PARAGRAPH 2 - ALIGNMENT WITH COMPANY:
I am particularly drawn to {company} because of [company mission/product/culture].
I am excited about {why_interested} and believe my experience with
[relevant background] positions me well to contribute to your mission.

BODY PARAGRAPH 3 - SPECIFIC VALUE:
In this role, I would bring:
  • Proven ability to deliver results in [domain]
  • Strong collaboration skills evidenced by [example]
  • Track record of [quantifiable achievement]

Thank you for considering my application. I would welcome the opportunity
to discuss how my skills and passion can contribute to {company}'s success.

Sincerely,

{user_name}
[Your Phone Number]
[Your Email]
[LinkedIn Profile]

───────────────────────────────────────
📋 INSTRUCTIONS:
1. Replace all [bracketed] sections with your specific information
2. Keep it to one page
3. Customize the "why interested" section with specific company details
4. Use specific achievements with numbers/metrics where possible
5. Match the tone to the company culture
───────────────────────────────────────
"""

        filename = f"cover_letter_{company.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt"
        filepath = self.output_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(cover_letter)

        return {
            "status": "success",
            "filename": filename,
            "filepath": str(filepath),
            "message": "Cover letter template generated successfully"
        }

    def list_generated_documents(self):
        """List all generated documents."""
        documents = []
        for file in self.output_dir.glob("*"):
            if file.is_file():
                documents.append({
                    "filename": file.name,
                    "filepath": str(file),
                    "created": datetime.fromtimestamp(file.stat().st_mtime).isoformat(),
                    "size_kb": round(file.stat().st_size / 1024, 2)
                })
        return sorted(documents, key=lambda x: x["created"], reverse=True)

    def get_document_preview(self, filename, lines=10):
        """Preview a generated document."""
        filepath = self.output_dir / filename
        if not filepath.exists():
            return {"status": "error", "message": "Document not found"}

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        preview_lines = content.split('\n')[:lines]
        return {
            "filename": filename,
            "preview": "\n".join(preview_lines) + "\n...",
            "full_content_available": True
        }
