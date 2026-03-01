"""
Database Module: Local SQLite with AES-256 Encrypted Backups
Manages all persistent data storage for CareerPath, Applications, and Analytics.
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime
from applywizard.core.security import SecurityManager


class Database:
    """SQLite database with encryption support for user career data."""

    def __init__(self, db_path=None, security_manager=None):
        self.db_path = db_path or Path.home() / ".applywizard" / "careerdata.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.security = security_manager or SecurityManager()
        self.connection = None
        self.init_database()

    def get_connection(self):
        """Get or create database connection."""
        if not self.connection:
            self.connection = sqlite3.connect(str(self.db_path))
            self.connection.row_factory = sqlite3.Row
        return self.connection

    def init_database(self):
        """Initialize database schema."""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Users & Career Profile
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS career_profile (
                id INTEGER PRIMARY KEY,
                user_name TEXT UNIQUE,
                current_role TEXT,
                current_company TEXT,
                skills TEXT,  -- JSON array
                experience_years INTEGER,
                target_roles TEXT,  -- JSON array
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Applications Tracking
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY,
                company TEXT,
                role TEXT,
                compatibility_score INTEGER,
                resume_persona TEXT,
                status TEXT,  -- 'submitted', 'responded', 'interviewing', 'rejected', 'offered'
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                response_at TIMESTAMP,
                url TEXT,
                notes TEXT
            )
        """)

        # A/B Testing Experiments
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS experiments (
                id INTEGER PRIMARY KEY,
                variant_name TEXT,  -- 'technical_depth', 'leadership_focus'
                total_applications INTEGER DEFAULT 0,
                total_responses INTEGER DEFAULT 0,
                response_rate REAL DEFAULT 0.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Offer History
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS offers (
                id INTEGER PRIMARY KEY,
                company TEXT,
                role TEXT,
                base_salary REAL,
                equity TEXT,
                bonus TEXT,
                benefits TEXT,  -- JSON
                received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                negotiation_status TEXT,
                final_offer TEXT  -- JSON
            )
        """)

        # Wellness Tracking
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS wellness_log (
                id INTEGER PRIMARY KEY,
                date DATE,
                applications_today INTEGER,
                burnout_score INTEGER,
                notes TEXT,
                logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Hallucination Guard (Resume Audit Trail)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS resume_audit (
                id INTEGER PRIMARY KEY,
                original_resume_hash TEXT,
                tailored_resume TEXT,
                tailored_hash TEXT,
                company TEXT,
                integrity_check BOOLEAN,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Career Contexts (Role switching)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS career_contexts (
                id INTEGER PRIMARY KEY,
                context_name TEXT UNIQUE,
                role_title TEXT,
                skills TEXT,  -- JSON array
                target_companies TEXT,  -- JSON array
                salary_expectation_min INTEGER,
                salary_expectation_max INTEGER,
                is_active BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Job Tracking
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS job_tracking (
                id INTEGER PRIMARY KEY,
                job_id TEXT,
                company TEXT,
                job_title TEXT,
                salary_min INTEGER,
                salary_max INTEGER,
                remote BOOLEAN,
                status TEXT,  -- 'found', 'prep-complete', 'applied', 'interview', 'offer', 'rejected'
                match_score INTEGER,
                discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                applied_at TIMESTAMP,
                status_updated_at TIMESTAMP,
                notes TEXT
            )
        """)

        conn.commit()

    def insert_career_profile(self, user_name, role, company, skills, years, targets):
        """Insert or update user career profile."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO career_profile 
            (user_name, current_role, current_company, skills, experience_years, target_roles, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (user_name, role, company, json.dumps(skills), years, json.dumps(targets)))
        conn.commit()
        return cursor.lastrowid

    def insert_application(self, company, role, score, persona, status, url, notes=""):
        """Log an application."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO applications 
            (company, role, compatibility_score, resume_persona, status, url, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (company, role, score, persona, status, url, notes))
        conn.commit()
        return cursor.lastrowid

    def insert_offer(self, company, role, salary, equity, bonus, benefits, status="pending"):
        """Log an offer received."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO offers 
            (company, role, base_salary, equity, bonus, benefits, negotiation_status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (company, role, salary, equity, bonus, json.dumps(benefits), status))
        conn.commit()
        return cursor.lastrowid

    def log_wellness(self, date, apps_today, burnout_score, notes=""):
        """Log daily wellness metrics."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO wellness_log (date, applications_today, burnout_score, notes)
            VALUES (?, ?, ?, ?)
        """, (date, apps_today, burnout_score, notes))
        conn.commit()
        return cursor.lastrowid

    def audit_resume(self, original_hash, tailored_resume, company):
        """Log resume tailoring for integrity verification."""
        conn = self.get_connection()
        cursor = conn.cursor()
        tailored_hash = self.security.hash_data(tailored_resume)
        cursor.execute("""
            INSERT INTO resume_audit (original_resume_hash, tailored_resume, tailored_hash, company, integrity_check)
            VALUES (?, ?, ?, ?, ?)
        """, (original_hash, self.security.encrypt(tailored_resume), tailored_hash, company, True))
        conn.commit()
        return cursor.lastrowid

    def get_applications_by_status(self, status):
        """Retrieve applications by status."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM applications WHERE status = ? ORDER BY applied_at DESC", (status,))
        return cursor.fetchall()

    def get_experiment_stats(self, variant_name):
        """Get A/B test statistics for a variant."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM experiments WHERE variant_name = ?", (variant_name,))
        return cursor.fetchone()

    def close(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None

    def backup_encrypted(self, backup_path=None):
        """Create an AES-256 encrypted backup of the database."""
        backup_path = backup_path or Path.home() / ".applywizard" / f"backup_{datetime.now().isoformat()}.db.aes"
        with open(self.db_path, 'rb') as f:
            db_content = f.read()
        encrypted = self.security.encrypt(db_content)
        with open(backup_path, 'w') as f:
            f.write(encrypted)
        return str(backup_path)

    def switch_career_context(self, context_name):
        """Switch to a different career context."""
        conn = self.get_connection()
        cursor = conn.cursor()
        # Deactivate all contexts
        cursor.execute("UPDATE career_contexts SET is_active = 0")
        # Activate target context
        cursor.execute("UPDATE career_contexts SET is_active = 1 WHERE context_name = ?", (context_name,))
        conn.commit()
        return {"status": "success", "active_context": context_name}

    def create_career_context(self, context_name, role_title, skills, target_companies, salary_min, salary_max):
        """Create a new career context."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO career_contexts
            (context_name, role_title, skills, target_companies, salary_expectation_min, salary_expectation_max)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (context_name, role_title, json.dumps(skills), json.dumps(target_companies), salary_min, salary_max))
        conn.commit()
        return cursor.lastrowid

    def get_active_context(self):
        """Get currently active career context."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM career_contexts WHERE is_active = 1 LIMIT 1")
        return cursor.fetchone()

    def track_job(self, job_id, company, job_title, salary_min, salary_max, remote, match_score):
        """Track a new job discovery."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO job_tracking (job_id, company, job_title, salary_min, salary_max, remote, status, match_score)
            VALUES (?, ?, ?, ?, ?, ?, 'found', ?)
        """, (job_id, company, job_title, salary_min, salary_max, remote, match_score))
        conn.commit()
        return cursor.lastrowid

    def update_job_status(self, job_id, new_status):
        """Update status of a tracked job."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE job_tracking SET status = ?, status_updated_at = CURRENT_TIMESTAMP WHERE job_id = ?
        """, (new_status, job_id))
        conn.commit()
        return {"status": "success", "job_id": job_id, "new_status": new_status}

    def get_tracked_jobs(self, status=None):
        """Retrieve tracked jobs, optionally filtered by status."""
        conn = self.get_connection()
        cursor = conn.cursor()
        if status:
            cursor.execute("SELECT * FROM job_tracking WHERE status = ? ORDER BY discovered_at DESC", (status,))
        else:
            cursor.execute("SELECT * FROM job_tracking ORDER BY discovered_at DESC")
        return cursor.fetchall()

    def get_job_tracking(self, job_id):
        """Get tracking info for a specific job."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM job_tracking WHERE job_id = ?", (job_id,))
        return cursor.fetchone()
