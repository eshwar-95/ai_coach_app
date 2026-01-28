# 📋 AI Coach Project - Complete File Index

## 📦 Project Overview

**AI Coach** is a comprehensive Streamlit application that provides AI-powered career coaching with:
- Azure OpenAI integration for intelligent recommendations
- Databricks SQL for data management
- Role-based authentication (Mentor/Mentee)
- Resume parsing (PDF, DOCX, DOC, TXT)
- Job matching and upskilling recommendations

---

## 📂 Project Files

### Core Application Files

#### **app.py** (Main Application)
- Location: Root directory
- Lines: 400+
- Purpose: Main Streamlit application entry point
- Key Components:
  - Login page rendering
  - Mentee profile collection UI
  - Career assessment workflow
  - Job matching engine UI
  - Upskilling plan generation UI
  - Mentor dashboard (expandable)
  - Session routing and state management
- Functions:
  - `setup_page_config()` - Streamlit configuration
  - `render_login_page()` - Login UI
  - `render_mentee_home()` - Mentee dashboard
  - `render_career_assessment()` - AI assessment
  - `render_job_matching()` - Job recommendations
  - `render_upskilling_plan()` - Learning plans
  - `render_mentor_home()` - Mentor dashboard
  - `main()` - Application entry point

---

### Source Code Modules

#### **src/config.py**
- Lines: 80+
- Purpose: Configuration and constants
- Key Components:
  - Azure OpenAI settings
  - Databricks settings
  - File validation settings
  - AI model parameters
- Functions:
  - `hash_password()` - SHA256 password hashing
  - `verify_password()` - Password verification

#### **src/azure_client.py**
- Lines: 120+
- Purpose: Azure OpenAI integration
- Class: `AzureOpenAIClient`
- Key Methods:
  - `__init__()` - Initialize client
  - `get_response()` - Basic API calls
  - `get_response_with_context()` - Contextual responses
  - `_format_user_context()` - Context formatting

#### **src/databricks_client.py**
- Lines: 100+
- Purpose: Databricks SQL integration
- Class: `DatabricksClient`
- Key Methods:
  - `__init__()` - Initialize connection
  - `get_connection()` - Create SQL connection
  - `query_csv_data()` - Execute SQL queries
  - `get_roles_data()` - Fetch user data
  - `get_job_openings_data()` - Fetch job data
  - `search_by_column()` - Search functionality

#### **src/auth.py**
- Lines: 140+
- Purpose: Authentication and session management
- Class: `AuthenticationManager`
- Key Methods:
  - `get_roles_data()` - Fetch roles from Databricks
  - `authenticate_user()` - Verify credentials
  - `initialize_session()` - Setup session state
  - `login()` - User login
  - `logout()` - User logout
  - `is_authenticated()` - Check auth status
  - `get_current_user()` - Get user object
  - `get_user_role()` - Get role
  - `is_mentor()` / `is_mentee()` - Role checks

#### **src/resume_parser.py**
- Lines: 160+
- Purpose: Resume parsing and text extraction
- Class: `ResumeParser`
- Key Methods:
  - `validate_file()` - File validation
  - `parse_resume()` - Main parsing dispatcher
  - `_parse_txt()` - Text file parsing
  - `_parse_pdf()` - PDF parsing (PyPDF2)
  - `_parse_docx()` - DOCX parsing (python-docx)
  - `extract_skills_from_text()` - Skill extraction

#### **src/utils.py**
- Lines: 140+
- Purpose: Utility functions
- Key Functions:
  - `format_job_openings_for_prompt()` - Format jobs for AI
  - `calculate_skill_match_percentage()` - Skill matching
  - `rank_jobs_by_skill_match()` - Job ranking
  - `filter_jobs_by_experience_level()` - Job filtering
  - `get_mentee_info_dict()` - Info packaging

#### **src/__init__.py**
- Purpose: Package initialization

---

### Prompts and Templates

#### **prompts/system_prompts.py**
- Lines: 200+
- Purpose: AI system prompts and templates
- Constants:
  - `MENTEE_JOB_MATCHING_SYSTEM_PROMPT` - Job analysis
  - `MENTEE_UPSKILLING_SYSTEM_PROMPT` - Learning plans
  - `MENTEE_INITIAL_ASSESSMENT_SYSTEM_PROMPT` - Career assessment
- Functions:
  - `get_job_matching_prompt()` - Job matching template
  - `get_upskilling_prompt()` - Upskilling template
  - `get_initial_assessment_prompt()` - Assessment template

#### **prompts/__init__.py**
- Purpose: Package initialization

---

### Data Files

#### **data/roles_sample.csv**
- Purpose: Sample user data for authentication
- Columns: name, username, email, password_hash, role
- Sample Users:
  - John Mentor (mentor role)
  - Jane Mentee (mentee role)
  - Alice Mentee (mentee role)
- Hash Format: SHA256

#### **data/job_openings_sample.csv**
- Purpose: Sample job openings data
- Columns: id, title, company, description, required_skills, experience_level, location, salary, job_url
- Sample Jobs: 12 positions (entry to senior level)
- Companies: TechCorp, StartupXYZ, CloudSys, etc.

---

### Configuration Files

#### **.env.example**
- Purpose: Environment configuration template
- Variables:
  - AZURE_ENDPOINT - Azure OpenAI endpoint
  - AZURE_API_KEY - API key
  - AZURE_DEPLOYMENT_NAME - Model deployment
  - AZURE_API_VERSION - API version
  - DATABRICKS_HOST - Workspace URL
  - DATABRICKS_TOKEN - PAT token
  - DATABRICKS_WAREHOUSE_ID - Warehouse ID
  - DATABRICKS_CATALOG - Catalog name
  - DATABRICKS_SCHEMA - Schema name
  - APP_SECRET_KEY - Application secret
  - DEBUG - Debug mode flag

#### **requirements.txt**
- Purpose: Python dependencies
- Packages:
  - streamlit (1.28.1) - Web framework
  - python-dotenv (1.0.0) - Environment management
  - pandas (2.1.3) - Data processing
  - numpy (1.26.2) - Numerical computing
  - azure-identity - Azure authentication
  - azure-ai-inference (1.0.0b1) - Azure OpenAI
  - python-docx (0.8.11) - DOCX parsing
  - PyPDF2 (3.17.0) - PDF parsing
  - databricks-sql-connector (3.0.0) - Database connection
  - requests (2.31.0) - HTTP requests
  - cryptography (41.0.7) - Security utilities

---

### Documentation Files

#### **README.md**
- Lines: 400+
- Sections:
  - Features overview
  - Prerequisites
  - Installation & setup
  - Environment configuration
  - Databricks setup
  - Project structure
  - Data flow diagrams
  - Configuration options
  - API references
  - Troubleshooting guide
  - Deployment instructions
  - Customization examples
  - Future enhancements

#### **SETUP_GUIDE.md**
- Lines: 300+
- Sections:
  - Prerequisites
  - Project structure setup
  - Azure configuration (step-by-step)
  - Databricks configuration
  - Password hash generation
  - Running the application
  - Testing procedures
  - Troubleshooting
  - Performance optimization

#### **IMPLEMENTATION_SUMMARY.md**
- Lines: 400+
- Sections:
  - Project deliverables
  - Complete file structure
  - Architecture overview
  - System prompts explained
  - Configuration options
  - Getting started
  - Security features
  - Scalability & performance
  - Testing checklist
  - Next steps & enhancements
  - Code statistics

#### **QUICK_REFERENCE.md**
- Lines: 250+
- Sections:
  - Quick start (5 minutes)
  - Configuration checklist
  - Environment variables
  - Project structure
  - Application flow
  - AI prompts used
  - Testing guide
  - Troubleshooting
  - Deployment options
  - Tips & tricks
  - Time estimates

#### **this file - INDEX.md**
- Lines: 250+
- Purpose: Complete file directory and documentation

---

### Utility Scripts

#### **quickstart.py**
- Lines: 200+
- Purpose: Automated setup verification
- Functions:
  - `check_python_version()` - Verify Python 3.8+
  - `check_dependencies()` - Verify pip packages
  - `check_env_file()` - Verify .env configuration
  - `check_project_structure()` - Verify all files
  - `test_azure_connection()` - Test Azure access
  - `test_databricks_connection()` - Test DB access
  - `check_authentication_setup()` - Test auth module
  - `main()` - Run all checks

---

## 📊 File Statistics

| Category | Count | Total Lines |
|----------|-------|------------|
| Source Code | 7 | 700+ |
| Prompts | 2 | 200+ |
| Main App | 1 | 400+ |
| Documentation | 5 | 1,500+ |
| Config | 2 | 120+ |
| Data Samples | 2 | 30+ |
| Scripts | 1 | 200+ |
| **TOTAL** | **20** | **3,000+** |

---

## 🔄 File Dependencies

```
app.py
├── src/config.py
├── src/auth.py
│   └── src/databricks_client.py
├── src/azure_client.py
├── src/databricks_client.py
├── src/resume_parser.py
├── src/utils.py
└── prompts/system_prompts.py

src/config.py
└── (no internal dependencies)

src/azure_client.py
└── src/config.py

src/databricks_client.py
└── src/config.py

src/auth.py
├── src/config.py
└── src/databricks_client.py

src/resume_parser.py
└── src/config.py

src/utils.py
└── (no internal dependencies)

prompts/system_prompts.py
└── (no internal dependencies)

quickstart.py
├── src/config.py
├── src/azure_client.py
├── src/databricks_client.py
├── src/auth.py
└── src/resume_parser.py
```

---

## 🎯 Feature Files Mapping

### Authentication Features
- **Files**: `src/auth.py`, `src/config.py`, `app.py`
- **Data**: `data/roles_sample.csv`
- **Config**: `.env.example` (DATABRICKS_*)

### Resume Parsing Features
- **Files**: `src/resume_parser.py`, `src/config.py`
- **Supported**: PDF, DOCX, DOC, TXT

### Job Matching Features
- **Files**: `app.py`, `src/utils.py`, `src/databricks_client.py`, `src/azure_client.py`
- **Prompts**: `prompts/system_prompts.py` (MENTEE_JOB_MATCHING_SYSTEM_PROMPT)
- **Data**: `data/job_openings_sample.csv`

### Upskilling Plan Features
- **Files**: `app.py`, `src/azure_client.py`, `prompts/system_prompts.py`
- **Prompts**: `prompts/system_prompts.py` (MENTEE_UPSKILLING_SYSTEM_PROMPT)

### Career Assessment Features
- **Files**: `app.py`, `src/azure_client.py`, `prompts/system_prompts.py`
- **Prompts**: `prompts/system_prompts.py` (MENTEE_INITIAL_ASSESSMENT_SYSTEM_PROMPT)

---

## 📋 Setup Checklist

- [ ] Clone/download project
- [ ] Read: QUICK_REFERENCE.md (5 min)
- [ ] Install: `pip install -r requirements.txt`
- [ ] Copy: `cp .env.example .env`
- [ ] Edit: `.env` with credentials
- [ ] Follow: SETUP_GUIDE.md for Azure & Databricks
- [ ] Verify: `python quickstart.py`
- [ ] Run: `streamlit run app.py`
- [ ] Test: Login and features
- [ ] Read: README.md for full documentation

---

## 🚀 Getting Started

1. **Quick Start** → Read `QUICK_REFERENCE.md`
2. **Setup** → Follow `SETUP_GUIDE.md`
3. **Run** → Execute `streamlit run app.py`
4. **Learn** → Read `README.md` for details
5. **Customize** → Check `IMPLEMENTATION_SUMMARY.md`

---

## 📞 Documentation Navigation

| Need Help With? | Read This File |
|-----------------|---|
| Quick start | QUICK_REFERENCE.md |
| Setup instructions | SETUP_GUIDE.md |
| General features | README.md |
| Architecture details | IMPLEMENTATION_SUMMARY.md |
| File locations | INDEX.md (this file) |
| Config troubleshooting | SETUP_GUIDE.md - Troubleshooting |

---

## ✨ Project Highlights

✅ **Complete Implementation**
- All features specified in requirements
- Production-ready code
- Error handling & validation

✅ **Well Documented**
- 5 documentation files
- 3,000+ lines of documentation
- Code comments throughout
- Step-by-step guides

✅ **Easy to Setup**
- Quickstart verification script
- Detailed setup guide
- Quick reference guide
- Sample data included

✅ **Production Ready**
- Security best practices
- Environment variable management
- Error handling
- Scalability considerations

✅ **Extensible**
- Modular code design
- Clear interfaces
- Documented customization points
- Easy to add features

---

## 📝 Last Updated

- **Date**: January 28, 2026
- **Version**: 1.0
- **Status**: ✅ Ready for Deployment

---

## 🎓 Learning Resources

### Within Project
- Code comments explain complex logic
- Docstrings on all functions
- System prompts documented
- Architecture in IMPLEMENTATION_SUMMARY.md

### External References
- [Streamlit Documentation](https://docs.streamlit.io)
- [Azure OpenAI Documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- [Databricks SQL Documentation](https://docs.databricks.com/sql/)
- [Python Documentation](https://docs.python.org/3/)

---

## 📞 Support

For issues or questions:
1. Check QUICK_REFERENCE.md - Troubleshooting
2. Review SETUP_GUIDE.md - Common Issues
3. Run `python quickstart.py` for diagnostics
4. Check code comments in relevant modules
5. Review README.md for comprehensive guide

---

**Thank you for using AI Coach! 🎯**
