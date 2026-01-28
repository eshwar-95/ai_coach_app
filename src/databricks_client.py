"""Data loading module for local CSV files (local mode) or Databricks SQL (production)."""
from typing import List, Dict, Optional
import pandas as pd
import os
from src.config import (
    DATABRICKS_HOST,
    DATABRICKS_TOKEN,
    DATABRICKS_WAREHOUSE_ID,
    DATABRICKS_CATALOG,
    DATABRICKS_SCHEMA,
    USE_LOCAL_CSV,
)


class DatabricksClient:
    """Client for loading data from Databricks SQL or local CSV files."""

    def __init__(self):
        """Initialize Databricks client."""
        self.use_local = USE_LOCAL_CSV
        
        if not self.use_local:
            # Validate Databricks credentials
            if not DATABRICKS_HOST or not DATABRICKS_TOKEN or not DATABRICKS_WAREHOUSE_ID:
                raise ValueError(
                    "Databricks host, token, and warehouse ID must be configured in .env file"
                )
            self.host = DATABRICKS_HOST
            self.token = DATABRICKS_TOKEN
            self.warehouse_id = DATABRICKS_WAREHOUSE_ID
            self.catalog = DATABRICKS_CATALOG
            self.schema = DATABRICKS_SCHEMA

    def get_connection(self):
        """Create and return a Databricks SQL connection."""
        try:
            from databricks import sql
        except ImportError:
            raise RuntimeError("databricks-sql-connector is not installed. Install it with: pip install databricks-sql-connector")
        
        return sql.connect(
            host=self.host,
            http_path=f"/sql/1.0/warehouses/{self.warehouse_id}",
            auth_type="pat",
            token=self.token,
        )

    def _load_local_csv(self, filename: str) -> pd.DataFrame:
        """
        Load CSV from local data folder.
        
        Args:
            filename: Name of the CSV file (e.g., 'roles_sample.csv')
        
        Returns:
            DataFrame containing CSV data
        """
        csv_path = os.path.join(os.path.dirname(__file__), "..", "data", filename)
        
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found: {csv_path}")
        
        return pd.read_csv(csv_path)

    def query_csv_data(self, table_name: str) -> pd.DataFrame:
        """
        Query CSV data from local files or Databricks.

        Args:
            table_name: Name of the table to query (e.g., 'roles', 'job_openings')

        Returns:
            DataFrame containing query results
        """
        # Map table names to CSV files
        csv_mapping = {
            "roles": "roles_sample.csv",
            "job_openings": "job_openings_sample.csv",
            "mentors": "mentors_sample.csv",
        }
        
        if table_name not in csv_mapping:
            raise ValueError(f"Unknown table: {table_name}")
        
        csv_filename = csv_mapping[table_name]
        
        try:
            if self.use_local:
                return self._load_local_csv(csv_filename)
            else:
                # Use Databricks SQL
                conn = self.get_connection()
                cursor = conn.cursor()
                full_table_name = f"{self.catalog}.{self.schema}.{table_name}"
                cursor.execute(f"SELECT * FROM {full_table_name}")
                results = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                df = pd.DataFrame(results, columns=columns)
                cursor.close()
                conn.close()
                return df
        except Exception as e:
            raise RuntimeError(
                f"Error querying '{table_name}': {str(e)}"
            )

    def get_roles_data(self) -> pd.DataFrame:
        """Fetch roles data."""
        return self.query_csv_data("roles")

    def get_job_openings_data(self) -> pd.DataFrame:
        """Fetch job openings data."""
        return self.query_csv_data("job_openings")
    
    def get_mentors_data(self) -> pd.DataFrame:
        """Fetch mentors data."""
        try:
            return self.query_csv_data("mentors")
        except FileNotFoundError:
            # Return empty dataframe if mentors file doesn't exist
            return pd.DataFrame()

    def search_by_column(
        self, table_name: str, column: str, value: str
    ) -> pd.DataFrame:
        """
        Search for records in a table by column value.

        Args:
            table_name: Name of the table
            column: Column name to search in
            value: Value to search for

        Returns:
            Filtered DataFrame
        """
        df = self.query_csv_data(table_name)
        return df[df[column].str.lower() == str(value).lower()]
