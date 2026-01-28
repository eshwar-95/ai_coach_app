# 🚀 Quick Setup Guide - AI Coach

## Current Status
✅ All dependencies installed and working  
✅ Demo authentication configured (ready to login)  
❌ **AI Services need configuration** (to get upskilling recommendations)

---

## Step 1: Run the Verification Script

First, verify your setup:

```powershell
python verify_setup.py
```

This will show you what's missing.

---

## Step 2: Configure AI Service (Choose ONE)

### Option A: Databricks LLM (Recommended - Faster)

1. **Get Databricks Token:**
   - Go to https://databricks.com/
   - Log into your workspace
   - Click your username → Account Settings
   - Click "Developer" → "Access Tokens"
   - Click "Generate new token"
   - Copy the token (starts with `dapi`)

2. **Get LLM Endpoint:**
   - In Databricks workspace, go to "Serving Endpoints"
   - Find or create an endpoint (e.g., `databricks-claude-sonnet-4-5`)
   - Click the endpoint name
   - Copy the "API URL" (format: `https://YOUR_WORKSPACE.cloud.databricks.com/serving-endpoints/...`)

3. **Update `.env` file:**
   ```env
   DATABRICKS_TOKEN=dapi1234567890abcdef...
   DATABRICKS_LLM_ENDPOINT=https://YOUR_WORKSPACE.cloud.databricks.com/serving-endpoints/databricks-claude-sonnet-4-5
   DATABRICKS_MODEL=databricks-claude-sonnet-4-5
   ```

### Option B: Azure OpenAI (Fallback)

1. **Get Azure Endpoint:**
   - Go to Azure Portal → OpenAI
   - Find your OpenAI resource
   - Click "Keys and Endpoints"
   - Copy the "Endpoint" (ends with `/`)

2. **Get Azure API Key:**
   - Same page, copy one of the keys

3. **Update `.env` file:**
   ```env
   AZURE_ENDPOINT=https://YOUR_RESOURCE.openai.azure.com/
   AZURE_API_KEY=abc123def456...
   AZURE_DEPLOYMENT_NAME=gpt-4-turbo
   ```

---

## Step 3: Run the App

```powershell
# Activate virtual environment
. .\venv\Scripts\Activate.ps1

# Run the app
streamlit run app.py
```

The app opens at `http://localhost:8501`

---

## Step 4: Test the App

1. **Login** with demo credentials:
   - Email: `jane@mentee.com`
   - Password: `password`

2. **Complete the 5-step chatbot:**
   - Step 0: Enter your name
   - Step 1: Enter your age
   - Step 2: Select skills (comma-separated)
   - Step 3: Select interests (comma-separated)
   - Step 4: Review & confirm

3. **View Results:**
   - **Job Recommendations**: Shows 3 best matching jobs with skill %, no AI needed
   - **Mentor Recommendations**: Shows 3 best matching mentors, no AI needed
   - **Upskilling Plan**: ⭐ Shows AI-generated upskilling plan (requires configured LLM)

---

## Troubleshooting

### "Could not generate AI recommendations" error
- Run `python verify_setup.py` to check configuration
- Make sure `.env` file is filled in with either Databricks OR Azure credentials
- Restart Streamlit: `Ctrl+C` then `streamlit run app.py`

### Can't find API keys?
- **Databricks**: https://docs.databricks.com/dev-tools/auth#generate-a-personal-access-token
- **Azure**: https://learn.microsoft.com/en-us/azure/ai-services/openai/reference

### Getting "Invalid credentials" error?
- Demo accounts work fine: `jane@mentee.com / password`
- If adding custom users, update `data/roles_sample.csv`

---

## Demo Credentials

| Email | Password | Role |
|-------|----------|------|
| jane@mentee.com | password | Mentee |
| john@mentor.com | password | Mentor |
| alice@company.com | password | Mentee |

---

## What Each AI Service Does

**Databricks LLM (Primary)**
- Generated upskilling recommendations
- Custom learning paths
- Faster, more private (runs in your Databricks workspace)
- **Recommended for production**

**Azure OpenAI (Fallback)**
- Same features as Databricks
- Uses GPT-4 Turbo
- Used only if Databricks is not configured
- Good backup option

---

## Next Steps

1. ✅ Verify setup: `python verify_setup.py`
2. ⬜ Configure LLM service (Databricks or Azure)
3. ⬜ Restart app: `streamlit run app.py`
4. ⬜ Test end-to-end flow

Questions? Check the debug info in the app (click "Debug Info" under error message).
