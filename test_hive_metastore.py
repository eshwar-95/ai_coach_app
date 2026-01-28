#!/usr/bin/env python
"""Test creating table in hive_metastore."""
import sys
sys.path.append(r'c:\workspace\ai_coach_app')
from src.databricks_sql import DatabricksSQLClient

try:
    c = DatabricksSQLClient()
    
    with c._connect() as conn:
        with conn.cursor() as cursor:
            # Switch to hive_metastore
            print("Attempting USE CATALOG hive_metastore...")
            try:
                cursor.execute("USE CATALOG hive_metastore")
                print("✓ Switched to hive_metastore")
            except Exception as e:
                print(f"✗ Could not switch: {e}")
                raise
            
            # Check current location
            cursor.execute("SELECT current_catalog(), current_schema()")
            row = cursor.fetchone()
            print(f"Current: catalog={row[0]}, schema={row[1]}")
            
            # Try table creation
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
            print("\nAttempting CREATE TABLE...")
            try:
                cursor.execute(create_sql)
                print("✓ Table creation succeeded!")
                
                # Try an insert
                print("\nAttempting insert...")
                cursor.execute(
                    "INSERT INTO upskilling_plans (id, email, created_at, plan, progress, notes, last_updated) "
                    "VALUES ('test-id-1', 'test@example.com', current_timestamp(), 'test plan', 0, 'notes', current_timestamp())"
                )
                print("✓ Insert succeeded!")
                
                # Try a select
                print("\nAttempting select...")
                cursor.execute("SELECT id, email FROM upskilling_plans WHERE email = 'test@example.com'")
                rows = cursor.fetchall()
                print(f"✓ Select returned {len(rows)} rows")
                if rows:
                    print(f"  First row: {rows[0]}")
                
            except Exception as e:
                print(f"✗ Error: {e}")
                
except Exception as e:
    import traceback
    print(f"Error: {e}")
    traceback.print_exc()
