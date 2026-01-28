#!/usr/bin/env python
"""Detailed test of DatabricksSQLClient with creation enabled."""
import sys
sys.path.append(r'c:\workspace\ai_coach_app')
from src.databricks_sql import DatabricksSQLClient
from src.config import DATABRICKS_ALLOW_SCHEMA_CREATE

print(f"DATABRICKS_ALLOW_SCHEMA_CREATE: {DATABRICKS_ALLOW_SCHEMA_CREATE}")

try:
    c = DatabricksSQLClient()
    print(f"✓ Client initialized")
    print(f"  server_hostname: {c.server_hostname}")
    print(f"  catalog: {c.catalog}")
    print(f"  schema: {c.schema}")
    
    c.ensure_table_exists()
    print(f"✓ ensure_table_exists() completed")
    print(f"  _available: {c._available}")
    print(f"  _qualified_table: {getattr(c, '_qualified_table', 'NOT SET')}")
    
    if c._available:
        rid = c.insert_plan('test@example.com', 'Test plan', 0, 'Initial')
        print(f"✓ insert_plan() succeeded: {rid}")
        
        plans = c.get_plans_by_email('test@example.com')
        print(f"✓ get_plans_by_email() returned {len(plans)} records")
    else:
        print("✗ SQL not available, would use CSV fallback")
        
except Exception as e:
    print(f"✗ Error: {type(e).__name__}: {str(e)[:200]}")
    import traceback
    traceback.print_exc()
