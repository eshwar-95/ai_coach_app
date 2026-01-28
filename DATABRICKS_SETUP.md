# Databricks LLM Integration Guide

Your AI Coach now supports **Databricks LLM serving endpoints** for generating upskilling plans and recommendations!

## 🚀 How to Set Up Databricks LLM

### Step 1: Get Your Databricks Token

1. Go to your Databricks workspace
2. Click your **profile icon** (top right)
3. Select **User Settings**
4. Go to **Access tokens**
5. Click **Generate new token**
6. Copy the token (starts with `dapi...`)

### Step 2: Find Your LLM Endpoint

1. In Databricks, go to **Serving endpoints**
2. Find an active LLM endpoint (e.g., `databricks-claude-sonnet-4-5`)
3. Copy the **serving endpoint URL**
   - Format: `https://your-workspace.azuredatabricks.net/serving-endpoints`
   - Or: `https://your-workspace.databricks.com/serving-endpoints`

### Step 3: Update Your `.env` File

Add these lines to `.env`:

```env
# Databricks LLM Configuration
DATABRICKS_TOKEN=dapi7b2e5fc97e1273fc9144af0da2da6017-2
DATABRICKS_LLM_ENDPOINT=https://adb-7405616962374519.19.azuredatabricks.net/serving-endpoints
DATABRICKS_MODEL=databricks-claude-sonnet-4-5
```

**Note:** Replace with your actual token, endpoint, and model name.

### Step 4: Restart the App

```powershell
# Ctrl+C to stop the current app
# Then restart:
. .\venv\Scripts\Activate.ps1
streamlit run app.py
```

## ✅ How It Works

When a mentee completes the 5-step profile:

1. **AI Coach** generates upskilling recommendations
2. **Priority order:**
   - **First:** Tries Databricks LLM (fast, available models)
   - **Fallback:** Uses Azure OpenAI if Databricks not configured
   - **Error handling:** Shows friendly message if neither is available

## 🎯 Available Databricks Models

Common models available through Databricks serving:
- `databricks-claude-sonnet-4-5` (Claude 3.5 Sonnet)
- `databricks-claude-opus-latest` (Claude 3 Opus)
- `databricks-meta-llama-3-405b-instruct` (Llama 3 405B)
- `databricks-mixtral-8x22b-instruct` (Mixtral)
- `databricks-llama-2-70b-chat` (Llama 2)

Check your Databricks workspace for available endpoints.

## 📝 Configuration Options

### Using Only Databricks (Remove Azure)
If you only want Databricks, you can leave Azure credentials empty:

```env
AZURE_ENDPOINT=
AZURE_API_KEY=

DATABRICKS_TOKEN=dapi...
DATABRICKS_LLM_ENDPOINT=https://...
DATABRICKS_MODEL=databricks-claude-sonnet-4-5
```

### Using Both (Recommended)
Keep both configured for automatic fallback:

```env
# Azure as fallback
AZURE_ENDPOINT=https://...
AZURE_API_KEY=...

# Databricks as primary
DATABRICKS_TOKEN=dapi...
DATABRICKS_LLM_ENDPOINT=https://...
DATABRICKS_MODEL=...
```

## 🔧 Troubleshooting

### "Error: Databricks token is not configured"
- Check `.env` file has `DATABRICKS_TOKEN`
- Make sure token is valid (starts with `dapi`)
- Token may have expired - regenerate in Databricks

### "Error: Invalid endpoint"
- Check endpoint format: `https://your-workspace.../serving-endpoints`
- Verify it's the serving endpoints URL, not SQL warehouse
- Remove trailing `/` if present

### "Model not found"
- Check `DATABRICKS_MODEL` matches available model in workspace
- List available models in Databricks UI
- Common typo: missing hyphens (e.g., `databricksclaude` vs `databricks-claude`)

### Response is slow
- Databricks LLM may be cold-starting
- First request is slower, subsequent requests are faster
- If very slow, check workspace is running
- Try Azure OpenAI as fallback

### Using Azure instead of Databricks
- Ensure Azure credentials are filled in
- Check if Databricks config is empty (app will use Azure automatically)
- Both work side-by-side

## 📊 Recommendation Flow

```
User completes 5-step profile
         ↓
Loads job openings from CSV
         ↓
Matches jobs to skills (local)
         ↓
Tries Databricks LLM for upskilling
    ├─ Success → Show AI recommendations
    └─ Fails → Try Azure OpenAI
         ↓
    ├─ Success → Show AI recommendations
    └─ Fails → Show friendly error message
         ↓
Loads mentor recommendations (local)
         ↓
Shows all results to user
```

## 🎓 Example Response

When configured properly, you'll see:

**Upskilling Recommendations**
> Based on your current skills (Python, SQL) and interests (Data Science), here's my recommendation...
> 
> **Top 3 Skills to Learn:**
> 1. Machine Learning (TensorFlow/PyTorch)
> 2. Advanced Statistics & Probability
> 3. Big Data Processing (Spark)
> 
> **Learning Path:**
> - **Short-term (1-3 months):** Online courses in ML fundamentals
> - **Medium-term (3-6 months):** Projects with real datasets
> - **Long-term (6+ months):** Kaggle competitions and advanced topics
> 
> **Estimated Time:** 20-30 hours per week

## 📞 Support

If Databricks LLM isn't working:
1. Verify token is valid and not expired
2. Check workspace is running
3. Confirm endpoint URL is correct
4. Try Azure OpenAI as fallback
5. Check app logs for specific error messages

The app is designed to work with either Databricks or Azure, so you have flexibility! 🚀
