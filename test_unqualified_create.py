#!/usr/bin/env python
"""Test unqualified table creation."""
import sys
sys.path.append(r'c:\workspace\ai_coach_app')
from src.databricks_sql import DatabricksSQLClient

try:
    c = DatabricksSQLClient()
    
    with c._connect() as conn:
        with conn.cursor() as cursor:
            # Try unqualified creation
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
            print("Attempting unqualified CREATE TABLE...")
            try:
                cursor.execute(create_sql)
                print("✓ Table creation succeeded (unqualified)")
            except Exception as e:
                print(f"✗ Table creation failed: {e}")
                
except Exception as e:
    import traceback
    print(f"Error: {e}")
    traceback.print_exc()
