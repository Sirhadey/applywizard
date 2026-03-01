"""
Intelligence Engine: Predictive Pathing, DNA Matching, Market Intelligence
Analyzes career trajectory, company culture fit, and market trends.
"""

import json
from datetime import datetime


class IntelligenceEngine:
    """Provides career path analysis and market intelligence."""

    # Career progression patterns (simplified)
    CAREER_PATHS = {
        "python_developer": {
            "next_steps": ["Senior Python Dev", "Python Architect", "DevOps Engineer", "AI/ML Engineer"],
            "skills_to_acquire": ["Cloud (AWS/GCP)", "System Design", "ML Basics"],
            "timeline_months": 12
        },
        "data_analyst": {
            "next_steps": ["Senior Data Analyst", "Analytics Engineer", "Data Scientist", "BI Developer"],
            "skills_to_acquire": ["SQL Advanced", "Python/R", "Statistics"],
            "timeline_months": 9
        },
        "product_manager": {
            "next_steps": ["Senior PM", "Director of Product", "VP Product", "Founder"],
            "skills_to_acquire": ["Strategy", "Leadership", "Analytics"],
            "timeline_months": 18
        }
    }

    # Company culture signals (simplified taxonomy)
    CULTURE_SIGNALS = {
        "startup": {
            "traits": ["fast-paced", "equity-based", "flat-hierarchy", "high-risk-high-reward"],
            "ideal_profiles": ["adaptable", "self-motivated", "risk-tolerant"]
        },
        "scale-up": {
            "traits": ["growth-focused", "standardized-processes", "emerging-hierarchy"],
            "ideal_profiles": ["ambitious", "structured-thinker"]
        },
        "enterprise": {
            "traits": ["stability", "hierarchical", "process-driven", "pension-benefits"],
            "ideal_profiles": ["detail-oriented", "collaborative", "process-expert"]
        }
    }

    # Market salary benchmarks (2026, USD)
    SALARY_BENCHMARKS = {
        "senior_engineer_us": {"median": 185000, "p75": 220000, "p90": 260000},
        "product_manager_us": {"median": 195000, "p75": 240000, "p90": 285000},
        "data_scientist_us": {"median": 175000, "p75": 210000, "p90": 250000},
        "ai_engineer_us": {"median": 215000, "p75": 260000, "p90": 310000},
    }

    def __init__(self, db=None):
        self.db = db

    def analyze_career_path(self, current_role, target_role=None):
        """Analyze career trajectory and suggest next steps."""
        current_normalized = current_role.lower().replace(" ", "_")
        
        if current_normalized not in self.CAREER_PATHS:
            return {
                "status": "role_not_found",
                "message": f"No predefined path for '{current_role}'. Consider exploring adjacent roles."
            }
        
        path = self.CAREER_PATHS[current_normalized]
        return {
            "current_role": current_role,
            "next_steps": path["next_steps"],
            "skills_to_acquire": path["skills_to_acquire"],
            "recommended_timeline_months": path["timeline_months"],
            "market_demand": "High (AI/Cloud skills trending +35% YoY)"
        }

    def dna_match_company(self, user_profile, company_name, company_culture_type="startup"):
        """Calculate compatibility score based on culture fit and role alignment."""
        if company_culture_type not in self.CULTURE_SIGNALS:
            company_culture_type = "startup"
        
        culture = self.CULTURE_SIGNALS[company_culture_type]
        user_traits = user_profile.get("traits", [])
        ideal_traits = culture["ideal_profiles"]
        
        overlap = len(set(user_traits) & set(ideal_traits))
        max_score = len(ideal_traits)
        compatibility_score = min(100, int((overlap / max_score * 100) if max_score > 0 else 0))
        
        return {
            "company": company_name,
            "company_type": company_culture_type,
            "compatibility_score": compatibility_score,
            "reasoning": f"Score based on {overlap}/{max_score} ideal traits match",
            "recommendation": "Strong fit" if compatibility_score >= 75 else "Moderate fit" if compatibility_score >= 50 else "Low fit"
        }

    def market_intelligence(self, role, region="US"):
        """Provide salary benchmarks and market trends."""
        role_normalized = role.lower().replace(" ", "_")
        
        benchmark = self.SALARY_BENCHMARKS.get(role_normalized)
        if not benchmark:
            return {"status": "role_not_benchmarked", "message": "Market data not available for this role."}
        
        return {
            "role": role,
            "region": region,
            "salary_data": benchmark,
            "market_trend": "+15% YoY (AI/ML roles driving demand)",
            "demand_level": "High",
            "negotiation_leverage": "Strong (candidate-favorable market)"
        }

    def predict_market_trends(self):
        """Predict market trends for 2026."""
        return {
            "top_emerging_skills": ["AI/ML Engineering", "Cloud Architecture", "Data Engineering"],
            "fastest_growing_roles": ["AI Engineer", "ML Ops Engineer", "Data Architect"],
            "sunset_roles": ["Traditional QA", "Junior Data Entry"],
            "salary_growth_sectors": ["AI/ML: +40%", "Cloud: +25%", "Cybersecurity: +30%"]
        }

    def personalized_move_recommendation(self, user_profile, applications_data):
        """Suggest next strategic move based on profile and application history."""
        if not applications_data:
            return {"recommendation": "Start applying to roles aligned with {}.".format(user_profile.get("current_role"))}
        
        responses = [app for app in applications_data if app.get("response_at")]
        response_rate = len(responses) / len(applications_data) if applications_data else 0
        
        if response_rate < 0.1:
            return {
                "recommendation": "Tailor resume more aggressively. Current response rate is low. Consider shifting to 'Leadership Focus' persona.",
                "action": "Run A/B test with different resume variant."
            }
        elif response_rate > 0.3:
            return {
                "recommendation": "Strong response rate. Accelerate pipeline. Prepare negotiation strategies.",
                "action": "Load offer negotiation engine."
            }
        
        return {"recommendation": "Maintain current trajectory. Response rate is normal."}
