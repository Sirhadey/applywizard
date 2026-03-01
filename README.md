# ApplyWizard v5.0 - Zero-Knowledge Career Operating System

A comprehensive Python CLI for intelligent career navigation, offer negotiation, and application strategy optimization. Built with privacy-first principles, zero telemetry, and local encryption.

## Architecture & Pillars

### 🔐 Zero-Knowledge Sovereignty
- **Local Storage**: SQLite database with AES-256 encrypted backups
- **Keyring Integration**: OS-level secure API key management
- **Privacy**: Zero telemetry, no cloud storage, no external data sharing
- **GDPR Compliant**: No third-party data collection

### 🧠 Intelligence Core
- **Predictive Pathing**: Career trajectory analysis and next-step recommendations
- **DNA Matching**: Company culture compatibility scoring
- **Market Intelligence**: 2026 salary benchmarks and negotiation leverage
- **Personalized Moves**: Strategic recommendations based on application history

### 📋 Semantic Bridge v2.0
- **Form Ingest**: Parse saved HTML forms from DevTools
- **ATS Detection**: Identify which system (Workday, Greenhouse, Taleo)
- **Guided Field Queue**: Sequential clipboard loop for high-friction forms
- **Smart Suggestions**: Pre-populate fields from profile data

### 💰 Negotiation Intelligence
- **3-Tier Scripts**: Conservative, Balanced, Aggressive negotiation tactics
- **Approval Probability**: Data-backed success likelihood for each tier
- **Total Comp Analysis**: Breakdown of salary, equity, bonus, benefits
- **Counter-Offer Generation**: Formal email templates with market justification

### 🧘 Wellness & Ethics Shield
- **Burnout Monitor**: Application velocity tracking with mandatory breaks
- **Hallucination Guard**: Resume integrity verification (100% factual accuracy)
- **A/B Testing Framework**: Track response rates for different resume personas
- **Statistical Significance**: Chi-square testing for variant comparison

## Installation

```bash
pip install -r requirements.txt
python applywizard.py --help
```

## Commands

### 1. Career Analysis
```bash
python applywizard.py analyze --path "Python Developer"
```
Shows next-step roles, skills to acquire, and timeline.

### 2. Market Intelligence
```bash
python applywizard.py market --trends
```
Predicts emerging skills, fastest-growing roles, and salary trends.

### 3. Job Posting Ingestion
```bash
python applywizard.py ingest "https://example.com/job-posting"
```
Scores compatibility and extracts key role markers.

### 4. Resume Tailoring
```bash
python applywizard.py tailor --persona "startup"
```
Options: startup, enterprise, technical, leadership

### 5. ATS Form Bridge
```bash
python applywizard.py bridge
```
Starts guided paste loop with suggested values.

### 6. Offer Negotiation
```bash
python applywizard.py negotiate --offer '{"salary": 150000, "company": "TechCorp", "role": "Senior Engineer"}'
```
Generates 3-tier scripts with success probabilities.

### 7. Wellness Check
```bash
python applywizard.py wellness --check 8
```
Assesses burnout risk and recommends breaks.

### 8. Initialize System
```bash
python applywizard.py init
```
Set up career profile with manual context selection.

### 9. Encrypted Backup
```bash
python applywizard.py backup
```
Creates AES-256 encrypted backup of all data.

## Key Features

| Feature | Details |
|---------|---------|
| **Encryption** | AES-256 for all sensitive data |
| **Database** | SQLite with encrypted backups |
| **Security** | OS keyring or env var for master key |
| **Telemetry** | None - 100% local processing |
| **Backup** | Encrypted exports available on demand |

## Data Model

### Career Profile
- Current role, company, years of experience
- Skills and target roles
- Profile-company compatibility scores

### Applications Log
- Company, role, compatibility score
- Resume persona used
- Status tracking (submitted, responded, interviewing, offered)
- Response timeline

### Offers & Negotiation
- Offer details (salary, equity, bonus, benefits)
- Negotiation history
- Counter-offer tracking

### Wellness & Experiments
- Daily application velocity
- Burnout score calculations
- A/B test results (variant response rates)
- Resume integrity audit trail

## Configuration

Set environment variable for master key (optional):
```bash
export APPLYWIZARD_KEY="your-secure-key"
```

All data stored in: `~/.applywizard/`

## Privacy Notice

✅ **What ApplyWizard Does NOT Do:**
- Send data to cloud services
- Track your IP or location
- Store third-party names (professionals at target companies)
- Require authentication
- Share data with anyone

✅ **What ApplyWizard Does:**
- Stores data locally in encrypted SQLite
- Provides market-backed negotiation scripts
- Tracks your application strategy
- Monitors burnout and wellness
- Generates resume variants for A/B testing

## Roadmap (v5.1+)

- [ ] LinkedIn profile auto-parsing
- [ ] Real-time job board scraping
- [ ] Interview prep with mock questions
- [ ] Equity calculator with vesting schedules
- [ ] Visa pathway simulator
- [ ] Tax optimization for RSU/options

## Contributing

This is a personal career OS. For bugs/features, use GitHub issues.

## License

Proprietary - ApplyWizard v5.0. Use at your own risk.
