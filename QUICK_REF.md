# 🎯 AI Coach - Quick Reference Card

## 🚀 START HERE (Copy & Paste)

```powershell
# Step 1: Verify setup
python verify_setup.py

# Step 2: Configure LLM (edit .env file - add EITHER option below)

# Option A: Databricks
DATABRICKS_TOKEN=dapi...
DATABRICKS_LLM_ENDPOINT=https://...

# Option B: Azure
AZURE_ENDPOINT=https://...
AZURE_API_KEY=...

# Step 3: Run app
. .\venv\Scripts\Activate.ps1
streamlit run app.py

# Step 4: Login
# Email: jane@mentee.com
# Password: password
```

---

## 📋 DEMO ACCOUNTS

| Email | Password | Role |
|-------|----------|------|
| jane@mentee.com | password | Mentee |
| john@mentor.com | password | Mentor |
| alice@company.com | password | Mentee |

---

## 🔧 DIAGNOSTIC COMMANDS

| Command | What It Does |
|---------|-----------|
| `python verify_setup.py` | Check configuration status |
| `python test_llm_services.py` | Test LLM connectivity |
| `streamlit run app.py` | Start the app |

---

## 📁 KEY FILES TO EDIT

| File | Purpose |
|------|---------|
| `.env` | Add LLM credentials HERE |
| `data/roles_sample.csv` | Add/edit user accounts |
| `data/job_openings_sample.csv` | Add/edit job listings |
| `data/mentors_sample.csv` | Add/edit mentors |

---

## 🆘 QUICK FIXES

| Problem | Solution |
|---------|----------|
| "Could not generate AI recommendations" | Run `python verify_setup.py` to check config |
| "Invalid credentials" at login | Use demo credentials above |
| "Module not found" | Run `pip install -r requirements.txt` |
| App won't start | Check venv is activated: `. .\venv\Scripts\Activate.ps1` |

---

## 📊 APP FLOW

```
Login (jane@mentee.com)
  ↓
Step 0: Enter Name
  ↓
Step 1: Enter Age
  ↓
Step 2: Select Skills (comma-separated)
  ↓
Step 3: Select Interests (comma-separated)
  ↓
Step 4: Review & Confirm
  ↓
Results Page:
  ├─ Job Recommendations (auto-calculated)
  ├─ Mentor Recommendations (auto-calculated)
  └─ Upskilling Plan (AI-generated, needs LLM config)
```

---

## 🔑 API CREDENTIAL FORMATS

**Databricks:**
```
Token format:     dapi1234567890abcdef...
Endpoint format:  https://workspace.cloud.databricks.com/serving-endpoints/model-name
```

**Azure:**
```
Endpoint format:  https://yourname.openai.azure.com/
API Key format:   32-character hex string (abc123def456...)
```

---

## ✅ SUCCESS CHECKLIST

- [ ] `python verify_setup.py` shows all ✅
- [ ] `.env` file has credentials (Databricks OR Azure)
- [ ] App starts: `streamlit run app.py`
- [ ] Can login with jane@mentee.com / password
- [ ] Can complete 5-step chatbot
- [ ] Job recommendations show (with % match)
- [ ] Mentor recommendations show
- [ ] Upskilling plan shows AI text ✨

---

## 📞 HELP RESOURCES

| Topic | Link |
|-------|------|
| Get Databricks Token | https://docs.databricks.com/dev-tools/auth |
| Get Azure Credentials | https://learn.microsoft.com/azure/ai-services/openai/reference |
| Streamlit Docs | https://docs.streamlit.io/ |

---

## ⏱️ TIME TO COMPLETION

- Setup verification: 1 min
- Get credentials: 3-5 min
- Configure .env: 1 min
- Restart app: 1 min
- **Total: 5-15 minutes**

---

## 🎉 YOU'RE 95% DONE!

Just need to add one credential to .env file and restart. That's it!

Questions? Run `python verify_setup.py` for diagnosis.
