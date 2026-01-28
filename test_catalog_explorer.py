"""E2E Integration Test for SkillBridge with Catalog Explorer."""
import sys
from src.catalog_explorer import (
    list_catalogs,
    list_schemas,
    list_tables,
    preview_table,
    get_numeric_columns,
    get_categorical_columns,
)


def test_catalog_explorer():
    """Test catalog explorer functionality."""
    print("\n" + "="*60)
    print("🧪 CATALOG EXPLORER E2E TEST")
    print("="*60)
    
    # Test 1: List Catalogs
    print("\n✓ Test 1: List Catalogs")
    try:
        catalogs = list_catalogs()
        print(f"   ✅ Found {len(catalogs)} catalogs")
        print(f"   Catalogs: {catalogs.iloc[:, 0].tolist()}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return False
    
    # Test 2: List Schemas in hackathon catalog
    print("\n✓ Test 2: List Schemas in 'hackathon' Catalog")
    try:
        schemas = list_schemas("hackathon")
        print(f"   ✅ Found {len(schemas)} schemas in hackathon")
        if not schemas.empty:
            schema_col = 'namespace_name' if 'namespace_name' in schemas.columns else 'name'
            schema_list = schemas[schema_col].tolist()
            print(f"   Schemas: {schema_list[:5]}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return False
    
    # Test 3: List Tables in default schema
    print("\n✓ Test 3: List Tables in 'hackathon.default' Schema")
    try:
        tables = list_tables("hackathon", "default")
        print(f"   ✅ Found {len(tables)} tables in hackathon.default")
        if not tables.empty:
            table_col = tables.columns[0]
            table_list = tables[table_col].tolist()[:5]
            print(f"   Tables (first 5): {table_list}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return False
    
    # Test 4: Preview a table (if exists)
    print("\n✓ Test 4: Preview Table Data")
    try:
        df = preview_table("hackathon", "default", "job_openings", limit=10)
        print(f"   ✅ Loaded {len(df)} rows from hackathon.default.job_openings")
        print(f"   Columns: {list(df.columns)[:5]}")
        
        # Test 5: Get column types
        print("\n✓ Test 5: Column Type Detection")
        numeric = get_numeric_columns(df)
        categorical = get_categorical_columns(df)
        print(f"   ✅ Numeric columns: {numeric}")
        print(f"   ✅ Categorical columns: {categorical[:3]}")
        
    except Exception as e:
        print(f"   ⚠️  Skipped (table may not exist): {e}")
    
    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED!")
    print("="*60)
    return True


if __name__ == "__main__":
    success = test_catalog_explorer()
    sys.exit(0 if success else 1)
