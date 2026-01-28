#!/usr/bin/env python
"""Explore available schemas in hive_metastore."""
import sys
sys.path.append(r'c:\workspace\ai_coach_app')
from src.databricks_sql import DatabricksSQLClient

try:
    c = DatabricksSQLClient()
    
    with c._connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute("USE CATALOG hive_metastore")
            
            # List schemas
            print("Listing schemas in hive_metastore...")
            try:
                cursor.execute("SHOW SCHEMAS")
                schemas = cursor.fetchall()
                schema_list = [row[0] for row in schemas]
                print(f"Available schemas: {schema_list}")
            except Exception as e:
                print(f"Could not list schemas: {e}")
                
            # Try accessing hackathon catalog
            print("\nTrying hackathon catalog...")
            cursor.execute("USE CATALOG hackathon")
            cursor.execute("SHOW SCHEMAS")
            schemas = cursor.fetchall()
            schema_list = [row[0] for row in schemas]
            print(f"Schemas in hackathon: {schema_list}")
            
            # Try creating in hackathon catalog
            print("\nAttempting to create table in hackathon...")
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
            try:
                cursor.execute(create_sql)
                print("✓ Table creation in hackathon.default succeeded!")
                
                # Test insert
                cursor.execute(
                    "INSERT INTO upskilling_plans (id, email, created_at, plan, progress, notes, last_updated) "
                    "VALUES ('test-2', 'jane@mentee.com', current_timestamp(), 'upskilling plan', 50, 'ongoing', current_timestamp())"
                )
                print("✓ Insert succeeded!")
                
                # Test select
                cursor.execute("SELECT id, email, progress FROM upskilling_plans WHERE email='jane@mentee.com'")
                rows = cursor.fetchall()
                print(f"✓ Select returned {len(rows)} rows")
                if rows:
                    print(f"  Row: id={rows[0][0]}, email={rows[0][1]}, progress={rows[0][2]}")
                
            except Exception as e:
                print(f"✗ Error: {e}")
                
except Exception as e:
    import traceback
    print(f"Error: {e}")
    traceback.print_exc()
