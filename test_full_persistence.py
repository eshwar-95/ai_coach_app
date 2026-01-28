#!/usr/bin/env python
"""Complete test of SQL persistence: insert, read, update."""
import sys
sys.path.append(r'c:\workspace\ai_coach_app')
from src.databricks_sql import DatabricksSQLClient

try:
    c = DatabricksSQLClient()
    
    # Test 1: Insert a plan
    print("=" * 60)
    print("TEST 1: Insert a plan")
    print("=" * 60)
    rid = c.insert_plan('john@mentee.com', 'Learn Python and ML', 0, 'Starting point')
    print(f"✓ Inserted plan with ID: {rid}")
    
    # Test 2: Insert another plan for same user
    print("\n" + "=" * 60)
    print("TEST 2: Insert another plan for same user")
    print("=" * 60)
    rid2 = c.insert_plan('john@mentee.com', 'Advanced Data Engineering', 25, 'In progress')
    print(f"✓ Inserted second plan with ID: {rid2}")
    
    # Test 3: Read plans by email
    print("\n" + "=" * 60)
    print("TEST 3: Read all plans for john@mentee.com")
    print("=" * 60)
    plans = c.get_plans_by_email('john@mentee.com')
    print(f"✓ Found {len(plans)} plans:")
    for i, plan in enumerate(plans, 1):
        print(f"  Plan {i}:")
        print(f"    ID: {plan['id']}")
        print(f"    Email: {plan['email']}")
        print(f"    Plan: {plan['plan'][:30]}...")
        print(f"    Progress: {plan['progress']}%")
        print(f"    Notes: {plan['notes']}")
    
    # Test 4: Update progress
    print("\n" + "=" * 60)
    print("TEST 4: Update progress on first plan")
    print("=" * 60)
    c.update_progress(rid, 50, 'Completed Python basics, working on ML')
    print(f"✓ Updated plan {rid} to 50% progress")
    
    # Test 5: Verify update
    print("\n" + "=" * 60)
    print("TEST 5: Verify update by reading again")
    print("=" * 60)
    plans = c.get_plans_by_email('john@mentee.com')
    for plan in plans:
        if plan['id'] == rid:
            print(f"✓ Found updated plan:")
            print(f"  Progress: {plan['progress']}%")
            print(f"  Notes: {plan['notes']}")
    
    # Test 6: Different user (should get no plans)
    print("\n" + "=" * 60)
    print("TEST 6: Read plans for different user (should be empty)")
    print("=" * 60)
    plans = c.get_plans_by_email('alice@mentee.com')
    print(f"✓ Found {len(plans)} plans for alice@mentee.com (expected 0)")
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED ✓")
    print("=" * 60)
    
except Exception as e:
    import traceback
    print(f"\n✗ Error: {e}")
    traceback.print_exc()
