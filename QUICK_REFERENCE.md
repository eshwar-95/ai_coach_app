# AI Coach - Quick Reference Guide

## 🚀 Quick Start (5 Minutes)

### Step 1: Install Dependencies
```bash
cd ai_coach_app
pip install -r requirements.txt
```

### Step 2: Configure Environment
```bash
cp .env.example .env
# Edit .env with your Azure & Databricks credentials
```

### Step 3: Verify Setup
```bash
python quickstart.py
```

### Step 4: Run Application
```bash
streamlit run app.py
# Open http://localhost:8501
```

---

## 📋 Configuration Checklist

### Azure OpenAI Setup
- [ ] Create Azure OpenAI resource in portal
- [ ] Deploy GPT-4 or GPT-4 Turbo model
- [ ] Get endpoint URL and API key
- [ ] Add to `.env` file

### Databricks Setup
- [ ] Create Databricks workspace
- [ ] Create SQL warehouse
- [ ] Create `roles` table with users
- [ ] Create `job_openings` table with jobs
- [ ] Generate personal access token
- [ ] Add credentials to `.env`

### Database Tables

**roles table** (required columns)
```sql
CREATE TABLE main.default.roles (
  id INT,
  name STRING,
  username STRING,
  email STRING,
  password_hash STRING,  -- SHA256 hash
  role STRING             -- 'mentor' or 'mentee'
);
```

**job_openings table** (required columns)
```sql
CREATE TABLE main.default.job_openings (
  id INT,
  title STRING,
  company STRING,
  description STRING,
  required_skills STRING,    -- comma-separated
  experience_level STRING,   -- 'entry-level', 'junior', 'mid-level', 'senior'
  location STRING,
  salary STRING,
  job_url STRING
);
```

---

## 🔑 Password Hash Generation

Generate SHA256 hashes for test users:

```python
import hashlib

password = "your_password"
hash_val = hashlib.sha256(password.encode()).hexdigest()
print(hash_val)
```

Example:
```
password = "password" → a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3
```

---

## 📁 Project Structure

```
ai_coach_app/
├── app.py                  # Main Streamlit app
├── requirements.txt        # Dependencies
├── .env.example           # Config template
├── src/                   # Core modules
│   ├── config.py          # Settings
│   ├── azure_client.py    # OpenAI integration
│   ├── databricks_client.py
│   ├── auth.py
│   ├── resume_parser.py
│   └── utils.py
├── prompts/
│   └── system_prompts.py  # AI prompts
├── data/
│   ├── roles_sample.csv
│   └── job_openings_sample.csv
├── README.md              # Full docs
├── SETUP_GUIDE.md         # Setup instructions
├── IMPLEMENTATION_SUMMARY.md
└── quickstart.py          # Verification script
```

---

## 💾 Environment Variables

```env
# Azure OpenAI Configuration
AZURE_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_API_KEY=sk-...
AZURE_DEPLOYMENT_NAME=gpt-4-turbo
AZURE_API_VERSION=2024-10-01-preview

# Databricks Configuration
DATABRICKS_HOST=https://your-workspace.cloud.databricks.com
DATABRICKS_TOKEN=dapi...
DATABRICKS_WAREHOUSE_ID=your-warehouse-id
DATABRICKS_CATALOG=main
DATABRICKS_SCHEMA=default

# App Configuration
APP_SECRET_KEY=your-secret-key
DEBUG=False
```

---

## 🎯 Features by Role

### Mentee Features ✅
- [ ] Create profile (name, age, skills, interests)
- [ ] Upload resume (PDF, DOCX, DOC, TXT)
- [ ] Get career assessment from AI Coach
- [ ] Find matching job openings
- [ ] Get personalized upskilling plan
- [ ] View AI recommendations

### Mentor Features (Coming Soon)
- [ ] View assigned mentees
- [ ] Track mentee progress
- [ ] Provide feedback
- [ ] Schedule sessions

---

## 🔄 Application Flow

```
START
  ↓
[Login Page]
  ├─ Email/Username + Password
  ├─ Check Databricks roles table
  └─ Verify password hash
  ↓
[Authenticated]
  ├─ User is MENTOR → Mentor Dashboard
  └─ User is MENTEE → Mentee Portal
      ↓
  [Profile Tab]
    ├─ Enter: Name, Age, Skills, Interests
    ├─ Optional: Upload Resume
    ├─ Click: Get Assessment
    └─ Display: AI Career Assessment
      ↓
  [Job Matching Tab]
    ├─ Fetch jobs from Databricks
    ├─ Filter by experience level
    ├─ Rank by skill match
    ├─ Send to Azure OpenAI for analysis
    └─ Display: Top job recommendations
      ↓
  [Upskilling Tab]
    ├─ Identify skill gaps
    ├─ Create 3-phase learning plan
    ├─ Get course recommendations
    └─ Display: Personalized roadmap
      ↓
[Logout]
```

---

## 🤖 AI Prompts Used

### 1. Job Matching Prompt
**Purpose**: Analyze jobs against mentee skills
**Features**: Match scoring, skill gap analysis, salary considerations
**Result**: Top 3-5 recommended jobs with justifications

### 2. Upskilling Prompt
**Purpose**: Create learning plans for skill development
**Features**: 3-phase structure, course links, time estimates
**Result**: Complete roadmap with courses and projects

### 3. Assessment Prompt
**Purpose**: Initial career evaluation
**Features**: Readiness level, strength identification, career paths
**Result**: Comprehensive career profile and action items

---

## 🧪 Testing Your Setup

### Quick Test
```bash
python quickstart.py
```

### Manual Tests
1. **Login Test**: Try valid credentials
2. **Profile Test**: Complete mentee profile
3. **Resume Test**: Upload a sample resume
4. **Job Test**: Click "Find Jobs"
5. **Plan Test**: Click "Create Plan"

---

## 🐛 Troubleshooting

### Login Not Working
```
Check:
1. User exists in roles table
2. Password hash matches
3. Email/username case sensitivity
4. Databricks connection working
```

### Azure OpenAI Error
```
Check:
1. AZURE_ENDPOINT is correct format
2. AZURE_API_KEY is valid
3. Model deployment exists
4. Warehouse is running
```

### Databricks Error
```
Check:
1. DATABRICKS_HOST, TOKEN, WAREHOUSE_ID
2. Warehouse is active
3. Tables exist: main.default.roles
4. Connection string is valid
```

---

## 📊 Sample Data

### Test User Logins
| Username | Password | Role |
|----------|----------|------|
| john_mentor | password | mentor |
| jane_mentee | password | mentee |

*(Hashes provided in roles_sample.csv)*

### Sample Jobs Included
- Senior Data Scientist
- Full Stack Developer
- Cloud Architect
- Junior Python Developer
- Data Analyst
- DevOps Engineer
- Frontend Developer
- Solutions Architect
- Data Engineer
- QA Automation Engineer
- Machine Learning Engineer
- Backend Developer

---

## 🔐 Security Tips

✅ **DO:**
- Keep `.env` file private
- Use strong passwords
- Rotate API keys regularly
- Use Azure Key Vault in production
- Enable warehouse security in Databricks

❌ **DON'T:**
- Commit `.env` to version control
- Share API keys or tokens
- Use simple password hashing in production
- Store credentials in code
- Leave DEBUG mode enabled

---

## 🚀 Deployment Options

### Streamlit Cloud (Free, Easy)
```bash
# Just push to GitHub and deploy via Streamlit dashboard
```

### Docker (Any Cloud)
```bash
docker build -t ai-coach .
docker run -p 8501:8501 ai-coach
```

### Cloud Platforms
- **AWS**: Use ECS + ALB
- **Azure**: Use Container Instances + Application Gateway
- **GCP**: Use Cloud Run
- **Kubernetes**: Use Helm charts

---

## 📚 Documentation Files

| File | Purpose | Read Time |
|------|---------|-----------|
| README.md | Complete feature guide | 15 min |
| SETUP_GUIDE.md | Step-by-step setup | 20 min |
| IMPLEMENTATION_SUMMARY.md | Architecture & details | 10 min |
| quickstart.py | Auto-verification | 2 min |
| This Guide | Quick reference | 5 min |

---

## 💡 Tips & Tricks

### Speed Up Testing
1. Use quickstart.py to verify configuration
2. Pre-populate test data in Databricks
3. Use Streamlit caching for data loads
4. Test Azure/Databricks separately first

### Improve Job Matching
- Add more job_openings to Databricks
- Ensure skills are consistent (lowercase, standard terms)
- Adjust skill matching threshold in `utils.py`

### Customize AI Responses
- Edit prompts in `prompts/system_prompts.py`
- Adjust TEMPERATURE in `src/config.py` (0-1)
- Increase MAX_TOKENS for longer responses

### Add More Resume Formats
- Add format to `ALLOWED_RESUME_FORMATS` in config.py
- Implement parser in `resume_parser.py`
- Test thoroughly

---

## 🔗 Useful Links

- **Streamlit Docs**: https://docs.streamlit.io
- **Azure OpenAI**: https://learn.microsoft.com/en-us/azure/ai-services/openai/
- **Databricks**: https://docs.databricks.com/
- **Python Docs**: https://docs.python.org/3/

---

## ⏱️ Common Time Estimates

| Task | Time |
|------|------|
| Install dependencies | 5 min |
| Setup Azure OpenAI | 15 min |
| Setup Databricks | 20 min |
| Configure .env | 5 min |
| Run verification | 2 min |
| First test run | 3 min |
| **Total** | **~50 min** |

---

## 📞 Getting Help

1. **Check Documentation**: README.md, SETUP_GUIDE.md
2. **Review Logs**: Check Streamlit terminal output
3. **Verify Configuration**: Run `python quickstart.py`
4. **Test Components**: Test Azure and Databricks separately
5. **Review Code**: Comments explain key functions

---

## ✨ What's Included

✅ Complete Streamlit application
✅ Azure OpenAI integration
✅ Databricks SQL integration
✅ Resume parsing (PDF, DOCX, TXT)
✅ Role-based authentication
✅ AI-powered career assessment
✅ Intelligent job matching
✅ Personalized upskilling plans
✅ 12 sample jobs
✅ 2 sample users
✅ Complete documentation
✅ Setup verification script
✅ System prompts for 3 features
✅ Utility functions
✅ Error handling & validation

---

**Status**: ✅ Ready to Deploy
**Last Updated**: January 28, 2026
**Version**: 1.0
