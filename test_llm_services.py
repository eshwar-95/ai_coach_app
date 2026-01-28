"""
Test script to verify LLM client configuration and connectivity.
Run this after configuring .env to test before running the full app.
"""

import os
import sys
from dotenv import load_dotenv

def test_databricks_llm():
    """Test Databricks LLM configuration and connectivity"""
    print("\n🧪 Testing Databricks LLM...")
    print("-" * 40)
    
    from src.databricks_llm_client import DatabricksLLMClient
    
    token = os.getenv('DATABRICKS_TOKEN', '').strip()
    endpoint = os.getenv('DATABRICKS_LLM_ENDPOINT', '').strip()
    
    if not token:
        print("❌ DATABRICKS_TOKEN not configured in .env")
        return False
    
    if not endpoint:
        print("❌ DATABRICKS_LLM_ENDPOINT not configured in .env")
        return False
    
    print(f"✅ Token configured: {token[:15]}...")
    print(f"✅ Endpoint configured: {endpoint[:60]}...")
    
    try:
        print("\n🔗 Initializing client...")
        client = DatabricksLLMClient()
        print("✅ Client initialized successfully")
        
        print("\n📝 Sending test request...")
        response = client.get_response(
            system_prompt="You are a helpful assistant.",
            user_message="Say 'Hello from Databricks!' in exactly 5 words."
        )
        
        if response:
            print(f"✅ Response received: {response}")
            return True
        else:
            print("❌ No response from LLM")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_azure_openai():
    """Test Azure OpenAI configuration and connectivity"""
    print("\n🧪 Testing Azure OpenAI...")
    print("-" * 40)
    
    from src.azure_client import AzureOpenAIClient
    
    endpoint = os.getenv('AZURE_ENDPOINT', '').strip()
    key = os.getenv('AZURE_API_KEY', '').strip()
    
    if not endpoint:
        print("❌ AZURE_ENDPOINT not configured in .env")
        return False
    
    if not key:
        print("❌ AZURE_API_KEY not configured in .env")
        return False
    
    print(f"✅ Endpoint configured: {endpoint[:60]}...")
    print(f"✅ API Key configured: {key[:15]}...")
    
    try:
        print("\n🔗 Initializing client...")
        client = AzureOpenAIClient()
        print("✅ Client initialized successfully")
        
        print("\n📝 Sending test request...")
        response = client.get_response(
            system_prompt="You are a helpful assistant.",
            user_message="Say 'Hello from Azure!' in exactly 5 words."
        )
        
        if response:
            print(f"✅ Response received: {response}")
            return True
        else:
            print("❌ No response from LLM")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🔬 AI Coach LLM Service Test")
    print("=" * 40)
    
    # Load environment
    load_dotenv()
    
    # Check which services are configured
    databricks_configured = bool(
        os.getenv('DATABRICKS_TOKEN', '').strip() and 
        os.getenv('DATABRICKS_LLM_ENDPOINT', '').strip()
    )
    azure_configured = bool(
        os.getenv('AZURE_ENDPOINT', '').strip() and 
        os.getenv('AZURE_API_KEY', '').strip()
    )
    
    if not databricks_configured and not azure_configured:
        print("\n❌ No LLM service configured!")
        print("\nPlease configure either:")
        print("1. Databricks: DATABRICKS_TOKEN + DATABRICKS_LLM_ENDPOINT")
        print("2. Azure OpenAI: AZURE_ENDPOINT + AZURE_API_KEY")
        return 1
    
    results = []
    
    # Test Databricks if configured
    if databricks_configured:
        results.append(("Databricks LLM", test_databricks_llm()))
    else:
        print("\n⏭️  Databricks not configured (skipping)")
    
    # Test Azure if configured
    if azure_configured:
        results.append(("Azure OpenAI", test_azure_openai()))
    else:
        print("\n⏭️  Azure OpenAI not configured (skipping)")
    
    # Summary
    print("\n" + "=" * 40)
    print("📊 Summary:")
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {name}")
    
    all_pass = all(success for _, success in results)
    if all_pass:
        print("\n✅ All configured services working!")
        print("Ready to run: streamlit run app.py")
    else:
        print("\n⚠️  Some services failed. Check config above.")
    
    return 0 if all_pass else 1

if __name__ == "__main__":
    sys.exit(main())
