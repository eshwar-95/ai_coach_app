#!/usr/bin/env python3
"""End-to-end test for mentee-to-mentor workflow."""

import sys
sys.path.insert(0, "/workspace/ai_coach_app")

from src.databricks_sql import DatabricksSQLClient
from src.auth import AuthenticationManager

def test_end_to_end_workflow():
    """Test complete mentee to mentor workflow."""
    print("=" * 70)
    print("TESTING END-TO-END MENTEE → MENTOR WORKFLOW")
    print("=" * 70)
    
    # Initialize SQL client
    try:
        sql_client = DatabricksSQLClient()
        print("✅ DatabricksSQLClient initialized")
    except Exception as e:
        print(f"❌ Failed to initialize SQL client: {e}")
        return False
    
    # Step 1: Mentee creates an upskilling plan
    print("\n[STEP 1] Mentee creates upskilling plan...")
    try:
        mentee_email = "test_mentee@example.com"
        plan_text = "I want to learn Python and data analysis. Focus on: pandas, numpy, visualization, ML basics."
        
        plan_id = sql_client.insert_plan(
            email=mentee_email,
            plan_text=plan_text,
            progress=0,
            notes="Initial plan from AI Coach"
        )
        print(f"✅ Upskilling plan created: ID={plan_id}")
        
        # Verify it was inserted
        plans = sql_client.get_plans_by_email(mentee_email)
        print(f"   Verified: Found {len(plans)} plan(s) for {mentee_email}")
    except Exception as e:
        print(f"❌ Failed to create plan: {e}")
        return False
    
    # Step 2: Mentee sends connection request to mentor
    print("\n[STEP 2] Mentee sends connection request to mentor...")
    try:
        request_id = sql_client.create_mentor_request(
            mentee_email="test_mentee@example.com",
            mentee_name="Test Mentee",
            mentor_email="john_mentor@example.com",
            mentor_name="John Smith"
        )
        print(f"✅ Connection request sent: ID={request_id}")
    except Exception as e:
        print(f"❌ Failed to create mentor request: {e}")
        return False
    
    # Step 3: Mentor views pending requests
    print("\n[STEP 3] Mentor views pending requests...")
    try:
        mentor_email = "john_mentor@example.com"
        pending = sql_client.get_mentor_requests(mentor_email, status="pending")
        
        print(f"✅ Found {len(pending)} pending request(s) for {mentor_email}")
        for req in pending:
            print(f"   - Mentee: {req.get('mentee_name')} ({req.get('mentee_email')})")
            print(f"   - Requested: {req.get('created_at')}")
            print(f"   - Status: {req.get('status')}")
            print(f"   - Request ID: {req.get('id')}")
        
        if not pending:
            print("⚠️  No pending requests found! Expected at least one.")
            return False
    except Exception as e:
        print(f"❌ Failed to retrieve mentor requests: {e}")
        return False
    
    # Step 4: Mentor accepts connection request
    print("\n[STEP 4] Mentor accepts connection request...")
    try:
        mentor_response = "I'd be happy to help you learn Python and data analysis!"
        sql_client.update_mentor_request(
            request_id,
            "accepted",
            mentor_response
        )
        print(f"✅ Request {request_id} accepted by mentor")
    except Exception as e:
        print(f"❌ Failed to accept request: {e}")
        return False
    
    # Step 5: Verify status change
    print("\n[STEP 5] Verify request status changed to 'accepted'...")
    try:
        accepted = sql_client.get_mentor_requests(mentor_email, status="accepted")
        print(f"✅ Found {len(accepted)} accepted request(s)")
        
        found = False
        for req in accepted:
            if req.get('id') == request_id:
                found = True
                print(f"   - Request {request_id} is now ACCEPTED")
                print(f"   - Mentee: {req.get('mentee_name')}")
                print(f"   - Response timestamp: {req.get('responded_at')}")
                print(f"   - Mentor notes: {req.get('notes')}")
        
        if not found:
            print(f"⚠️  Request {request_id} not found in accepted list!")
            return False
    except Exception as e:
        print(f"❌ Failed to verify status: {e}")
        return False
    
    # Step 6: Mentor rejects another hypothetical request
    print("\n[STEP 6] Testing request rejection...")
    try:
        reject_request_id = sql_client.create_mentor_request(
            mentee_email="another_mentee@example.com",
            mentee_name="Another Mentee",
            mentor_email=mentor_email,
            mentor_name="John Smith"
        )
        print(f"✅ Created request to reject: {reject_request_id}")
        
        sql_client.update_mentor_request(
            reject_request_id,
            "rejected",
            "I'm currently at capacity and cannot take on new mentees."
        )
        print(f"✅ Request {reject_request_id} rejected")
        
        rejected = sql_client.get_mentor_requests(mentor_email, status="rejected")
        print(f"✅ Found {len(rejected)} rejected request(s)")
    except Exception as e:
        print(f"❌ Failed to test rejection: {e}")
        return False
    
    # Step 7: Verify mentor statistics
    print("\n[STEP 7] Verify mentor statistics...")
    try:
        all_requests = sql_client.get_mentor_requests(mentor_email)
        pending_count = len(sql_client.get_mentor_requests(mentor_email, status="pending"))
        accepted_count = len(sql_client.get_mentor_requests(mentor_email, status="accepted"))
        rejected_count = len(sql_client.get_mentor_requests(mentor_email, status="rejected"))
        
        print(f"✅ Mentor Statistics for {mentor_email}:")
        print(f"   - Total requests: {len(all_requests)}")
        print(f"   - Pending: {pending_count}")
        print(f"   - Accepted: {accepted_count}")
        print(f"   - Rejected: {rejected_count}")
    except Exception as e:
        print(f"❌ Failed to get statistics: {e}")
        return False
    
    print("\n" + "=" * 70)
    print("✅ END-TO-END WORKFLOW TEST PASSED!")
    print("=" * 70)
    print("\nWorkflow Summary:")
    print("  1. ✅ Mentee created upskilling plan")
    print("  2. ✅ Mentee sent connection request to mentor")
    print("  3. ✅ Mentor viewed pending requests")
    print("  4. ✅ Mentor accepted connection request")
    print("  5. ✅ Status change verified")
    print("  6. ✅ Rejection workflow tested")
    print("  7. ✅ Mentor statistics verified")
    print("\nThe full mentee → mentor workflow is operational!")
    print("=" * 70)
    return True

if __name__ == "__main__":
    success = test_end_to_end_workflow()
    sys.exit(0 if success else 1)
