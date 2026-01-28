#!/usr/bin/env python3
"""
Quick start script for AI Coach application setup and testing.
Helps verify all configurations are correct before running the app.
"""

import os
import sys
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible."""
    print("📋 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor} (OK)")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} (Requires 3.8+)")
        return False


def check_dependencies():
    """Check if all required packages are installed."""
    print("\n📋 Checking dependencies...")
    required_packages = [
        "streamlit",
        "pandas",
        "python-dotenv",
        "azure",
        "docx",
        "PyPDF2",
        "databricks",
    ]

    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing.append(package)

    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("Install with: pip install -r requirements.txt")
        return False
    return True


def check_env_file():
    """Check if .env file exists and is configured."""
    print("\n📋 Checking .env configuration...")

    if not os.path.exists(".env"):
        print("❌ .env file not found")
        print("   Create it with: cp .env.example .env")
        return False

    print("✅ .env file found")

    # Check key variables
    required_vars = [
        ("AZURE_ENDPOINT", "Azure OpenAI endpoint"),
        ("AZURE_API_KEY", "Azure OpenAI API key"),
        ("AZURE_DEPLOYMENT_NAME", "Azure deployment name"),
        ("DATABRICKS_HOST", "Databricks workspace host"),
        ("DATABRICKS_TOKEN", "Databricks personal access token"),
        ("DATABRICKS_WAREHOUSE_ID", "Databricks warehouse ID"),
    ]

    from dotenv import load_dotenv

    load_dotenv()

    all_configured = True
    for var, description in required_vars:
        value = os.getenv(var)
        if value and value != f"your_{var.lower()}_here":
            print(f"✅ {var}")
        else:
            print(f"⚠️  {var} - {description}")
            all_configured = False

    return all_configured


def check_project_structure():
    """Check if all required files exist."""
    print("\n📋 Checking project structure...")

    required_files = [
        "app.py",
        "requirements.txt",
        "README.md",
        "SETUP_GUIDE.md",
        "src/__init__.py",
        "src/config.py",
        "src/auth.py",
        "src/azure_client.py",
        "src/databricks_client.py",
        "src/resume_parser.py",
        "src/utils.py",
        "prompts/__init__.py",
        "prompts/system_prompts.py",
        "data/roles_sample.csv",
        "data/job_openings_sample.csv",
    ]

    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
            all_exist = False

    return all_exist


def test_azure_connection():
    """Test Azure OpenAI connection."""
    print("\n📋 Testing Azure OpenAI connection...")

    try:
        from src.azure_client import AzureOpenAIClient

        client = AzureOpenAIClient()
        print("✅ Azure client initialized successfully")
        return True
    except ValueError as e:
        print(f"⚠️  Configuration needed: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_databricks_connection():
    """Test Databricks connection."""
    print("\n📋 Testing Databricks connection...")

    try:
        from src.databricks_client import DatabricksClient

        client = DatabricksClient()
        print("✅ Databricks client initialized")

        # Try to connect
        try:
            conn = client.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            conn.close()
            print("✅ Databricks connection successful")
            return True
        except Exception as e:
            print(f"⚠️  Connection failed: {str(e)}")
            print("   Ensure Databricks warehouse is running")
            return False

    except ValueError as e:
        print(f"⚠️  Configuration needed: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def check_authentication_setup():
    """Check if authentication is properly configured."""
    print("\n📋 Checking authentication setup...")

    try:
        from src.auth import AuthenticationManager

        print("✅ Authentication module loaded")

        # Try to get roles data (won't work without Databricks, but tests the code)
        try:
            roles_df = AuthenticationManager.get_roles_data()
            if not roles_df.empty:
                print(f"✅ Found {len(roles_df)} user(s) in roles table")
                return True
            else:
                print("⚠️  No users found in roles table")
                return False
        except Exception as e:
            print(f"⚠️  Could not fetch roles: {str(e)}")
            return False

    except Exception as e:
        print(f"❌ Error loading authentication: {str(e)}")
        return False


def main():
    """Run all checks."""
    print("🚀 AI Coach - Quick Start Verification\n")
    print("=" * 50)

    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Project Structure", check_project_structure),
        ("Environment Configuration", check_env_file),
        ("Azure Configuration", test_azure_connection),
        ("Databricks Configuration", test_databricks_connection),
        ("Authentication Setup", check_authentication_setup),
    ]

    results = {}
    for check_name, check_func in checks:
        try:
            results[check_name] = check_func()
        except Exception as e:
            print(f"❌ Unexpected error in {check_name}: {str(e)}")
            results[check_name] = False

    # Summary
    print("\n" + "=" * 50)
    print("📊 Summary")
    print("=" * 50)

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for check_name, passed_check in results.items():
        status = "✅" if passed_check else "⚠️ " if "Configuration" in check_name else "❌"
        print(f"{status} {check_name}")

    print(f"\nResult: {passed}/{total} checks passed")

    if passed == total:
        print("\n✅ All systems ready! Run: streamlit run app.py")
        return 0
    elif passed >= total - 2:
        print("\n⚠️  Most systems ready, but some configuration needed.")
        print("   See SETUP_GUIDE.md for detailed instructions.")
        return 0
    else:
        print("\n❌ Please fix configuration issues before running the app.")
        print("   See SETUP_GUIDE.md for detailed instructions.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
