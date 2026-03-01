"""
Negotiation Intelligence Engine: 3-Tier Scripts, Approval Probability, Market Leverage
Provides personalized negotiation strategies with data-backed recommendations.
"""

import json
from datetime import datetime


class NegotiationEngine:
    """Generates negotiation scripts and strategies based on offers and market data."""

    # Negotiation templates (3-tier)
    NEGOTIATION_TIERS = {
        "conservative": {
            "tone": "Respectful, appreciation-focused",
            "script_template": [
                "Thank you for the offer. I'm excited about this opportunity.",
                "I've researched market rates for this role in {market}, and the typical range is ${min_salary}-${max_salary}.",
                "Given my experience and qualifications, I'd like to request a base salary of ${target_salary}.",
                "I'm flexible on other terms and open to discussion."
            ],
            "approval_probability": 0.65
        },
        "balanced": {
            "tone": "Professional, data-driven",
            "script_template": [
                "I appreciate the offer and I'm very interested in joining the team.",
                "Based on my market research, similar roles in {market} command {percentile}th percentile salaries.",
                "Considering my background in {skills}, I'd like to propose ${target_salary} base + {equity} equity.",
                "I'd also like to discuss {benefits}. Are these negotiable?"
            ],
            "approval_probability": 0.55
        },
        "aggressive": {
            "tone": "Confident, high-value positioning",
            "script_template": [
                "Thank you for the opportunity. I'm strong proponent of this role.",
                "My market value is ${target_salary} based on: {skills}, {achievements}, {market_data}.",
                "I'm seeking ${target_salary} base, {equity} options, and {signing_bonus} signing bonus.",
                "I have competing offers at this level. I'd prefer to join your team, but the compensation must align with market standards."
            ],
            "approval_probability": 0.35
        }
    }

    def __init__(self, db=None):
        self.db = db

    def analyze_offer(self, offered_salary, offered_equity, target_role, market_data):
        """Analyze offer against market benchmarks."""
        market_median = market_data.get("median", 0)
        market_p75 = market_data.get("p75", 0)
        market_p90 = market_data.get("p90", 0)
        
        percentile = 0
        if offered_salary >= market_p90:
            percentile = 90
        elif offered_salary >= market_p75:
            percentile = 75
        elif offered_salary >= market_median:
            percentile = 50
        else:
            percentile = 25
        
        return {
            "offered_salary": offered_salary,
            "market_median": market_median,
            "market_p75": market_p75,
            "percentile": percentile,
            "vs_median": offered_salary - market_median,
            "evaluation": "Above market" if percentile >= 75 else "Market rate" if percentile >= 50 else "Below market",
            "negotiation_urgency": "Not recommended" if percentile >= 80 else "Recommended" if percentile >= 40 else "Highly recommended"
        }

    def generate_negotiation_scripts(self, offer_details, market_data, user_skills):
        """Generate 3-tier negotiation scripts."""
        analysis = self.analyze_offer(
            offer_details["salary"],
            offer_details.get("equity", ""),
            offer_details["role"],
            market_data
        )
        
        market_median = market_data.get("median")
        market_p75 = market_data.get("p75")
        percentile = analysis["percentile"]
        
        # Calculate target salaries for each tier
        conservative_target = int(market_median * 1.05)
        balanced_target = int(market_p75 * 0.95)
        aggressive_target = int(market_p75 * 1.15)
        
        scripts = {}
        for tier_name, tier_config in self.NEGOTIATION_TIERS.items():
            if tier_name == "conservative":
                target = conservative_target
            elif tier_name == "balanced":
                target = balanced_target
            else:
                target = aggressive_target
            
            script_lines = []
            for template_line in tier_config["script_template"]:
                line = template_line.format(
                    market="US Market",
                    min_salary=market_median,
                    max_salary=market_p75,
                    target_salary=target,
                    percentile=percentile,
                    skills=", ".join(user_skills[:3]),
                    achievements="strong track record",
                    market_data=f"{percentile}th percentile",
                    equity=offer_details.get("equity", "0.1%"),
                    benefits="401k match, remote flexibility",
                    signing_bonus="$10,000"
                )
                script_lines.append(line)
            
            scripts[tier_name] = {
                "tone": tier_config["tone"],
                "script": "\n".join(script_lines),
                "target_salary": target,
                "approval_probability": tier_config["approval_probability"],
                "recommendation": self._tier_recommendation(tier_name, percentile)
            }
        
        return scripts

    def _tier_recommendation(self, tier_name, percentile):
        """Recommend tier based on market position."""
        if percentile < 40:
            return "🔴 Use AGGRESSIVE: You're undervalued. Significant upside available."
        elif percentile < 60:
            return "🟡 Use BALANCED: Reasonable negotiation point. Fair upside."
        else:
            return "🟢 Use CONSERVATIVE: Strong position. Minimal negotiation needed."

    def calculate_total_compensation(self, salary, equity_percent, bonus, benefits_value):
        """Calculate total compensation package."""
        return {
            "base_salary": salary,
            "equity_annual_value": equity_percent,
            "annual_bonus": bonus,
            "benefits_value": benefits_value,
            "total_comp": salary + bonus + benefits_value,
            "equity_note": f"{equity_percent}% vesting over 4 years = ${equity_percent * 0.25:.0f}K/year"
        }

    def compare_offers(self, offers_list):
        """Compare multiple offers side-by-side."""
        comparison = {
            "total_offers": len(offers_list),
            "offers": []
        }
        
        for offer in offers_list:
            total_comp = self.calculate_total_compensation(
                offer["salary"],
                offer.get("equity_value", 0),
                offer.get("bonus", 0),
                offer.get("benefits_value", 0)
            )
            comparison["offers"].append({
                "company": offer["company"],
                **total_comp
            })
        
        # Find best offer
        best_offer = max(comparison["offers"], key=lambda x: x["total_comp"])
        comparison["best_offer"] = best_offer
        
        return comparison

    def generate_counter_offer(self, original_offer, negotiation_tier, market_data):
        """Generate formal counter-offer email."""
        adjustments = {
            "conservative": 0.05,
            "balanced": 0.15,
            "aggressive": 0.30
        }
        
        adjustment_pct = adjustments.get(negotiation_tier, 0.10)
        new_salary = int(original_offer["salary"] * (1 + adjustment_pct))
        
        email = f"""
Subject: Re: Offer for {original_offer['role']} at {original_offer['company']}

Dear [Hiring Manager],

Thank you for the offer to join {original_offer['company']} as {original_offer['role']}.
I'm thrilled about the opportunity to contribute to the team.

After careful consideration and researching market benchmarks for this role,
I'd like to propose the following adjusted offer:

• Base Salary: ${new_salary:,} (vs. offered ${original_offer['salary']:,})
• Equity: {original_offer.get('equity', 'as discussed')}
• Signing Bonus: ${10000} (if applicable)
• Benefits: As discussed

I believe this represents fair market value for the position while demonstrating
my commitment to joining your organization.

I'm flexible and open to discussing these terms further.

Best regards,
[Your Name]
        """
        
        return {
            "email_template": email.strip(),
            "proposed_salary": new_salary,
            "adjustment_from_offer": new_salary - original_offer["salary"],
            "negotiation_tier": negotiation_tier
        }

    def estimate_success_probability(self, negotiation_tier, market_position, competing_offers):
        """Estimate probability of successful negotiation."""
        base_probability = self.NEGOTIATION_TIERS[negotiation_tier]["approval_probability"]
        
        # Adjust based on market position
        if market_position == "strong":
            base_probability += 0.20
        elif market_position == "weak":
            base_probability -= 0.10
        
        # Adjust based on competing offers
        if competing_offers > 2:
            base_probability += 0.15
        
        return {
            "tier": negotiation_tier,
            "success_probability": min(1.0, base_probability),
            "recommendation": "High chance of success" if base_probability > 0.75 else "Moderate chance" if base_probability > 0.50 else "Low chance - proceed with caution"
        }
