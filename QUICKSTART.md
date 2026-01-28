# Quick Start Guide - AI Coach

Get AI Coach running in just 3 steps!

## Step 1: Install Dependencies (1 minute)

```bash
# Option A: With virtual environment (recommended)
python -m venv venv
venv\Scripts\activate  # Windows: Use this
# Or on macOS/Linux: source venv/bin/activate

# Option B: Without virtual environment (just run this)
pip install -r requirements.txt
```

## Step 2: Configure Azure (1 minute)

1. Create `.env` file by copying the template:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your Azure OpenAI credentials:
   ```
   AZURE_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_API_KEY=your_api_key_here
   AZURE_DEPLOYMENT_NAME=gpt-4-turbo
   USE_LOCAL_CSV=True
   ```

3. **How to get Azure credentials:**
   - Go to https://portal.azure.com
   - Find your Azure OpenAI resource
   - Click "Keys and Endpoint"
   - Copy the endpoint and API key

## Step 3: Run the App (1 minute)

```bash
streamlit run app.py
```

The app opens automatically at `http://localhost:8501`

---

## Login & Test

Use these demo credentials:
- **Username:** `jane_mentee` or `john_mentor`
- **Password:** `password`

Or view `data/roles_sample.csv` to see all users.

---

## What Happens Next

1. **Mentee Flow:**
   - Answer 5 simple questions (name, age, skills, interests)
   - Get job recommendations matching your skills
   - Receive personalized upskilling plan from AI Coach
   - See mentor recommendations

2. **Mentor Flow:**
   - View dashboard (features coming soon)

---

## Common Issues

**"streamlit: command not found"**
```bash
pip install streamlit
```

**"No module named 'azure'"**
```bash
pip install -r requirements.txt
```

**"CSV file not found"**
Make sure you're running from the project root:
```bash
cd ai_coach_app
streamlit run app.py
```

**"Azure API Error"**
- Double-check your `.env` file has correct credentials
- Make sure `AZURE_ENDPOINT` ends with `/` : `https://...openai.azure.com/`

---

## That's It! 🎉

Your AI Coach app is now running locally with:
- ✅ Login system (roles_sample.csv)
- ✅ Job recommendations (job_openings_sample.csv)
- ✅ Mentor matching (mentors_sample.csv)
- ✅ AI upskilling plans (Azure OpenAI)

No Databricks account needed. Pure local setup!

---

## Next Steps

- **Add more users:** Edit `data/roles_sample.csv`
- **Add more jobs:** Edit `data/job_openings_sample.csv`
- **Add more mentors:** Edit `data/mentors_sample.csv`
- **Customize prompts:** Edit `prompts/system_prompts.py`

See `README.md` for full documentation.
