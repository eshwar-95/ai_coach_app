#!/usr/bin/env python
"""Debug table creation attempt."""
import sys
sys.path.append(r'c:\workspace\ai_coach_app')
from src.databricks_sql import DatabricksSQLClient

try:
    c = DatabricksSQLClient()
    print(f"Client config: catalog={c.catalog}, schema={c.schema}")
    
    # Try to get current catalog/schema manually
    with c._connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT current_catalog(), current_schema()")
            row = cursor.fetchone()
            if row:
                print(f"Session current_catalog(): {row[0]}")
                print(f"Session current_schema(): {row[1]}")
            else:
                print("Could not read current_catalog/current_schema")
    
    print("\nAttempting to create schema in current location...")
    with c._connect() as conn:
        with conn.cursor() as cursor:
            # Try creating in the actual current catalog/schema
            cursor.execute("SELECT current_catalog(), current_schema()")
            row = cursor.fetchone()
            if row:
                curr_cat = row[0]
                curr_sch = row[1]
                qualified_schema = f"`{curr_cat}`.`{curr_sch}`"
                print(f"Will try to create schema: {qualified_schema}")
                try:
                    cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {qualified_schema}")
                    print(f"✓ Schema creation succeeded")
                except Exception as e:
                    print(f"✗ Schema creation failed: {e}")
                
                # Now try table creation
                table_name = "upskilling_plans"
                qualified_table = f"{qualified_schema}.`{table_name}`"
                create_sql = f"""
CREATE TABLE IF NOT EXISTS {qualified_table} (
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
                print(f"Will try to create table: {qualified_table}")
                try:
                    cursor.execute(create_sql)
                    print(f"✓ Table creation succeeded")
                except Exception as e:
                    print(f"✗ Table creation failed: {e}")
                    
except Exception as e:
    import traceback
    print(f"Error: {e}")
    traceback.print_exc()
