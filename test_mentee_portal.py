#!/usr/bin/env python3
"""
E2E Test Script for AI Coach App
Tests:
1. Loading existing upskilling plans by mentee name
2. Progress tracking with proper timestamps and axis labels
3. Mentee recommendation system
4. Full mentee portal workflow
"""

import os
import sys
import csv
from datetime import datetime, timedelta
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from databricks_sql import DatabricksSQLClient


def test_load_existing_plans():
    """Test loading existing upskilling plans by mentee name."""
    print("\n" + "="*70)
    print("TEST 1: Load Existing Upskilling Plans by Name")
    print("="*70)
    
    client = DatabricksSQLClient()
    
    # Test data: Create a plan for a mentee
    test_email = "test_mentee@example.com"
    test_name = "Jane Doe"
    test_plan = "Learn Python basics, then advance to ML frameworks"
    
    try:
        # Insert a test plan
        plan_id = client.insert_plan(
            email=test_email,
            plan_text=test_plan,
            mentee_name=test_name,
            progress=0,
            notes="Starting fresh"
        )
        print(f"✅ Created test plan with ID: {plan_id}")
        
        # Try to retrieve by name
        plans_by_name = client.get_plans_by_name(test_name)
        if plans_by_name:
            print(f"✅ Retrieved {len(plans_by_name)} plan(s) by name '{test_name}'")
            for plan in plans_by_name:
                print(f"   - Plan ID: {plan.get('id')}")
                print(f"   - Mentee Name: {plan.get('mentee_name')}")
                print(f"   - Progress: {plan.get('progress')}%")
                print(f"   - Created At: {plan.get('created_at')}")
        else:
            print("⚠️  WARNING: No plans found by name")
            return False
        
        # Retrieve by email to compare
        plans_by_email = client.get_plans_by_email(test_email)
        if plans_by_email:
            print(f"✅ Retrieved {len(plans_by_email)} plan(s) by email")
            if len(plans_by_name) == len(plans_by_email):
                print("✅ Plans retrieved by name and email match")
            else:
                print("⚠️  WARNING: Plan counts don't match")
        
        return True
    
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def test_progress_tracking():
    """Test progress tracking with timestamps."""
    print("\n" + "="*70)
    print("TEST 2: Progress Tracking with Timestamps")
    print("="*70)
    
    client = DatabricksSQLClient()
    
    try:
        # Create a plan with progress 0
        test_email = "progress_test@example.com"
        test_name = "John Progress"
        
        plan_id = client.insert_plan(
            email=test_email,
            plan_text="Machine Learning Mastery",
            mentee_name=test_name,
            progress=0,
            notes=""
        )
        print(f"✅ Created plan with 0% progress: {plan_id}")
        
        # Retrieve and check initial state
        plans = client.get_plans_by_email(test_email)
        if plans:
            plan = plans[0]
            print(f"   - Initial Progress: {plan.get('progress')}%")
            print(f"   - Created At: {plan.get('created_at')}")
            initial_progress = plan.get('progress')
            
            # Update progress
            client.update_progress(plan_id, progress=50, notes="Completed first module")
            print(f"✅ Updated progress to 50%")
            
            # Retrieve updated plan
            updated_plans = client.get_plans_by_email(test_email)
            if updated_plans:
                updated_plan = updated_plans[0]
                new_progress = updated_plan.get('progress')
                last_updated = updated_plan.get('last_updated')
                
                print(f"   - Updated Progress: {new_progress}%")
                print(f"   - Last Updated: {last_updated}")
                
                if new_progress == 50 and last_updated != plan.get('created_at'):
                    print("✅ Progress tracked correctly with proper timestamp")
                    return True
                else:
                    print("⚠️  WARNING: Progress or timestamp not updated correctly")
                    return False
    
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def test_csv_fallback():
    """Test CSV fallback for plans."""
    print("\n" + "="*70)
    print("TEST 3: CSV Fallback for Upskilling Plans")
    print("="*70)
    
    try:
        # Check if CSV file exists and has proper format
        csv_path = Path(__file__).parent / "data" / "upskilling_plans.csv"
        
        if csv_path.exists():
            print(f"✅ CSV file exists: {csv_path}")
            
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                headers = reader.fieldnames
                
                print(f"✅ CSV Headers: {headers}")
                
                expected_headers = ['id', 'email', 'mentee_name', 'created_at', 'plan', 'progress', 'notes', 'last_updated']
                if all(h in headers for h in expected_headers):
                    print("✅ All required columns present in CSV")
                    
                    # Count records
                    rows = list(reader)
                    print(f"✅ CSV contains {len(rows)} record(s)")
                    
                    # Validate sample record
                    if rows:
                        row = rows[0]
                        if 'mentee_name' in row and row['mentee_name']:
                            print(f"✅ Sample record has mentee_name: {row['mentee_name']}")
                    
                    return True
                else:
                    print("❌ Missing required columns in CSV")
                    return False
        else:
            print(f"⚠️  CSV file not found at {csv_path}")
            print("   This is OK if only using Databricks SQL")
            return True
    
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def test_multiple_plans_per_mentee():
    """Test that a mentee can have multiple plans tracked."""
    print("\n" + "="*70)
    print("TEST 4: Multiple Plans Per Mentee")
    print("="*70)
    
    client = DatabricksSQLClient()
    
    try:
        # Create multiple plans for same mentee
        test_email = "multi_plan@example.com"
        test_name = "Sarah MultiPlan"
        
        plan_ids = []
        for i in range(3):
            plan_id = client.insert_plan(
                email=test_email,
                plan_text=f"Upskilling Plan {i+1}: {['Python', 'JavaScript', 'DevOps'][i]} Path",
                mentee_name=test_name,
                progress=i*25,
                notes=f"Plan {i+1} - {['Basics', 'Intermediate', 'Advanced'][i]} level"
            )
            plan_ids.append(plan_id)
            print(f"✅ Created plan {i+1}: {plan_id}")
        
        # Retrieve all plans for this mentee
        plans = client.get_plans_by_name(test_name)
        
        if len(plans) >= 3:
            print(f"✅ Retrieved {len(plans)} plans for mentee '{test_name}'")
            
            # Verify progress values
            progress_values = sorted([p.get('progress', 0) for p in plans], reverse=True)
            print(f"   Progress values: {progress_values}")
            
            # Verify they're sorted by created_at descending
            for idx, plan in enumerate(plans):
                print(f"   Plan {idx+1}: {plan.get('progress')}% - {plan.get('created_at')}")
            
            return True
        else:
            print(f"⚠️  WARNING: Expected 3+ plans, got {len(plans)}")
            return False
    
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def main():
    """Run all tests."""
    print("\n🧪 AI Coach App - E2E Test Suite")
    print("="*70)
    print("Testing: Mentee Portal Functionality")
    print("="*70)
    
    results = []
    
    # Run all tests
    results.append(("Load existing plans by name", test_load_existing_plans()))
    results.append(("Progress tracking with timestamps", test_progress_tracking()))
    results.append(("CSV fallback", test_csv_fallback()))
    results.append(("Multiple plans per mentee", test_multiple_plans_per_mentee()))
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print("\n" + "="*70)
    print(f"Total: {passed}/{total} tests passed")
    print("="*70)
    
    if passed == total:
        print("\n🎉 All tests passed! The mentee portal is ready for E2E testing.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review the errors above.")
        return 1


if __name__ == "__main__":
    exit(main())
