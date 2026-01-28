#!/usr/bin/env python
"""Test USE CATALOG to switch to a working catalog."""
import sys
sys.path.append(r'c:\workspace\ai_coach_app')
from src.databricks_sql import DatabricksSQLClient

try:
    c = DatabricksSQLClient()
    
    with c._connect() as conn:
        with conn.cursor() as cursor:
            # First, list available catalogs
            print("Listing available catalogs...")
            try:
                cursor.execute("SHOW CATALOGS")
                catalogs = cursor.fetchall()
                print(f"Available catalogs: {[row[0] for row in catalogs]}")
            except Exception as e:
                print(f"Could not list catalogs: {e}")
            
            # Try switching to 'main' catalog which typically exists
            print("\nAttempting USE CATALOG main...")
            try:
                cursor.execute("USE CATALOG main")
                print("✓ Switched to catalog 'main'")
            except Exception as e:
                print(f"✗ Could not switch to main: {e}")
            
            # Check current catalog after switch
            cursor.execute("SELECT current_catalog(), current_schema()")
            row = cursor.fetchone()
            print(f"After switch: catalog={row[0]}, schema={row[1]}")
            
            # Try table creation in main.default
            create_sql = """
CREATE TABLE IF NOT EXISTS upskilling_plans (
  id STRING,
  email STRING,
  created_at TIMESTAMP,
  plan STRING,
  progress INT,
  notes STRING,
  last_updated TIMESTAMP
)
USING DELTA
"""
            print("\nAttempting CREATE TABLE in main.default...")
            try:
                cursor.execute(create_sql)
                print("✓ Table creation succeeded!")
                
                # Try an insert
                print("\nAttempting insert...")
                cursor.execute(
                    "INSERT INTO upskilling_plans (id, email, created_at, plan, progress, notes, last_updated) "
                    "VALUES ('test-id', 'test@example.com', current_timestamp(), 'test plan', 0, 'notes', current_timestamp())"
                )
                print("✓ Insert succeeded!")
                
                # Try a select
                print("\nAttempting select...")
                cursor.execute("SELECT * FROM upskilling_plans WHERE email = 'test@example.com'")
                rows = cursor.fetchall()
                print(f"✓ Select returned {len(rows)} rows")
                
            except Exception as e:
                print(f"✗ Error: {e}")
                import traceback
                traceback.print_exc()
                
except Exception as e:
    import traceback
    print(f"Error: {e}")
    traceback.print_exc()
