"""
Verification script to check AI Coach configuration and dependencies.
Run this to diagnose setup issues before running the app.
"""

import os
import sys
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.10+"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python version too old: {version.major}.{version.minor} (need 3.10+)")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    required = [
        'streamlit',
        'pandas',
        'numpy',
        'azure',
        'openai',
        'requests',
        'dotenv',
        'cryptography'
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing.append(package)
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    return True

def check_data_files():
    """Check if required data files exist"""
    required_files = [
        'data/roles_sample.csv',
        'data/job_openings_sample.csv',
        'data/mentors_sample.csv'
    ]
    
    all_exist = True
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} (missing)")
            all_exist = False
    
    return all_exist

def check_env_configuration():
    """Check if .env file is configured"""
    from dotenv import load_dotenv
    
    # Load .env file
    load_dotenv()
    
    databricks_token = os.getenv('DATABRICKS_TOKEN', '').strip()
    databricks_endpoint = os.getenv('DATABRICKS_LLM_ENDPOINT', '').strip()
    azure_endpoint = os.getenv('AZURE_ENDPOINT', '').strip()
    azure_key = os.getenv('AZURE_API_KEY', '').strip()
    
    print("\n📋 Configuration Status:")
    print("-" * 40)
    
    # Check Databricks
    databricks_ready = databricks_token and databricks_endpoint
    if databricks_ready:
        print(f"✅ Databricks: Configured")
        print(f"   - Token: {databricks_token[:10]}..." if len(databricks_token) > 10 else f"   - Token: {databricks_token}")
        print(f"   - Endpoint: {databricks_endpoint[:50]}...")
    else:
        print("❌ Databricks: Not configured")
        if not databricks_token:
            print("   - Missing DATABRICKS_TOKEN")
        if not databricks_endpoint:
            print("   - Missing DATABRICKS_LLM_ENDPOINT")
    
    # Check Azure
    azure_ready = azure_endpoint and azure_key
    if azure_ready:
        print(f"✅ Azure OpenAI: Configured")
        print(f"   - Endpoint: {azure_endpoint[:50]}...")
        print(f"   - Key: {azure_key[:10]}...")
    else:
        print("❌ Azure OpenAI: Not configured")
        if not azure_endpoint:
            print("   - Missing AZURE_ENDPOINT")
        if not azure_key:
            print("   - Missing AZURE_API_KEY")
    
    # Check at least one is configured
    if databricks_ready or azure_ready:
        print("\n✅ AI service configured (at least one)")
        return True
    else:
        print("\n❌ No AI service configured")
        print("\nTo enable AI recommendations, configure either:")
        print("1. Databricks (primary): Set DATABRICKS_TOKEN and DATABRICKS_LLM_ENDPOINT")
        print("2. Azure OpenAI (fallback): Set AZURE_ENDPOINT and AZURE_API_KEY")
        return False

def check_auth_data():
    """Check if auth CSV has valid credentials"""
    try:
        import pandas as pd
        df = pd.read_csv('data/roles_sample.csv')
        
        if 'email' in df.columns and 'password' in df.columns:
            print(f"\n✅ Auth CSV valid: {len(df)} users configured")
            print("   Demo credentials:")
            for idx, row in df.iterrows():
                print(f"   - {row['email']} / {row['password']}")
            return True
        else:
            print("❌ Auth CSV missing email/password columns")
            return False
    except Exception as e:
        print(f"❌ Error reading auth CSV: {e}")
        return False

def main():
    print("🔍 AI Coach Setup Verification")
    print("=" * 40)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Data Files", check_data_files),
        ("Auth Configuration", check_auth_data),
        ("LLM Configuration", check_env_configuration),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n📌 {name}:")
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Error: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 40)
    print("📊 Summary:")
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    all_pass = all(r for _, r in results)
    if all_pass:
        print("\n✅ All checks passed! Ready to run: streamlit run app.py")
    else:
        print("\n⚠️  Some checks failed. See above for details.")
    
    return 0 if all_pass else 1

if __name__ == "__main__":
    sys.exit(main())
