# 🎯 AI Coach - Complete Setup Guide

## 📋 Quick Navigation

**Just want to get started?** → Read **QUICK_SETUP.md** (3 min read)

**Need detailed help?** → Read **SETUP_COMPLETE.md** (10 min read)

**Running into issues?** → Use `python verify_setup.py` (automatic diagnosis)

---

## 🚀 30-Second Start

```powershell
# 1. Verify setup (shows what's configured)
python verify_setup.py

# 2. Configure .env (edit file with your LLM credentials)
# Option A: Databricks - https://databricks.com/ → User Settings → Access Tokens
# Option B: Azure - https://portal.azure.com/ → OpenAI resource → Keys and Endpoints

# 3. Run app
. .\venv\Scripts\Activate.ps1
streamlit run app.py

# 4. Login with: jane@mentee.com / password
```

That's it! App works at http://localhost:8501

---

## 📚 Documentation Files

| File | Purpose | Read Time |
|------|---------|-----------|
| **QUICK_SETUP.md** | Fast setup instructions | 3 min |
| **SETUP_COMPLETE.md** | Detailed configuration guide | 10 min |
| **README.md** | Full feature overview | 5 min |
| **DATABRICKS_SETUP.md** | Databricks-specific instructions | 5 min |
| **This file** | Navigation and overview | 2 min |

---

## 🔧 Diagnostic Tools

### Check Setup Status
```powershell
python verify_setup.py
```
- Shows what's installed ✅
- Shows what's configured ✅
- Shows what needs attention ⚠️

### Test LLM Connection
```powershell
python test_llm_services.py
```
- Tests Databricks connection (if configured)
- Tests Azure connection (if configured)
- Shows exact error messages if something fails

---

## 🎯 Your Next Steps

### ✅ Already Done For You
- ✅ App architecture simplified (local CSV, no Docker)
- ✅ All dependencies installed
- ✅ Authentication system working
- ✅ Job/mentor matching implemented
- ✅ Streamlit UI built and tested
- ✅ Fallback error handling implemented

### ⏳ You Need to Do (5-15 minutes)

**Choose ONE of these options:**

#### Option A: Databricks LLM (Recommended)
1. Visit https://databricks.com/
2. Go to User Settings → Developer → Generate Token
3. Copy the token (dapi...)
4. Go to Serving Endpoints, copy endpoint URL
5. Edit `.env` file:
   ```
   DATABRICKS_TOKEN=dapi...
   DATABRICKS_LLM_ENDPOINT=https://...
   ```
6. Restart app

#### Option B: Azure OpenAI
1. Visit https://portal.azure.com/
2. Go to OpenAI resource → Keys and Endpoints
3. Copy endpoint and API key
4. Edit `.env` file:
   ```
   AZURE_ENDPOINT=https://...
   AZURE_API_KEY=...
   ```
5. Restart app

### ✨ Then You're Done!
- Full chatbot flow working ✅
- AI recommendations generating ✅
- Production-ready app ✅

---

## 📊 What Works (& What Doesn't Yet)

| Feature | Status | Details |
|---------|--------|---------|
| Login | ✅ | Works with demo accounts |
| Profile Chatbot | ✅ | Collects all user info |
| Job Matching | ✅ | No AI needed, instant |
| Mentor Matching | ✅ | No AI needed, instant |
| AI Upskilling | ⏳ | Needs LLM config |

---

## 🎓 Demo Credentials

Use these to test:

```
Email:    jane@mentee.com
Password: password
Role:     Mentee
```

Other demo accounts:
- john@mentor.com / password (Mentor)
- alice@company.com / password (Mentee)

---

## 🆘 Common Issues & Solutions

### Problem: "Could not generate AI recommendations"
**Solution:** Run `python verify_setup.py` to check configuration

### Problem: "Invalid credentials" at login
**Solution:** Use demo credentials above, or edit `data/roles_sample.csv`

### Problem: "Module not found" errors
**Solution:** 
```powershell
. .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Problem: App won't start
**Solution:** 
1. Check virtual environment is activated
2. Check `.env` file exists in project root
3. Run `python verify_setup.py` to diagnose

---

## 📁 Project Structure

```
ai_coach_app/
├── app.py                           # Main app (ready to run)
├── verify_setup.py                  # ✅ Diagnostic tool
├── test_llm_services.py             # ✅ LLM tester
├── .env                             # ✅ Configure this!
├── requirements.txt                 # All dependencies
│
├── README.md                        # Feature overview
├── QUICK_SETUP.md                   # Fast guide
├── SETUP_COMPLETE.md                # Detailed guide
├── DATABRICKS_SETUP.md              # Databricks details
│
├── src/
│   ├── config.py                    # Configuration loading
│   ├── auth.py                      # Login system
│   ├── azure_client.py              # Azure OpenAI integration
│   ├── databricks_llm_client.py     # Databricks integration
│   ├── databricks_client.py         # CSV data loading
│   └── utils.py                     # Helper functions
│
└── data/
    ├── roles_sample.csv             # User accounts
    ├── job_openings_sample.csv      # Job listings
    └── mentors_sample.csv           # Mentor profiles
```

---

## 🎯 Success Criteria

You'll know everything is working when:

1. ✅ `python verify_setup.py` shows all ✅ marks
2. ✅ App starts with `streamlit run app.py`
3. ✅ Can login with jane@mentee.com / password
4. ✅ Can complete 5-step chatbot
5. ✅ Job recommendations show with % match
6. ✅ Mentor recommendations show
7. ✅ **Upskilling plan shows AI-generated text** ← This is the final step!

---

## 🔄 Workflow (After Setup)

```
START → Login → 5-Step Chatbot → Results Page
                                     ├─ Job Matches (instant)
                                     ├─ Mentor Matches (instant)
                                     └─ AI Upskilling (if LLM configured)
```

---

## 💡 Pro Tips

1. **Customize demo data:**
   - Edit `data/roles_sample.csv` to add users
   - Edit `data/job_openings_sample.csv` to add jobs
   - Edit `data/mentors_sample.csv` to add mentors

2. **Test without AI:**
   - App fully works for job/mentor matching
   - AI upskilling is optional enhancement

3. **Enable debug mode:**
   - If error occurs, click "Debug Info" section
   - Shows exact error message and config values

4. **Switch LLM services:**
   - Just update `.env` and restart app
   - App automatically tries Databricks first, then Azure

---

## 📞 Need Help?

1. **Run diagnostic:** `python verify_setup.py`
2. **Test LLM:** `python test_llm_services.py`
3. **Check debug info:** Click "Debug Info" in app error
4. **Read guides:** SETUP_COMPLETE.md or QUICK_SETUP.md
5. **Verify credentials:** 
   - Databricks token format: `dapi...`
   - Databricks endpoint: Contains `/serving-endpoints/`
   - Azure endpoint: Ends with `/`

---

## 🎉 Ready?

1. Open terminal in project folder
2. Run: `python verify_setup.py`
3. Follow the output's recommendations
4. Run: `streamlit run app.py`
5. Login and test!

**Total time: 5-15 minutes**

Good luck! 🚀
