# AI Coach - Career Guidance Platform

A Streamlit application that provides personalized career coaching using Azure OpenAI and local CSV data files.

## 🎯 Features

### Authentication
- Simple login with username/email and password
- Role-based access (Mentor/Mentee)
- SHA256 password hashing
- Session management

### Mentee Flow
1. **Interactive Chatbot Profile Collection**
   - Name
   - Age
   - Technical and professional skills
   - Career interests
   - Instant confirmation

2. **Smart Job Recommendations**
   - Matches mentee skills against job openings
   - Shows skill match percentage
   - Displays job details with apply links

3. **AI-Powered Upskilling Plans**
   - Personalized learning roadmap
   - Top skills to learn next
   - Learning timeline (short/medium/long-term)
   - Time commitment estimates

4. **Mentor Recommendations**
   - Matches mentors based on mentee interests
   - Shows mentor expertise and experience
   - One-click connection requests

### Mentor Dashboard
- View profile
- Connect with mentees (placeholder for now)

## 🚀 Quick Start

### 1. Setup & Verification (30 seconds)

```powershell
# Activate virtual environment
. .\venv\Scripts\Activate.ps1

# Run setup verification
python verify_setup.py
```

This shows what's configured and what's missing.

### 2. Configure AI Service (2-5 minutes)

**Option A: Databricks LLM** (Recommended)
- Get token from https://databricks.com/ (User Settings → Access Tokens)
- Get endpoint from Serving Endpoints in Databricks workspace
- Edit `.env` file:
  ```env
  DATABRICKS_TOKEN=dapi...
  DATABRICKS_LLM_ENDPOINT=https://...
  ```

**Option B: Azure OpenAI** (Fallback)
- Get credentials from Azure Portal (OpenAI resource → Keys and Endpoints)
- Edit `.env` file:
  ```env
  AZURE_ENDPOINT=https://...
  AZURE_API_KEY=...
  ```

### 3. Run the App (30 seconds)

```powershell
# Activate virtual environment
. .\venv\Scripts\Activate.ps1

# Run app
streamlit run app.py
```

The app opens at `http://localhost:8501`

### 4. Login & Test

**Demo Credentials:**
| Email | Password | Role |
|-------|----------|------|
| jane@mentee.com | password | Mentee |
| john@mentor.com | password | Mentor |
| alice@company.com | password | Mentee |

**Test the Flow:**
1. Login with any demo account
2. Complete the 5-step profile chatbot
3. View job & mentor recommendations (AI-free)
4. See AI-generated upskilling plan (requires configured LLM)

## 📊 Troubleshooting

Run these commands in order if something doesn't work:

```powershell
# 1. Verify everything is installed correctly
python verify_setup.py

# 2. Test LLM services (if configured)
python test_llm_services.py

# 3. If still having issues, check the debug info
# - App will show "Debug Info" expandable section if there's an error
# - Check what error message is displayed
```

**Common Issues:**
- **"Could not generate AI recommendations"**: Configure DATABRICKS or AZURE credentials in `.env`
- **"Invalid credentials" at login**: Use demo credentials above or update `data/roles_sample.csv`
- **Module not found**: Run `pip install -r requirements.txt` inside activated venv

## 📁 Project Structure

```
ai_coach_app/
├── app.py                      # Main Streamlit app
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
│
├── src/
│   ├── __init__.py
│   ├── config.py              # Configuration & constants
│   ├── auth.py                # Authentication manager
│   ├── azure_client.py        # Azure OpenAI integration
│   ├── databricks_client.py   # CSV file data loading
│   ├── resume_parser.py       # Resume parsing (unused in chatbot mode)
│   └── utils.py               # Utility functions
│
├── data/
│   ├── roles_sample.csv       # User accounts (mentors & mentees)
│   ├── job_openings_sample.csv # Job listings
│   └── mentors_sample.csv     # Mentor profiles
│
├── prompts/
│   └── system_prompts.py      # AI prompt templates
│
└── README.md                  # This file
```

## 📊 Data Files

### roles_sample.csv
User accounts for login. Format:
```
name,username,email,password_hash,role
Jane Mentee,jane_mentee,jane@company.com,6512bd43d9caa6e02c990b0a82652dca2c4ab4cc4d6482fa3c2aa9f0c1234567,mentee
John Mentor,john_mentor,john@mentor.com,a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3,mentor
```

**Password for demo users:** `password`

To create your own user with a different password:
```python
import hashlib
password = "mypassword"
hash_val = hashlib.sha256(password.encode()).hexdigest()
print(hash_val)
# Add this hash to roles_sample.csv
```

### job_openings_sample.csv
Job listings that mentees will match against. Format:
```
title,company,description,required_skills,experience_level,location,salary,job_url
Senior Data Scientist,TechCorp,Lead ML initiatives,"Python, ML, TensorFlow, AWS",senior,San Francisco CA,150000-200000,https://example.com/job1
```

### mentors_sample.csv
Mentor profiles for recommendations. Format:
```
name,username,email,expertise,experience_years,bio
John Mentor,john_mentor,john@mentor.com,"Data Science, ML, Python",8,"Passionate about machine learning and mentoring junior data scientists."
```

## 🔧 Configuration

### Using Azure OpenAI

The app integrates with Azure OpenAI for:
- Upskilling plan generation
- Job match analysis
- Career recommendations

If Azure is not configured, the app still works but skips AI-powered features.

### Using Local Data

By default, the app loads data from CSV files in the `data/` folder:
- `roles_sample.csv` - User authentication
- `job_openings_sample.csv` - Job listings
- `mentors_sample.csv` - Mentor profiles

No Databricks account needed!

## 🐛 Troubleshooting

### "streamlit: command not found"
```bash
# Install streamlit explicitly
pip install streamlit

# Or reinstall all dependencies
pip install -r requirements.txt
```

### "ModuleNotFoundError: No module named 'src'"
Make sure you're running from the project root directory:
```bash
cd ai_coach_app
streamlit run app.py
```

### "Invalid Azure credentials" or API errors
1. Verify your `.env` file has correct credentials
2. Check that `AZURE_ENDPOINT` ends with a trailing slash: `https://...openai.azure.com/`
3. Verify your API key is valid in Azure Portal
4. Confirm the deployment name matches your actual Azure deployment

### "CSV file not found"
1. Check that CSV files are in the `data/` folder
2. Make sure filenames match exactly (case-sensitive on Linux/Mac):
   - `roles_sample.csv`
   - `job_openings_sample.csv`
   - `mentors_sample.csv`

### App is slow or hanging
- Azure API calls can take 10-30 seconds
- This is normal for GPT-4 Turbo
- For faster responses, use `gpt-35-turbo` in `.env`

### "Logout button not appearing"
Try refreshing the page (F5) or clearing browser cache

## 🔐 Security Notes

- Passwords are hashed with SHA256 (for demo only)
- In production, use bcrypt or argon2
- Keep `.env` file out of version control
- Store Azure API keys in secure secret managers (Azure Key Vault, etc.)
- Rotate API keys periodically

## 📝 Adding More Data

### Add More Users
Edit `data/roles_sample.csv`:
```python
# Generate password hash
import hashlib
password = "secure_password"
hash_val = hashlib.sha256(password.encode()).hexdigest()
print(hash_val)
```

Then add to CSV:
```
New User,new_user,new@email.com,<hash_value>,mentee
```

### Add More Job Openings
Edit `data/job_openings_sample.csv` with new rows. Make sure to match the column format.

### Add More Mentors
Edit `data/mentors_sample.csv` with new mentor profiles.

## 🎓 How It Works

1. **Login Page**: Users authenticate against `roles_sample.csv`

2. **Mentee Flow** (Interactive Chatbot):
   - Step 1: Ask for name
   - Step 2: Ask for age
   - Step 3: Ask for skills (comma-separated)
   - Step 4: Ask for career interests
   - Step 5: Show confirmation and get recommendations

3. **Recommendations**:
   - **Job Matches**: Skills are compared to job requirements using simple string matching
   - **Upskilling Plan**: Azure OpenAI generates personalized learning path
   - **Mentor Suggestions**: Mentors are matched based on their expertise and mentee interests

4. **Mentor Dashboard**: Simple placeholder for mentor features

## 🚀 Running on Different Systems

### Windows (PowerShell)
```powershell
# Create virtual environment
python -m venv venv

# Activate
.\venv\Scripts\Activate.ps1

# Install and run
pip install -r requirements.txt
streamlit run app.py
```

### macOS/Linux (Bash)
```bash
# Create virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate

# Install and run
pip install -r requirements.txt
streamlit run app.py
```

## 📚 System Prompts

The app uses simple, template-based prompts for Azure OpenAI:

### Upskilling Prompt
Generates personalized learning plans based on:
- Current skills
- Career interests
- Age and experience level

### Job Matching Prompt
Analyzes job fit based on:
- Mentee skills
- Experience level
- Career interests

See `prompts/system_prompts.py` for full prompt templates.

## 🔄 Future Enhancements

- [ ] Mentor-mentee messaging
- [ ] Progress tracking dashboard
- [ ] Email notifications
- [ ] Resume upload and parsing
- [ ] Interview preparation modules
- [ ] Salary negotiation guides
- [ ] LinkedIn integration
- [ ] Multi-language support

## 📞 Support

1. Check the **Troubleshooting** section above
2. Verify `.env` configuration
3. Check terminal logs for error messages
4. Ensure all CSV files exist in `data/` folder
5. Verify Azure credentials in Azure Portal

## 📄 License

This project is provided as-is for educational and commercial use.

## 🎯 Key Technologies

- **Streamlit** - Web UI framework
- **Azure OpenAI** - LLM for recommendations
- **Pandas** - Data processing
- **Python 3.8+** - Programming language

Enjoy using AI Coach! 🚀
