"""Databricks Unity Catalog Explorer - Integrated with existing Databricks client."""
from databricks import sql
from src.config import (
    DATABRICKS_HOST,
    DATABRICKS_TOKEN,
    DATABRICKS_WAREHOUSE_ID,
    DATABRICKS_HTTP_PATH,
    DATABRICKS_CATALOG,
    DATABRICKS_SCHEMA,
    USE_LOCAL_CSV,
)
import pandas as pd
from decimal import Decimal
from typing import Optional
import streamlit as st


# Cache the connection to avoid OAuth issues with Streamlit reruns
@st.cache_resource
def get_catalog_connection():
    """Return a cached databricks.sql connection for catalog exploration.
    
    Uses environment variables from config.
    Connection is cached using @st.cache_resource to avoid multiple
    authentication attempts and OAuth state mismatches on Streamlit reruns.
    """
    # Allow catalog exploration even if USE_LOCAL_CSV is true
    # as long as we have explicit warehouse config
    if not (DATABRICKS_HOST and DATABRICKS_TOKEN):
        if not (DATABRICKS_HTTP_PATH and DATABRICKS_WAREHOUSE_ID):
            raise RuntimeError(
                "Databricks credentials not configured. Add DATABRICKS_HOST, DATABRICKS_TOKEN, "
                "and either DATABRICKS_WAREHOUSE_ID or DATABRICKS_HTTP_PATH to .env file."
            )
    
    # Build HTTP path from either DATABRICKS_HTTP_PATH or DATABRICKS_WAREHOUSE_ID
    if DATABRICKS_HTTP_PATH:
        http_path = DATABRICKS_HTTP_PATH
    elif DATABRICKS_WAREHOUSE_ID:
        http_path = f"/sql/1.0/warehouses/{DATABRICKS_WAREHOUSE_ID}"
    else:
        raise RuntimeError("Either DATABRICKS_HTTP_PATH or DATABRICKS_WAREHOUSE_ID must be configured.")
    
    conn = sql.connect(
        server_hostname=DATABRICKS_HOST,
        http_path=http_path,
        access_token=DATABRICKS_TOKEN,  # Use access_token instead of auth_type
    )
    return conn


@st.cache_data(ttl=300)  # Cache results for 5 minutes
def query_to_df(query: str, params: dict = None) -> pd.DataFrame:
    """Execute a query and return a pandas DataFrame.
    
    Handles Decimal type conversion from SQL NUMERIC/DECIMAL columns.
    """
    conn = get_catalog_connection()
    try:
        with conn.cursor() as cur:
            if params:
                cur.execute(query, params)
            else:
                cur.execute(query)
            cols = [c[0] for c in cur.description]
            rows = cur.fetchall()
        
        df = pd.DataFrame(rows, columns=cols)
        
        # Convert Decimal columns to numeric types
        for col in df.columns:
            sample = df[col].dropna().head(10)
            if not sample.empty and any(isinstance(x, Decimal) for x in sample):
                df[col] = df[col].apply(lambda x: float(x) if isinstance(x, Decimal) else x)
                df[col] = pd.to_numeric(df[col], errors='coerce')
            else:
                # Try to coerce numeric-like strings
                if df[col].dtype == object:
                    try:
                        coerced = pd.to_numeric(df[col])
                        df[col] = coerced
                    except (ValueError, TypeError):
                        pass  # Keep original type if coercion fails
        
        return df
    except Exception as e:
        raise RuntimeError(f"Query execution failed: {e}")
    # Don't close connection - it's cached with @st.cache_resource


def list_catalogs() -> pd.DataFrame:
    """List all catalogs in Unity Catalog."""
    return query_to_df("SHOW CATALOGS")


def list_schemas(catalog: str) -> pd.DataFrame:
    """List all schemas in a catalog."""
    return query_to_df(f"SHOW SCHEMAS IN {catalog}")


def list_tables(catalog: str, schema: str) -> pd.DataFrame:
    """List all tables in a schema."""
    return query_to_df(f"SHOW TABLES IN {catalog}.{schema}")


def preview_table(catalog: str, schema: str, table: str, limit: int = 100) -> pd.DataFrame:
    """Preview data from a table with row limit."""
    q = f"SELECT * FROM {catalog}.{schema}.{table} LIMIT {limit}"
    return query_to_df(q)


def get_numeric_columns(df: pd.DataFrame) -> list:
    """Return list of numeric column names."""
    return df.select_dtypes(include='number').columns.tolist()


def get_categorical_columns(df: pd.DataFrame) -> list:
    """Return list of categorical column names."""
    return df.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()


def get_datetime_columns(df: pd.DataFrame) -> list:
    """Return list of datetime column names."""
    return df.select_dtypes(include=['datetime', 'datetimetz']).columns.tolist()
