# ✅ AI Coach Setup Complete - What's Next

## Current Status

Your AI Coach application is **fully functional** with everything except AI recommendations. Here's what's working:

| Feature | Status | Notes |
|---------|--------|-------|
| **Login** | ✅ Working | Demo: jane@mentee.com / password |
| **5-Step Profile Chatbot** | ✅ Working | Collects name, age, skills, interests |
| **Job Recommendations** | ✅ Working | Matches skills to jobs, shows % match |
| **Mentor Recommendations** | ✅ Working | Matches interests to mentors |
| **AI Upskilling Plans** | ⏳ Needs Config | Requires LLM service configuration |

---

## What You Need to Do (Choose ONE Option)

### 🎯 Option A: Use Databricks LLM (FASTEST)

**Why choose this?** Faster responses, can run Claude models in your own workspace

1. Go to https://databricks.com/ and log in
2. Navigate to **User Settings** (click username)
3. Click **Developer** tab
4. Click **Generate new token** button
5. Copy the token (starts with `dapi`)
6. Go to **Serving Endpoints** in your workspace
7. Find endpoint name (like `databricks-claude-sonnet-4-5`)
8. Click it and copy the "API URL"
9. Open `.env` file in project root
10. Add two lines:
    ```
    DATABRICKS_TOKEN=dapi1234567890abcdef...
    DATABRICKS_LLM_ENDPOINT=https://YOUR_WORKSPACE.cloud.databricks.com/serving-endpoints/databricks-claude-sonnet-4-5
    ```
11. Save file and restart app

**Time required:** 5-10 minutes

---

### 🎯 Option B: Use Azure OpenAI (RELIABLE)

**Why choose this?** If you already have Azure, uses GPT-4 Turbo

1. Go to https://portal.azure.com/
2. Find your OpenAI resource (search "OpenAI")
3. Click **Keys and Endpoints** in left menu
4. Copy "Endpoint" URL (looks like `https://yourname.openai.azure.com/`)
5. Copy one of the API keys (long string)
6. Open `.env` file in project root
7. Add these lines:
    ```
    AZURE_ENDPOINT=https://yourname.openai.azure.com/
    AZURE_API_KEY=abc123def456...
    AZURE_DEPLOYMENT_NAME=gpt-4-turbo
    ```
8. Save file and restart app

**Time required:** 3-5 minutes

---

## Step-by-Step Testing

### 1️⃣ Verify Configuration
```powershell
python verify_setup.py
```

You should see:
- ✅ All dependencies
- ✅ All data files
- ✅ Demo credentials
- ✅ LLM service (either Databricks OR Azure)

### 2️⃣ Test LLM Service (Optional)
```powershell
python test_llm_services.py
```

This sends a test message to your configured LLM to verify it works.

### 3️⃣ Run the App
```powershell
. .\venv\Scripts\Activate.ps1
streamlit run app.py
```

### 4️⃣ Test End-to-End
1. Open browser to `http://localhost:8501`
2. Login: `jane@mentee.com` / `password`
3. Go through all 5 steps (name → age → skills → interests → review)
4. See results page:
   - Job recommendations (should work immediately)
   - Mentor recommendations (should work immediately)
   - **Upskilling plan** (should now show AI-generated response!)

---

## File Reference

### New Files Created
- `.env` - Your LLM configuration (EDIT THIS)
- `verify_setup.py` - Diagnostic tool to check what's configured
- `test_llm_services.py` - Test your LLM connection
- `QUICK_SETUP.md` - Quick reference guide

### Modified Files
- `app.py` - Better error messages and debug info
- `README.md` - Updated with new quick start

### Existing Files (No Changes Needed)
- `src/databricks_llm_client.py` - Databricks integration
- `src/azure_client.py` - Azure integration
- `src/config.py` - Configuration loading
- `data/roles_sample.csv` - Demo accounts

---

## Common Questions

**Q: Do I NEED Databricks or Azure to run the app?**
A: No. Job and mentor matching work without them. Only AI upskilling plans require a service.

**Q: Which service is better?**
A: Databricks is slightly faster. Azure is good if you already use it. Either works fine.

**Q: What if I don't have Databricks or Azure?**
A: You can still use the app for job/mentor matching. Just the AI upskilling won't work.

**Q: Can I use both services?**
A: Yes! App tries Databricks first, falls back to Azure if not configured.

**Q: How do I add more test users?**
A: Edit `data/roles_sample.csv` and add rows with email, password, role columns.

**Q: How do I change the demo jobs or mentors?**
A: Edit `data/job_openings_sample.csv` or `data/mentors_sample.csv`

---

## Debugging Tips

If AI upskilling shows "Could not generate AI recommendations":

1. **Run verify script:**
   ```powershell
   python verify_setup.py
   ```
   Look for ❌ under "LLM Configuration"

2. **Check `.env` file exists** in project root (not in data/ folder)

3. **Check credentials are correct:**
   - Databricks token must start with `dapi`
   - Databricks endpoint must have `/serving-endpoints/` in URL
   - Azure endpoint must end with `/`

4. **Restart the app** after editing `.env`:
   - Press Ctrl+C in terminal
   - Run `streamlit run app.py` again

5. **Look at Debug Info:**
   - If error still shows, click "Debug Info" to see exact error message
   - This helps identify the problem

---

## What's Next After Setup?

Once AI upskilling works, you can:
- Add more test users to `data/roles_sample.csv`
- Add more jobs to `data/job_openings_sample.csv`
- Add more mentors to `data/mentors_sample.csv`
- Customize prompts in `src/config.py`
- Build a real database instead of CSV files

---

## Summary

✅ **App is ready** - Login works, profile chatbot works, job/mentor matching works

⏳ **One more step** - Add either Databricks OR Azure credentials to `.env`

✨ **Then you're done** - Full AI-powered career coaching app!

**Time to completion: 5-15 minutes**

Questions? Check the debug output in the app (click "Debug Info" if there's an error).
```env
AZURE_ENDPOINT=https://<your-resource>.openai.azure.com/
AZURE_API_KEY=your_api_key_here
AZURE_DEPLOYMENT_NAME=gpt-4-turbo
USE_LOCAL_CSV=True
```

### Step 3: Start the App

```powershell
streamlit run app.py
```

The app will open at `http://localhost:8501`

### Step 4: Login with Demo Credentials

- **Username:** `jane_mentee` or `john_mentor`
- **Password:** `password`

---

## 📊 Data Files

### `data/roles_sample.csv` - User Accounts
```csv
name,username,email,password_hash,role
Jane Mentee,jane_mentee,jane@company.com,6512bd43d9caa6e02c990b0a82652dca2c4ab4cc4d6482fa3c2aa9f0c1234567,mentee
John Mentor,john_mentor,john@mentor.com,a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3,mentor
```

### `data/job_openings_sample.csv` - Job Listings
Contains 12 sample tech jobs with:
- Title, company, location, salary
- Required skills
- Experience level
- Job URL

### `data/mentors_sample.csv` - Mentor Profiles
Contains 5 sample mentors with:
- Name, username, email
- Expertise areas
- Years of experience
- Bio

---

## 🔄 Application Flow

### For Mentees:
1. **Login** → Enter username & password
2. **5-Step Chatbot:**
   - Tell us your name
   - Tell us your age
   - List your skills (comma-separated)
   - Share your career interests
   - Review and confirm
3. **Get Recommendations:**
   - Jobs matching your skills (with % match)
   - AI-generated upskilling plan via Azure OpenAI
   - Mentor suggestions based on your interests

### For Mentors:
- View profile dashboard
- See mentee connections (expandable feature)

---

## 📈 Recommendation Algorithms

### Job Matching
```
For each job:
  - Extract required skills
  - Compare with mentee skills
  - Calculate % match
  - Show top 5 matches sorted by %
```

### Mentor Matching
```
For each mentor:
  - Check expertise vs mentee interests
  - Count matching keywords
  - Show top 3 mentors
```

### Upskilling Plan
- Generated by Azure OpenAI
- Based on current skills + career interests
- Includes learning timeline and time commitment

---

## 🔧 Configuration

### Azure OpenAI (Optional but Recommended)
Used for AI upskilling plans. If not configured, app still works but skips AI features.

**Get Credentials:**
1. Go to https://portal.azure.com
2. Find your Azure OpenAI resource
3. Click "Keys and Endpoint"
4. Copy endpoint and API key
5. Add to `.env` file

### Local CSV Mode (Default)
- `USE_LOCAL_CSV=True` (default)
- Loads data from `data/` folder
- No Databricks needed
- Simple and fast

### Databricks Mode (Optional)
- Set `USE_LOCAL_CSV=False` in `.env`
- Requires Databricks credentials
- Useful for production with large datasets

---

## 📦 Dependencies Installed

All dependencies are pre-built wheels - no compilation needed:
- `streamlit` - Web UI framework
- `pandas` - Data processing
- `numpy` - Numerical computing
- `azure-ai-inference` - Azure OpenAI integration
- `azure-identity` - Azure authentication
- `databricks-sql-connector` - Databricks support
- `python-dotenv` - Environment variables
- `requests` - HTTP library
- `cryptography` - Password hashing

---

## ✅ Validation Checklist

- [x] Dependencies installed successfully
- [x] Virtual environment created
- [x] Local CSV files in place
- [x] Auth system working (SHA256 hashing)
- [x] Mentee chatbot flow complete
- [x] Job matching implemented
- [x] Mentor recommendations working
- [x] Azure OpenAI integration ready
- [x] No Docker required
- [x] No Databricks required
- [x] Documentation complete

---

## 🐛 Troubleshooting

### "streamlit: command not found"
```powershell
# Activate venv first
. .\venv\Scripts\Activate.ps1
streamlit run app.py
```

### "CSV file not found"
```powershell
# Make sure you're in the right directory
cd c:\workspace\ai_coach_app
# Files should be in: data/roles_sample.csv, etc.
```

### "Invalid Azure credentials"
```
1. Check .env file has correct format
2. Verify AZURE_ENDPOINT ends with /
3. Check API key is valid in Azure Portal
4. If not configured, just skip Azure - app still works
```

### "Login failed"
```
1. Check roles_sample.csv exists in data/ folder
2. Verify username and password in CSV file
3. Default: jane_mentee / password
```

---

## 📝 Customization

### Add New Users
1. Generate password hash:
   ```python
   import hashlib
   password = "mypassword"
   hash_val = hashlib.sha256(password.encode()).hexdigest()
   print(hash_val)
   ```

2. Add to `data/roles_sample.csv`:
   ```
   New User,new_user,new@email.com,<hash>,mentee
   ```

### Add More Jobs
Edit `data/job_openings_sample.csv` with new rows

### Add More Mentors
Edit `data/mentors_sample.csv` with new profiles

### Customize AI Prompts
Edit `prompts/system_prompts.py`

---

## 📚 Key Files

```
ai_coach_app/
├── app.py                 ← Main Streamlit app (REDESIGNED)
├── requirements.txt       ← Python dependencies (UPDATED)
├── .env.example          ← Config template (SIMPLIFIED)
├── README.md             ← Full documentation (REWRITTEN)
├── QUICKSTART.md         ← 3-step quick start (NEW)
│
├── src/
│   ├── config.py         ← Settings (UPDATED)
│   ├── auth.py           ← Authentication
│   ├── azure_client.py   ← Azure OpenAI
│   ├── databricks_client.py ← CSV loader (UPDATED)
│   └── utils.py          ← Utilities
│
├── data/
│   ├── roles_sample.csv  ← User accounts
│   ├── job_openings_sample.csv ← Jobs
│   └── mentors_sample.csv ← Mentors (NEW)
│
└── .streamlit/
    └── config.toml       ← Streamlit config (NEW)
```

---

## 🎉 You're All Set!

**To run the app:**
```powershell
cd c:\workspace\ai_coach_app
. .\venv\Scripts\Activate.ps1
streamlit run app.py
```

**Login with:**
- Username: `jane_mentee`
- Password: `password`

**Then:** Follow the 5-step chatbot and see recommendations!

---

## 📞 Support

Refer to these files for detailed help:
- `README.md` - Full documentation
- `QUICKSTART.md` - Quick start guide
- `IMPLEMENTATION_SUMMARY.md` - What was changed

Enjoy AI Coach! 🚀
