#!/usr/bin/env python3
"""Test mentor request functionality."""

import sys
sys.path.insert(0, "/workspace/ai_coach_app")

from src.databricks_sql import DatabricksSQLClient

def test_mentor_requests():
    """Test mentor request CRUD operations."""
    print("=" * 60)
    print("Testing Mentor Request Functionality")
    print("=" * 60)
    
    try:
        sql_client = DatabricksSQLClient()
        print("✅ DatabricksSQLClient initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize client: {e}")
        return False
    
    # Test 1: Create mentor request
    print("\n[Test 1] Creating mentor request...")
    try:
        request_id = sql_client.create_mentor_request(
            mentee_email="jane_mentee@example.com",
            mentee_name="Jane Doe",
            mentor_email="john_mentor@example.com",
            mentor_name="John Smith"
        )
        print(f"✅ Mentor request created with ID: {request_id}")
    except Exception as e:
        print(f"❌ Failed to create mentor request: {e}")
        return False
    
    # Test 2: Get mentor requests
    print("\n[Test 2] Getting mentor requests for john_mentor@example.com...")
    try:
        requests = sql_client.get_mentor_requests("john_mentor@example.com")
        print(f"✅ Retrieved {len(requests)} request(s)")
        for req in requests:
            print(f"   - ID: {req.get('id')}, Mentee: {req.get('mentee_name')}, Status: {req.get('status')}")
    except Exception as e:
        print(f"❌ Failed to get mentor requests: {e}")
        return False
    
    # Test 3: Get pending requests
    print("\n[Test 3] Getting pending requests for john_mentor@example.com...")
    try:
        pending = sql_client.get_mentor_requests("john_mentor@example.com", status="pending")
        print(f"✅ Retrieved {len(pending)} pending request(s)")
    except Exception as e:
        print(f"❌ Failed to get pending requests: {e}")
        return False
    
    # Test 4: Update request status
    print(f"\n[Test 4] Updating request {request_id} to 'accepted'...")
    try:
        sql_client.update_mentor_request(
            request_id,
            "accepted",
            "I'd be happy to mentor you!"
        )
        print(f"✅ Request updated to 'accepted'")
    except Exception as e:
        print(f"❌ Failed to update request: {e}")
        return False
    
    # Test 5: Verify status change
    print("\n[Test 5] Verifying status change...")
    try:
        accepted = sql_client.get_mentor_requests("john_mentor@example.com", status="accepted")
        print(f"✅ Retrieved {len(accepted)} accepted request(s)")
        for req in accepted:
            print(f"   - ID: {req.get('id')}, Mentee: {req.get('mentee_name')}, Status: {req.get('status')}, Responded: {req.get('responded_at')}")
    except Exception as e:
        print(f"❌ Failed to verify status change: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✅ All mentor request tests passed!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = test_mentor_requests()
    sys.exit(0 if success else 1)
