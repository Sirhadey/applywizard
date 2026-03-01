# ApplyWizard v5.0 - Interactive Workflow Guide

## Complete Example Workflow

This guide demonstrates the four new interactive commands added to ApplyWizard v5.0 for streamlined job application management.

---

## 🔄 Workflow Step 1: Switch Career Context

When pivoting to a new role type or target industry, use `--switch`:

```bash
applywizard switch --switch "Senior_Dev_Role"
```

**Output:**
```
[ApplyWizard] 🔄 Switching career context to: 'Senior_Dev_Role'
✅ Career context switched to: Senior_Dev_Role

📋 Available contexts:
  • Senior_Dev_Role (ACTIVE)
```

**What this does:**
- Activates a new career context (role title, target skills, companies, salary expectations)
- Scopes all subsequent operations to this context
- Enables A/B testing different career paths

**Real-world usage:**
- Switching from "Full-Stack Engineer" to "DevOps Engineer"
- Pivoting from "Data Analyst" to "ML Engineer"
- Testing "Startup Founder" vs "Big Tech" career paths

---

## 🔍 Workflow Step 2: Find Jobs with Filters

Search for opportunities matching your criteria:

```bash
applywizard find --find "Remote Python Engineer" --min-salary 120000
```

**Output:**
```
[ApplyWizard] 🔍 Searching for jobs: 'Remote Python Engineer'
   Min Salary: $120,000

📊 Found 1 matching jobs:

1. Remote Python Engineer
   Company: Monzo | Location: Remote (UK)
   Salary: $120,000 - $160,000
   Tech Stack: Python, Django, PostgreSQL
   Remote: ✓
   ID: JOB002
```

**Supported filters:**
- `--find "keyword"` - Search title/company (required)
- `--min-salary 120000` - Minimum salary threshold
- `--max-salary 200000` - Maximum salary threshold
- `--remote` - Remote positions only

**Real-world usage:**
```bash
# Find senior roles at higher salary
applywizard find --find "Senior Python Engineer" --min-salary 180000

# Find remote-only opportunities
applywizard find --find "Python Developer" --remote

# Find within salary band
applywizard find --find "Full-Stack Engineer" --min-salary 130000 --max-salary 180000

# Find at specific company
applywizard find --find "Stripe"
```

---

## 📝 Workflow Step 3: Prepare Application Materials

Generate tailored resume + custom pitch for a specific job:

```bash
applywizard prep JOB002
```

**Output:**
```
[ApplyWizard] 📝 Preparing materials for job: JOB002

Job: Remote Python Engineer at Monzo

📋 Generating tailored resume...
✅ Tailored resume generated successfully
   📁 resume_JOB002_Monzo_tailored.txt

💬 Generating custom pitch...
✅ Custom pitch generated successfully
   📁 pitch_Monzo_20260228_230331.txt

✅ All materials ready! Status: prep-complete

📂 Documents saved to: /home/elliot/.applywizard/generated_documents
```

**Generated files:**
1. `resume_[JOB_ID]_[COMPANY]_tailored.txt` - Tailored resume
   - Emphasizes relevant tech stack
   - Reorders experience to match job priorities
   - Includes integrity verification note (Hallucination Guard)

2. `pitch_[COMPANY]_[TIMESTAMP].txt` - Custom pitch
   - 30-second elevator pitch
   - 1-2 minute extended version
   - LinkedIn outreach hook
   - Interview talking points
   - Questions to ask interviewer

**What happens behind the scenes:**
- Resume integrity verified (Hallucination Guard)
- Compatibility score calculated (85% in this example)
- Job tracking initiated
- Materials audited for factual accuracy
- Status set to "prep-complete"

**Usage tips:**
- Copy resume pitch directly to LinkedIn/email
- Use generated talking points in interviews
- Keep questions handy for calls
- All generated materials saved locally for privacy

---

## 📋 Workflow Step 4: Track Application Status

Update the status of tracked applications:

```bash
applywizard status JOB002 "Interview Scheduled"
```

**Output:**
```
[ApplyWizard] 📋 Updating job status: JOB002 → Interview Scheduled
✅ Job status updated to: Interview Scheduled
   Job ID: JOB002
   Status: Interview Scheduled
   Updated: 2026-02-28 23:03:37
```

**Common status flows:**
```
found → prep-complete → applied → interview → offer → accepted
                    ↓
                rejected (any stage)
```

**Real-world workflow:**

```bash
# Step 1: Find job
applywizard find --find "Senior Engineer" --min-salary 150000

# Step 2: Prepare materials
applywizard prep JOB003

# Step 3: Submit application
applywizard status JOB003 "applied"

# Step 4: Got response
applywizard status JOB003 "responded"

# Step 5: Interview scheduled
applywizard status JOB003 "Interview Scheduled"

# Step 6: Interview completed
applywizard status JOB003 "Interview Round 1 Complete"

# Step 7: Offer received
applywizard status JOB003 "offer"

# Step 8: Run negotiation
applywizard negotiate --offer '{"salary": 180000, "company": "X", "role": "Senior Engineer", "equity": "0.5%"}'

# Step 9: Update final status
applywizard status JOB003 "offer accepted"
```

---

## Complete Example: Full Day Workflow

Here's a realistic daily workflow using all features:

```bash
# Morning: Switch to target role
applywizard switch --switch "Remote_Senior_Python_Dev"

# Find remote Python opportunities (min $140k)
applywizard find --find "Remote Python Engineer" --min-salary 140000
# Result: Found 2 jobs

# Prep materials for first job
applywizard prep JOB002  # Monzo
# Generated: resume + pitch

# Mark as applied
applywizard status JOB002 "applied"

# Check market trends
applywizard market --trends

# Analyze career path
applywizard analyze --path "Python Developer"

# Check wellness (applied to 4 jobs so far)
applywizard wellness --check 4

# Afternoon: Prep for second job
applywizard prep JOB005  # Databricks
# Generated: resume + pitch

# Mark as applied
applywizard status JOB005 "applied"

# Evening: Got callback from Monzo
applywizard status JOB002 "Interview Scheduled"

# Run negotiation prep for potential Monzo offer:
applywizard negotiate --offer '{"salary": 140000, "company": "Monzo", "role": "Senior Python Engineer", "equity": "0.15%"}'

# Create encrypted backup
applywizard backup
```

---

## Data Storage & Privacy

All materials are stored locally:
- **Resumes:** `~/.applywizard/generated_documents/resume_*.txt`
- **Pitches:** `~/.applywizard/generated_documents/pitch_*.txt`
- **Database:** `~/.applywizard/careerdata.db` (encrypted)
- **Backups:** `~/.applywizard/backup_*.db.aes` (AES-256 encrypted)

### Privacy Features:
✅ No cloud storage  
✅ No external API calls  
✅ No tracking or analytics  
✅ Encrypted backups  
✅ Local-only processing  

---

## Command Reference

| Command | Syntax | Purpose | Output |
|---------|--------|---------|--------|
| `switch` | `applywizard switch --switch "RoleName"` | Switch career context | Activates context |
| `find` | `applywizard find --find "query" [filters]` | Search jobs | Matching jobs with scores |
| `prep` | `applywizard prep JOB_ID` | Generate materials | Resume + Pitch files |
| `status` | `applywizard status JOB_ID "new_status"` | Update application status | Confirmation with timestamp |

---

## Integration with Other Commands

These new commands work alongside existing ApplyWizard features:

```bash
# Find + Prepare + Negotiate complete workflow
applywizard find --find "Senior Engineer" --min-salary 180000
applywizard prep JOB001
applywizard status JOB001 "applied"
# (Assume application successful after interview)
applywizard negotiate --offer '{"salary": 200000, "company": "X", "role": "Senior Engineer"}'

# Career planning + Job search
applywizard analyze --path "Current Role"      # See next steps
applywizard find --find "Next Step Role"       # Find matching jobs
applywizard tailor --persona "startup"         # Tailor resume
applywizard prep JOB_ID                        # Prepare

# Wellness + Application tracking
applywizard wellness --check 6                 # Check burnout
applywizard find --find "Senior Engineer"      # Search
applywizard prep JOB_ID                        # Prepare
applywizard wellness --check 8                 # Check again if necessary
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Job not found | Verify job ID exists. Use `find` first to get IDs. |
| Resume generation fails | Check sample_resume.txt exists in ~/.applywizard/ |
| Status update fails | Job must exist in database first. Use `prep` to track. |
| Documents not saved | Verify ~/.applywizard/generated_documents/ has write permissions |

---

## Next Steps

1. **Daily usage:** Integrate into your job search routine
2. **A/B testing:** Try different personas and track response rates
3. **Automation:** Create shell scripts for common workflows
4. **Tracking:** Monitor applications through to offer stage
5. **Backup:** Run `applywizard backup` weekly for security

---

**Remember:** ApplyWizard is your strategic partner. Use it to be intentional, data-driven, and stress-free in your job search. 🚀
