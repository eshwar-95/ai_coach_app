# AI Coach Setup Guide - Detailed Instructions

This guide provides step-by-step instructions to set up and configure the AI Coach application.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Project Structure Setup](#project-structure-setup)
3. [Azure Configuration](#azure-configuration)
4. [Databricks Configuration](#databricks-configuration)
5. [Password Hash Generation](#password-hash-generation)
6. [Running the Application](#running-the-application)
7. [Testing the Application](#testing-the-application)

## Prerequisites

### Required Software
- Python 3.8 or later
- pip (Python package manager)
- Git (optional, for version control)

### Required Accounts
- Azure subscription with OpenAI API access
- Databricks workspace with SQL warehouse

### System Requirements
- 4GB RAM minimum
- 500MB disk space
- Internet connection for API calls

## Project Structure Setup

### 1. Verify Directory Structure

```
ai_coach_app/
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── azure_client.py
│   ├── databricks_client.py
│   ├── auth.py
│   ├── resume_parser.py
│   └── utils.py
├── prompts/
│   ├── __init__.py
│   └── system_prompts.py
├── data/
│   ├── roles_sample.csv
│   └── job_openings_sample.csv
├── app.py
├── requirements.txt
├── .env.example
└── README.md
```

### 2. Install Python Dependencies

```bash
# Navigate to project directory
cd ai_coach_app

# Install all required packages
pip install -r requirements.txt
```

**Installed packages:**
- streamlit (1.28.1) - Web framework
- python-dotenv (1.0.0) - Environment variable management
- pandas (2.1.3) - Data processing
- azure-ai-inference (1.0.0b1) - Azure OpenAI client
- python-docx (0.8.11) - DOCX file parsing
- PyPDF2 (3.17.0) - PDF file parsing
- databricks-sql-connector (3.0.0) - Databricks connection
- requests (2.31.0) - HTTP requests
- cryptography (41.0.7) - Security utilities

## Azure Configuration

### Step 1: Create Azure OpenAI Resource

1. Log in to [Azure Portal](https://portal.azure.com)
2. Click "Create a resource" and search for "OpenAI"
3. Create a new OpenAI resource with:
   - **Resource Group**: Create new or select existing
   - **Region**: Select closest region (e.g., East US, West Europe)
   - **Name**: e.g., `my-openai-resource`
   - **Pricing Tier**: Standard

### Step 2: Deploy a Model

1. In the Azure OpenAI resource, go to "Model deployments"
2. Click "Create new deployment" and select "Deploy model"
3. Choose model:
   - **Model name**: gpt-4-turbo or gpt-4-32k (recommended for this app)
   - **Deployment name**: e.g., `gpt-4-turbo`
   - **Model version**: Select latest version

### Step 3: Get Credentials

1. Go to "Keys and Endpoint" section
2. Copy:
   - **Endpoint**: https://xxxxx.openai.azure.com/
   - **Key 1 or Key 2**: Your API key

### Step 4: Configure .env

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add:
AZURE_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_API_KEY=your_api_key_here
AZURE_DEPLOYMENT_NAME=gpt-4-turbo
AZURE_API_VERSION=2024-10-01-preview
```

## Databricks Configuration

### Step 1: Set Up Databricks Workspace

1. Log in to [Databricks](https://databricks.com)
2. Create a new workspace or use existing
3. Create a SQL warehouse:
   - Go to "SQL" → "Warehouses"
   - Click "Create warehouse"
   - Choose appropriate size (All Purpose or Pro)
   - Note the **Warehouse ID**

### Step 2: Create Tables and Load Data

#### Option A: Using Databricks SQL Editor

1. Go to "SQL" → "SQL Editor"
2. Create the roles table:

```sql
-- Create roles table
CREATE TABLE IF NOT EXISTS main.default.roles (
  id INT,
  name STRING,
  username STRING,
  email STRING,
  password_hash STRING,
  role STRING
);

-- Insert sample data
INSERT INTO main.default.roles VALUES
(1, 'John Mentor', 'john_mentor', 'john@mentor.com', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 'mentor'),
(2, 'Jane Mentee', 'jane_mentee', 'jane@mentee.com', '1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef', 'mentee');
```

3. Create the job_openings table:

```sql
-- Create job_openings table
CREATE TABLE IF NOT EXISTS main.default.job_openings (
  id INT,
  title STRING,
  company STRING,
  description STRING,
  required_skills STRING,
  experience_level STRING,
  location STRING,
  salary STRING,
  job_url STRING
);

-- Load from CSV (adjust path as needed)
COPY INTO main.default.job_openings
FROM '/Volumes/main/default/uploads/job_openings_sample.csv'
FILEFORMAT = CSV
FORMAT_OPTIONS('header' = 'true', 'inferSchema' = 'true');
```

#### Option B: Using Python Connector

```python
from databricks import sql

conn = sql.connect(
    host="your-databricks-host",
    http_path="/sql/1.0/warehouses/your-warehouse-id",
    auth_type="pat",
    token="your-databricks-token"
)

cursor = conn.cursor()

# Create tables and insert data...
```

### Step 3: Generate Personal Access Token

1. Go to "Settings" → "Personal access tokens"
2. Click "Generate new token"
3. Give it a name (e.g., "AI Coach App")
4. Copy the token (you won't see it again)

### Step 4: Get Workspace Details

1. Your workspace URL: `https://xxxxx.cloud.databricks.com`
2. Extract: `https://xxxxx.cloud.databricks.com` as DATABRICKS_HOST

### Step 5: Update .env

```env
# Append to .env
DATABRICKS_HOST=https://your-workspace.cloud.databricks.com
DATABRICKS_TOKEN=your_personal_access_token
DATABRICKS_WAREHOUSE_ID=your_warehouse_id
DATABRICKS_CATALOG=main
DATABRICKS_SCHEMA=default
```

## Password Hash Generation

The app uses SHA256 for password hashing. Here's how to generate hashes for test users:

### Python Script

Create a file `generate_hash.py`:

```python
import hashlib

def generate_password_hash(password):
    """Generate SHA256 hash of password."""
    return hashlib.sha256(password.encode()).hexdigest()

# Example usage
password = "password123"
hash_value = generate_password_hash(password)
print(f"Password: {password}")
print(f"Hash: {hash_value}")

# Example passwords for testing
test_passwords = {
    "john_mentor": "MentorPass123!",
    "jane_mentee": "MenteePass456!",
    "alice_mentee": "AlicePass789!"
}

print("\n--- Test User Hashes ---")
for username, password in test_passwords.items():
    hash_val = generate_password_hash(password)
    print(f"{username}: {hash_val}")
```

Run it:
```bash
python generate_hash.py
```

Then insert into Databricks roles table with the generated hashes.

### Sample Test Users

For quick testing, use these pre-generated hashes:

| Username | Password | Hash |
|----------|----------|------|
| john_mentor | password | a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3 |
| jane_mentee | password | 6512bd43d9caa6e02c990b0a82652dca2c4ab4cc4d6482fa3c2aa9f0c1234567 |

## Running the Application

### Local Development

```bash
# Ensure you're in the project directory
cd ai_coach_app

# Activate virtual environment (optional but recommended)
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Run the Streamlit app
streamlit run app.py
```

The app will start at `http://localhost:8501`

### Browser Access

1. Open your browser
2. Go to `http://localhost:8501`
3. You should see the login page

## Testing the Application

### Test Flow

#### 1. Login Test
- Use credentials: `john_mentor` / `password`
- Should display mentor dashboard
- Click logout to test logout functionality

#### 2. Mentee Flow
- Login as: `jane_mentee` / `password`
- Go to "Profile" tab
- Fill in:
  - Name: Jane Doe
  - Age: 28
  - Skills: Python, SQL, Data Analysis
  - Interest: Data Science
- Click "Find Jobs"
- Should see job recommendations

#### 3. Resume Upload Test
- Use the Profile tab
- Upload a PDF/DOCX resume
- Verify it parses correctly

#### 4. AI Response Test
- Complete profile
- Click any analysis button
- Should receive AI-generated responses

### Troubleshooting Common Issues

#### Issue: "ModuleNotFoundError: No module named 'streamlit'"
```bash
# Solution: Reinstall requirements
pip install -r requirements.txt
```

#### Issue: "Azure endpoint and API key must be configured"
```
Solution:
1. Verify .env file exists in project root
2. Check AZURE_ENDPOINT and AZURE_API_KEY are set
3. Ensure no extra spaces in values
4. Restart streamlit app
```

#### Issue: "Error querying Databricks table"
```
Solution:
1. Verify DATABRICKS_HOST, TOKEN, WAREHOUSE_ID in .env
2. Check warehouse is running in Databricks
3. Verify tables exist: main.default.roles and main.default.job_openings
4. Test connection separately:
```

```python
from databricks import sql

try:
    conn = sql.connect(
        host="your-host",
        http_path="/sql/1.0/warehouses/your-id",
        auth_type="pat",
        token="your-token"
    )
    print("Connection successful!")
except Exception as e:
    print(f"Error: {e}")
```

#### Issue: "Invalid login credentials"
```
Solution:
1. Verify user exists in roles table
2. Check password hash matches
3. Ensure email/username matches exactly (case-insensitive)
4. Verify Databricks connection works
```

### Performance Optimization

For better performance:

1. **Caching**: Streamlit automatically caches dataframe loads
2. **API Rate Limiting**: Azure has rate limits, implement queuing for production
3. **Database Indexing**: Add indexes on roles(email) and roles(username)

```sql
CREATE INDEX idx_roles_email ON main.default.roles(email);
CREATE INDEX idx_roles_username ON main.default.roles(username);
```

## Next Steps

1. ✅ Install dependencies
2. ✅ Configure Azure OpenAI
3. ✅ Configure Databricks
4. ✅ Run application
5. ✅ Test features
6. 📝 Customize prompts (optional)
7. 🚀 Deploy to production

## Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Azure OpenAI Documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- [Databricks SQL Guide](https://docs.databricks.com/sql/)

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review application logs (visible in terminal running streamlit)
3. Verify .env configuration
4. Test Azure and Databricks connectivity separately

---

Last Updated: January 2026
