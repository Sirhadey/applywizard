# ApplyWizard v5.0 - Architecture & Implementation Guide

## Overview
ApplyWizard v5.0 is a comprehensive, privacy-first career operating system built with Python. It combines intelligent career guidance, strategic application optimization, offer negotiation, and wellness monitoring into a unified CLI tool.

## Project Structure

```
ApplyWizard v6.3/
├── applywizard/                    # Main package
│   ├── __init__.py                # Package initialization
│   ├── core/                       # Core modules
│   │   ├── __init__.py
│   │   ├── security.py            # AES-256 encryption, keyring integration
│   │   └── database.py            # SQLite with encrypted backups
│   ├── engines/                    # Intelligence engines
│   │   ├── __init__.py
│   │   ├── intelligence.py        # Career path analysis, DNA matching
│   │   ├── semantic_bridge.py     # Form ingest, ATS parsing
│   │   ├── negotiation.py         # Negotiation scripts, approval probability
│   │   └── wellness.py            # Burnout monitor, hallucination guard, A/B testing
│   └── utils/                      # Utility modules
│       └── __init__.py
├── applywizard.py                 # Main CLI entry point
├── requirements.txt               # Dependencies
└── README.md                       # Project documentation
```

## Core Components

### 1. Security Manager (`applywizard/core/security.py`)
- **AES-256 Encryption**: Fernet-based encryption for data protection
- **Keyring Integration**: OS-level secret management (Linux, macOS, Windows compatible)
- **Hash Verification**: SHA-256 integrity checks
- **Fallback Mechanism**: Encrypted file storage if keyring unavailable

**Key Methods:**
- `encrypt(data)` - Encrypts sensitive data
- `decrypt(data)` - Decrypts encrypted data
- `store_secret(key, value)` - Securely stores API keys
- `retrieve_secret(key)` - Retrieves stored secrets
- `hash_data(data)` - Creates SHA-256 hash for verification

### 2. Database (`applywizard/core/database.py`)
- **SQLite Backend**: Local persistence without cloud
- **Encrypted Backups**: Optional AES-256 encrypted backups
- **Schema Management**: Automatic table creation and schema initialization
- **Data Models**:
  - Career profiles (skills, experience, targets)
  - Applications log (tracking status, compatibility)
  - Offers history (salary, equity, benefits)
  - Wellness metrics (burnout tracking)
  - A/B experiments (resume variant testing)
  - Resume audit trail (hallucination detection)

**Key Methods:**
- `insert_career_profile()` - Store user profile
- `insert_application()` - Log job application
- `insert_offer()` - Record offer received
- `log_wellness()` - Track daily metrics
- `audit_resume()` - Verify resume integrity
- `backup_encrypted()` - Create encrypted backup

### 3. Intelligence Engine (`applywizard/engines/intelligence.py`)
- **Career Path Analysis**:
  - Predefined career progression patterns
  - Next-step recommendations
  - Skills gap identification
  - Timeline-based roadmap

- **DNA Matching**:
  - Company culture signal classification (startup, scale-up, enterprise)
  - User trait mapping
  - Compatibility scoring (0-100%)

- **Market Intelligence**:
  - 2026 salary benchmarks (US market)
  - Trending skills (+35% YoY)
  - Sector growth rates
  - Negotiation leverage assessment

**Key Methods:**
- `analyze_career_path(current_role, target_role)` 
- `dna_match_company(user_profile, company_name, culture_type)`
- `market_intelligence(role, region)`
- `predict_market_trends()`
- `personalized_move_recommendation(user_profile, applications_data)`

### 4. Semantic Bridge (`applywizard/engines/semantic_bridge.py`)
- **HTML Form Parsing**:
  - Custom HTMLParser for extracting form fields
  - Support for input, textarea, select elements
  - Label text extraction

- **ATS Detection**:
  - Identifies Workday, Greenhouse, Taleo systems
  - System-specific field mapping

- **Guided Field Queue**:
  - Sequential form completion guidance
  - Smart value suggestions from user profile
  - Required field validation

- **Form Management**:
  - Field-by-field instructions
  - Progress tracking
  - Completion validation

**Key Methods:**
- `ingest_html_form(html_file_path)` - Parse saved HTML
- `detect_ats_system(html_file_path)` - Identify ATS
- `create_field_queue(fields, user_data)` - Create sequential queue
- `guided_paste_loop(field_sequence_num)` - Guide user through field
- `validate_form_completion(field_values)` - Check required fields
- `export_form_data(field_values, format)` - Export as JSON/CSV

### 5. Negotiation Engine (`applywizard/engines/negotiation.py`)
- **3-Tier Negotiation Scripts**:
  1. **Conservative** (65% approval): Respectful, appreciation-focused
  2. **Balanced** (55% approval): Professional, data-driven
  3. **Aggressive** (35% approval): High-value positioning

- **Market Analysis**:
  - Benchmark comparison (median, p75, p90)
  - Percentile positioning
  - Negotiation recommendation

- **Total Compensation**:
  - Salary breakdown
  - Equity valuation
  - Signing bonus
  - Benefits package

- **Negotiation Tools**:
  - Counter-offer email templates
  - Success probability calculation
  - Offer comparison analysis

**Key Methods:**
- `analyze_offer(offered_salary, equity, role, market_data)`
- `generate_negotiation_scripts(offer_details, market_data, user_skills)`
- `calculate_total_compensation(salary, equity, bonus, benefits)`
- `compare_offers(offers_list)`
- `generate_counter_offer(original_offer, tier, market_data)`
- `estimate_success_probability(tier, market_position, competing_offers)`

### 6. Wellness Engine (`applywizard/engines/wellness.py`)
- **Burnout Monitoring**:
  - Applications per day tracking
  - Weekly velocity calculation
  - Burnout score (0-100%)
  - Status levels: healthy, moderate, high, critical

- **Hallucination Guard**:
  - Original vs. tailored resume comparison
  - Fact extraction and verification
  - Integrity scoring (0-100%)
  - Audit trail logging

- **A/B Testing Framework**:
  - Setup experiments with two variants
  - Track response rates
  - Statistical significance testing
  - Winner determination

- **Wellness Dashboard**:
  - Summary metrics
  - Burnout status
  - Active experiments count
  - Recommendations

**Key Methods:**
- `calculate_burnout_score(apps_today, apps_week, hours_spent)`
- `check_burnout_status(apps_today)`
- `hallucination_guard(original_resume, tailored_resume, company)`
- `setup_ab_test(test_name, variant_a, variant_b)`
- `record_application_response(test_name, variant, success)`
- `get_ab_test_results(test_name)`
- `calculate_statistical_significance(responses_a, total_a, responses_b, total_b)`
- `wellness_dashboard()`

## CLI Commands

### Career Analysis
```bash
python applywizard.py analyze --path "Python Developer"
```
Returns next steps, skills to acquire, timeline, and market demand.

### Market Intelligence
```bash
python applywizard.py market --trends
```
Shows emerging skills, fastest-growing roles, sunset roles, salary growth.

### Job Posting Ingestion
```bash
python applywizard.py ingest "https://example.com/job"
```
Scores compatibility and provides match analysis.

### Resume Tailoring
```bash
python applywizard.py tailor --persona "startup"
```
Options: `startup`, `enterprise`, `technical`, `leadership`

### ATS Form Bridge
```bash
python applywizard.py bridge
```
Initiates guided form completion.

### Offer Negotiation
```bash
python applywizard.py negotiate --offer '{"salary": 150000, "company": "X", "role": "Y"}'
```
Generates 3-tier scripts with success probabilities.

### Wellness Check
```bash
python applywizard.py wellness --check 8
```
Assesses burnout and provides recommendations.

### Initialization
```bash
python applywizard.py init
```
Sets up career profile with privacy-first context.

### Encrypted Backup
```bash
python applywizard.py backup
```
Creates AES-256 encrypted backup of all data.

## Data Flow Diagrams

### Application Submission Flow
```
Job Posting 
    ↓
[Ingest: Parse & Score]
    ↓
Intelligence Engine → Compatibility Score (0-100%)
    ↓
[Tailor Resume]
    ↓
Semantic Bridge → ATS Detection & Form Parsing
    ↓
[Bridge] → Guided Field Queue
    ↓
Application Submitted → Logged to Database
    ↓
A/B Test Tracking (Variant, Response Rate)
```

### Offer Negotiation Flow
```
Offer Received
    ↓
[Negotiation Engine]
    ↓
Market Analysis → Benchmarking
    ↓
Generate 3-Tier Scripts
    ├─ Conservative (65% chance)
    ├─ Balanced (55% chance)
    └─ Aggressive (35% chance)
    ↓
Success Probability Calculation
    ↓
Counter-Offer Template
    ↓
Total Comp Breakdown
```

### Wellness Monitoring Flow
```
Daily Application Activity
    ↓
[Wellness Engine]
    ↓
Calculate Burnout Score
    ├─ Apps/day
    ├─ Apps/week
    └─ Hours spent
    ↓
Status Assessment (Healthy/Moderate/High/Critical)
    ↓
Resume Integrity Check (Hallucination Guard)
    ↓
A/B Test Results Tracking
    ↓
Dashboard & Recommendations
```

## Configuration

### Environment Variables
```bash
# Set custom master password
export APPLYWIZARD_KEY="your-secure-key"

# Path to database (optional)
export APPLYWIZARD_DB_PATH="/custom/path/careerdata.db"
```

### Data Storage
All data stored in: `~/.applywizard/`
- `careerdata.db` - Main SQLite database
- `secrets.json` - Encrypted secrets (if keyring unavailable)
- `backup_*.db.aes` - Encrypted backups

## Security Considerations

✅ **What's Secure:**
- All data encrypted at rest (AES-256)
- Encryption keys stored in OS keyring
- No cloud synchronization
- No telemetry or external calls
- SHA-256 integrity verification

⚠️ **What to Remember:**
- Master password stored in encrypted file if keyring unavailable
- Backups encrypted but stored locally
- No protection against local machine compromise
- Export backups securely if backing up to cloud

## Performance Characteristics

| Operation | Typical Time |
|-----------|------------|
| Career path analysis | < 100ms |
| Market intelligence | < 100ms |
| Database queries | < 200ms |
| Encryption/decryption | 50-200ms |
| Form parsing | 500ms-1s |
| A/B test calculation | < 100ms |

## Testing

### Test the CLI
```bash
# Test help
python applywizard.py --help

# Test init
python applywizard.py init

# Test analysis
python applywizard.py analyze --path "Data Scientist"

# Test negotiation
python applywizard.py negotiate --offer '{"salary": 200000, "company": "Apple", "role": "ML Engineer", "equity": "1%"}'

# Test wellness
python applywizard.py wellness --check 12
```

## Future Enhancements (v5.1+)

- [ ] LinkedIn profile auto-parsing
- [ ] Real-time job board scraping
- [ ] Interview prep with mock questions
- [ ] Equity calculator with vesting schedules
- [ ] Visa pathway simulator
- [ ] Tax optimization for RSU/options
- [ ] Browser extension for quick form ingestion
- [ ] API for third-party integrations
- [ ] Mobile app companion
- [ ] Team/company insights backend

## Dependencies

- `cryptography>=41.0.0` - AES-256 encryption
- `keyring>=24.0.0` - OS-level secret management

## License & Privacy

ApplyWizard v5.0 is proprietary software designed for personal career management. It respects your privacy and does not collect, store, or transmit any personal data beyond your local machine.
