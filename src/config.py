import os
import hashlib
from dotenv import load_dotenv

load_dotenv()

# Mode Configuration
USE_LOCAL_CSV = os.getenv("USE_LOCAL_CSV", "True").lower() == "true"

# Azure Configuration
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
AZURE_API_KEY = os.getenv("AZURE_API_KEY")
AZURE_DEPLOYMENT_NAME = os.getenv("AZURE_DEPLOYMENT_NAME", "gpt-4-turbo")
AZURE_API_VERSION = "2024-10-01-preview"

# Databricks Configuration (only needed if USE_LOCAL_CSV=False)
DATABRICKS_HOST = os.getenv("DATABRICKS_HOST")
DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN")
DATABRICKS_WAREHOUSE_ID = os.getenv("DATABRICKS_WAREHOUSE_ID") or os.getenv("DATABRICKS_SQL_WAREHOUSE_ID")
DATABRICKS_CATALOG = os.getenv("DATABRICKS_CATALOG", "main")
DATABRICKS_SCHEMA = os.getenv("DATABRICKS_SCHEMA", "default")
DATABRICKS_HTTP_PATH = os.getenv("DATABRICKS_HTTP_PATH") or os.getenv("DATABRICKS_SQL_ENDPOINT")
# Whether the app is allowed to create catalogs/schemas/tables in Databricks.
# Default: False (safer). Set to "True" in `.env` to allow schema creation attempts.
DATABRICKS_ALLOW_SCHEMA_CREATE = os.getenv("DATABRICKS_ALLOW_SCHEMA_CREATE", "False").lower() == "true"

# Databricks LLM Configuration (for AI responses)
DATABRICKS_LLM_ENDPOINT = os.getenv("DATABRICKS_LLM_ENDPOINT")
DATABRICKS_MODEL = os.getenv("DATABRICKS_MODEL", "databricks-claude-sonnet-4-5")

# App Configuration
SECRET_KEY = os.getenv("APP_SECRET_KEY", "default_secret_key")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Supported file types
ALLOWED_RESUME_FORMATS = {"pdf", "doc", "docx", "txt"}
MAX_RESUME_SIZE = 10 * 1024 * 1024  # 10MB

# AI Model Parameters
TEMPERATURE = 0.7
MAX_TOKENS = 2000


def hash_password(password: str) -> str:
    """Hash password using SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    """Verify password against hash."""
    return hash_password(password) == password_hash
