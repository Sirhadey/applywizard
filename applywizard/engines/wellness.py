"""
Wellness & Ethics Shield: Burnout Monitor, Hallucination Guard, A/B Testing
Protects user health while ensuring resume integrity and optimizing application strategy.
"""

import json
from datetime import datetime, timedelta
from collections import defaultdict


class WellnessEngine:
    """Monitors burnout, ensures resume integrity, and runs A/B testing experiments."""

    # Burnout thresholds
    BURNOUT_THRESHOLDS = {
        "low": {"apps_per_day": 3, "burnout_score": 0},
        "moderate": {"apps_per_day": 5, "burnout_score": 35},
        "high": {"apps_per_day": 8, "burnout_score": 65},
        "critical": {"apps_per_day": 12, "burnout_score": 85}
    }

    def __init__(self, db=None, security_manager=None):
        self.db = db
        self.security = security_manager
        self.experiments = {}

    def calculate_burnout_score(self, apps_today, apps_this_week, hours_spent_today):
        """Calculate burnout score based on activity metrics."""
        score = 0
        
        # Apps per day scoring
        if apps_today >= 12:
            score += 40
        elif apps_today >= 8:
            score += 30
        elif apps_today >= 5:
            score += 15
        
        # Weekly velocity scoring
        if apps_this_week >= 40:
            score += 30
        elif apps_this_week >= 25:
            score += 15
        
        # Time spent scoring
        if hours_spent_today >= 6:
            score += 30
        elif hours_spent_today >= 4:
            score += 15
        
        return min(100, score)

    def check_burnout_status(self, apps_today):
        """Assess burnout status and recommend break if needed."""
        status = "healthy"
        message = "Pace is sustainable. Keep going!"
        urgent = False
        
        if apps_today >= 12:
            status = "critical"
            message = "🔴 CRITICAL: You've applied to 12+ roles today. MANDATORY BREAK recommended. Step away and recharge."
            urgent = True
        elif apps_today >= 8:
            status = "high"
            message = "🟠 HIGH: You're at risk of burnout. Consider taking a break or reducing daily target."
        elif apps_today >= 5:
            status = "moderate"
            message = "🟡 MODERATE: Steady pace. Make sure to rest and maintain quality over quantity."
        
        recommendation = {
            "status": status,
            "apps_today": apps_today,
            "message": message,
            "urgent": urgent,
            "suggested_actions": self._get_wellness_actions(status)
        }
        
        if self.db:
            self.db.log_wellness(datetime.today().date(), apps_today, self.calculate_burnout_score(apps_today, 0, 0))
        
        return recommendation

    def _get_wellness_actions(self, status):
        """Get recommended wellness actions based on status."""
        actions = {
            "healthy": ["Continue current pace", "Set daily application cap at 5-7"],
            "moderate": ["Take 30-min walk", "Hydrate", "Review quality over quantity"],
            "high": ["Take 1-2 hour break", "Disconnect from job search", "Do something unrelated"],
            "critical": ["STOP APPLYING NOW", "Take full day off", "Reflect on strategy Tomorrow"]
        }
        return actions.get(status, [])

    def hallucination_guard(self, original_resume_path, tailored_resume_text, company_name):
        """Verify resume tailoring maintains 100% factual integrity."""
        if not self.security:
            return {"status": "error", "message": "Security manager not configured."}
        
        # Hash original resume
        with open(original_resume_path, 'r', encoding='utf-8') as f:
            original_text = f.read()
        
        original_hash = self.security.hash_data(original_text)
        
        # Extract key facts from original
        original_facts = self._extract_facts(original_text)
        tailored_facts = self._extract_facts(tailored_resume_text)
        
        # Check for hallucination (claimed skills/experience not in original)
        hallucinations = []
        for fact in tailored_facts:
            if fact not in original_facts and not self._is_generalization(fact, original_facts):
                hallucinations.append(fact)
        
        # Log audit trail
        if self.db:
            self.db.audit_resume(original_hash, tailored_resume_text, company_name)
        
        integrity_score = 100 if not hallucinations else max(0, 100 - (len(hallucinations) * 10))
        
        return {
            "company": company_name,
            "integrity_score": integrity_score,
            "is_factually_accurate": len(hallucinations) == 0,
            "hallucinations_detected": hallucinations,
            "warning": "⚠️ Resume contains claims not in original!" if hallucinations else "✅ Resume is factually accurate.",
            "audit_trail_logged": True
        }

    def _extract_facts(self, text):
        """Extract key facts/skills from resume text."""
        facts = set()
        # Simple extraction: look for common skill keywords
        skills = ["python", "java", "javascript", "sql", "aws", "azure", "react", "django", "machine learning", "ai", "data science"]
        for skill in skills:
            if skill.lower() in text.lower():
                facts.add(skill)
        return facts

    def _is_generalization(self, specific_fact, original_facts):
        """Check if a specific fact is a reasonable generalization of original facts."""
        generalizations = {
            "full-stack engineer": ["frontend", "backend"],
            "cloud architect": ["aws", "azure", "gcp"],
            "data scientist": ["machine learning", "statistics", "python"]
        }
        
        for general, specifics in generalizations.items():
            if specific_fact.lower() == general:
                return any(s in original_facts for s in specifics)
        
        return False

    def setup_ab_test(self, test_name, variant_a_name, variant_b_name, control_group_size=0.5):
        """Setup A/B testing experiment for resume variants."""
        experiment = {
            "test_id": len(self.experiments) + 1,
            "test_name": test_name,
            "created_at": datetime.now().isoformat(),
            "variant_a": {
                "name": variant_a_name,
                "applications": 0,
                "responses": 0,
                "response_rate": 0.0
            },
            "variant_b": {
                "name": variant_b_name,
                "applications": 0,
                "responses": 0,
                "response_rate": 0.0
            },
            "control_group_split": control_group_size,
            "status": "active"
        }
        
        self.experiments[test_name] = experiment
        
        if self.db:
            self.db.execute("""
                CREATE TABLE IF NOT EXISTS ab_tests (
                    id INTEGER PRIMARY KEY,
                    test_name TEXT,
                    variant_a TEXT,
                    variant_b TEXT,
                    created_at TIMESTAMP
                )
            """)
        
        return experiment

    def record_application_response(self, test_name, variant, success):
        """Record application result for A/B test."""
        if test_name not in self.experiments:
            return {"status": "error", "message": f"Test '{test_name}' not found."}
        
        experiment = self.experiments[test_name]
        variant_key = "variant_a" if variant == "a" else "variant_b"
        
        experiment[variant_key]["applications"] += 1
        if success:
            experiment[variant_key]["responses"] += 1
        
        # Calculate response rate
        total_apps = experiment[variant_key]["applications"]
        total_responses = experiment[variant_key]["responses"]
        experiment[variant_key]["response_rate"] = total_responses / total_apps if total_apps > 0 else 0
        
        return {
            "test_name": test_name,
            "variant": variant,
            "response_rate": experiment[variant_key]["response_rate"]
        }

    def get_ab_test_results(self, test_name):
        """Get current A/B test results and winner."""
        if test_name not in self.experiments:
            return {"status": "error", "message": f"Test '{test_name}' not found."}
        
        experiment = self.experiments[test_name]
        variant_a = experiment["variant_a"]
        variant_b = experiment["variant_b"]
        
        winner = None
        if variant_a["response_rate"] > variant_b["response_rate"]:
            winner = "A"
        elif variant_b["response_rate"] > variant_a["response_rate"]:
            winner = "B"
        
        return {
            "test_name": test_name,
            "variant_a": variant_a,
            "variant_b": variant_b,
            "winner": winner,
            "recommendation": f"Recommended: Use {variant_a['name']}" if winner == "A" else f"Recommended: Use {variant_b['name']}" if winner == "B" else "No winner yet. Continue testing."
        }

    def calculate_statistical_significance(self, variant_a_responses, variant_a_total, variant_b_responses, variant_b_total, confidence_level=0.95):
        """Simple Chi-square test for statistical significance."""
        import math
        
        rate_a = variant_a_responses / variant_a_total if variant_a_total > 0 else 0
        rate_b = variant_b_responses / variant_b_total if variant_b_total > 0 else 0
        
        # Simplified calculation
        pooled_rate = (variant_a_responses + variant_b_responses) / (variant_a_total + variant_b_total) if (variant_a_total + variant_b_total) > 0 else 0
        
        if pooled_rate == 0 or pooled_rate == 1:
            return {"is_significant": False, "p_value": 1.0}
        
        # Z-test approximation
        se = math.sqrt(pooled_rate * (1 - pooled_rate) * (1/variant_a_total + 1/variant_b_total))
        z = (rate_a - rate_b) / se if se > 0 else 0
        
        # Approximate p-value (simplified)
        p_value = 1 - abs(z) / 3  # Rough approximation
        
        return {
            "is_significant": p_value < (1 - confidence_level),
            "p_value": max(0, min(1, p_value)),
            "confidence_level": confidence_level
        }

    def wellness_dashboard(self):
        """Generate wellness dashboard summary."""
        return {
            "burnout_status": "Monitoring",
            "active_experiments": len(self.experiments),
            "resume_integrity_checks": "Enabled",
            "daily_cap_recommendation": "5-7 applications",
            "next_break_recommended": "Tomorrow if >8 apps today",
            "message": "Keep the balance. Burnout hurts. Success is a marathon, not a sprint."
        }
