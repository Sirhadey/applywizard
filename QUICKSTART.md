# ApplyWizard v5.0 - Quick Start Guide

## Installation

1. Navigate to the project directory:
```bash
cd /home/elliot/Documents/OSINT/ApplyWizard\ v6.3
```

2. View all available commands:
```bash
python applywizard.py --help
```

## First Steps

### 1. Initialize Your Profile
```bash
python applywizard.py init
```
This sets up your career OS with privacy-first context selection.

### 2. Analyze Your Career Path
```bash
python applywizard.py analyze --path "Python Developer"
```
Outputs:
- Next-step career options
- Skills to acquire
- Timeline (typically 9-18 months)
- Market demand assessment

### 3. Check Market Trends
```bash
python applywizard.py market --trends
```
Outputs:
- Top emerging skills
- Fastest-growing roles
- Sunset roles to avoid
- Salary growth by sector (2026)

## Common Workflows

### Workflow 1: Evaluate a Job Posting

```bash
# Step 1: Ingest the job posting
python applywizard.py ingest "https://example.com/job-posting"
# Returns compatibility score (0-100%)

# Step 2: Analyze your fit against career path
python applywizard.py analyze --path "Your Current Role"

# Step 3: Decide to apply and start form completion
python applywizard.py bridge
# Guided step-by-step form filling with pre-filled suggestions
```

### Workflow 2: Tailor Resume & Apply

```bash
# Step 1: Choose a resume persona
python applywizard.py tailor --persona "startup"
# Choose from: startup, enterprise, technical, leadership

# Step 2: Save the tailored resume

# Step 3: Complete the application form
python applywizard.py bridge

# Step 4: Track in system (database logs automatically)
```

### Workflow 3: Negotiate an Offer

```bash
# When you receive an offer:
python applywizard.py negotiate --offer '{
  "salary": 150000,
  "company": "TechCorp",
  "role": "Senior Engineer",
  "equity": "0.5%"
}'
```

**You'll get:**
- **Conservative Script** (65% success): Safe negotiation
- **Balanced Script** (55% success): Typical approach
- **Aggressive Script** (35% success): Maximum upside

Choose the tier based on your market position and competing offers.

### Workflow 4: Monitor Burnout & Wellness

```bash
# End of day check
python applywizard.py wellness --check 8
# Pass the number of applications you submitted today

# Outputs:
# - Burnout status (Healthy/Moderate/High/Critical)
# - Recommended actions
# - Wellness dashboard
```

## Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| `init` | Initialize ApplyWizard | `python applywizard.py init` |
| `analyze` | Career path analysis | `python applywizard.py analyze --path "Python Developer"` |
| `market` | Market trends 2026 | `python applywizard.py market --trends` |
| `ingest` | Score job posting | `python applywizard.py ingest "https://..."`|
| `tailor` | Generate resume variant | `python applywizard.py tailor --persona "startup"` |
| `bridge` | Guided ATS form filling | `python applywizard.py bridge` |
| `negotiate` | Generate negotiation scripts | `python applywizard.py negotiate --offer '{"salary": 150000, ...}'` |
| `wellness` | Burnout check | `python applywizard.py wellness --check 8` |
| `backup` | Encrypted backup | `python applywizard.py backup` |

## Tips & Best Practices

### Resume Personas
- **Startup**: Emphasize adaptability, growth mindset, MVP thinking
- **Enterprise**: Highlight process expertise, team leadership, scalability
- **Technical**: Deep skills, architecture, systems design
- **Leadership**: Management experience, team building, strategic vision

### Negotiation Strategy
- Use **Conservative** if you're below market rate by <10%
- Use **Balanced** if you're at market rate or slightly below
- Use **Aggressive** if you have competing offers or are significantly undervalued

### Burnout Prevention
- Keep daily applications under 5-7
- If you hit 8+ apps, take a mandatory break
- If you hit 12+, stop for the day (critical alert)
- A/B test different resume personas to improve response rates

### Data Privacy
- All data stays on your machine (encrypted)
- No cloud sync, no external integrations
- Optional backups can be created with encryption
- Safe to use on work/personal computers

## FAQ

**Q: Will my data be safe?**
A: Yes. All data is encrypted locally using AES-256. No data leaves your machine.

**Q: Can I back up my data?**
A: Yes, use `python applywizard.py backup` to create an encrypted backup.

**Q: How do I know which negotiation script to use?**
A: Check the recommendation at the bottom. It considers your market position.

**Q: What if I get an error about keyring?**
A: That's normal on Linux. ApplyWizard falls back to encrypted file storage. Ignore the DBus warnings.

**Q: Can I use this from multiple machines?**
A: You'd need to manually transfer encrypted backups. Each machine has its own local encryption key.

**Q: How accurate are the career predictions?**
A: They're based on aggregated 2026 market data. Use them as guidance, not gospel. Always research roles independently.

## Examples

### Example 1: Python Developer → AI Engineer Path
```bash
$ python applywizard.py analyze --path "Python Developer"

Output:
{
  "current_role": "Python Developer",
  "next_steps": [
    "Senior Python Dev",
    "Python Architect",
    "AI/ML Engineer"
  ],
  "skills_to_acquire": [
    "ML/AI Fundamentals",
    "PyTorch/TensorFlow",
    "Statistics & Math"
  ],
  "recommended_timeline_months": 12,
  "market_demand": "High (AI/ML trending +35% YoY)"
}
```

### Example 2: Evaluate Offer (Below Market)
```bash
$ python applywizard.py negotiate --offer '{"salary": 150000, "company": "X", "role": "Senior Engineer"}'

Output shows all 3 tiers with:
🔴 AGGRESSIVE RECOMMENDED: You're undervalued. Significant upside available.

Target: $252,999 (vs. offered $150,000 = +$102,999 delta)
Success Probability: 35% but high leverage
```

### Example 3: Burnout Alert
```bash
$ python applywizard.py wellness --check 14

Output:
🔴 CRITICAL: You've applied to 12+ roles today. MANDATORY BREAK recommended.

Recommended Actions:
  • STOP APPLYING NOW
  • Take full day off
  • Reflect on strategy tomorrow
```

## Getting Help

For bugs or feature requests, check the README.md or ARCHITECTURE.md files for detailed documentation.

---

**Remember:** ApplyWizard is your strategic career OS. Use it to be intentional, not desperate. Quality over quantity. 🚀
