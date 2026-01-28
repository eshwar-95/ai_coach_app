"""Databricks SQL helper for storing and retrieving upskilling plans."""
from databricks import sql
from src.config import DATABRICKS_HOST, DATABRICKS_TOKEN, DATABRICKS_WAREHOUSE_ID, DATABRICKS_LLM_ENDPOINT, DATABRICKS_CATALOG, DATABRICKS_SCHEMA, DATABRICKS_ALLOW_SCHEMA_CREATE
from datetime import datetime
import uuid
import json
import os
import csv


class DatabricksSQLClient:
    """Simple Databricks SQL client using databricks-sql-connector."""

    def __init__(self, server_hostname: str = None, http_path: str = None, access_token: str = None):
        # prefer explicit params, fall back to env-configured values
        self.server_hostname = server_hostname or DATABRICKS_HOST
        # fall back to config value if not passed
        from src.config import DATABRICKS_HTTP_PATH
        self.http_path = http_path or DATABRICKS_HTTP_PATH
        # The user can pass DATABRICKS_SQL_WAREHOUSE_ID instead of http_path; keep http_path required for connector
        # access_token is required
        self.access_token = access_token or DATABRICKS_TOKEN

        # Preferred target catalog/schema for persistence. These may be overridden
        # at runtime by the server's current_catalog()/current_schema() values.
        self.catalog = DATABRICKS_CATALOG
        self.schema = DATABRICKS_SCHEMA
        # Whether SQL persistence is currently available. Set to False when
        # table/schema aren't usable and we should fallback to CSV storage.
        self._available = True
        if not self.server_hostname:
            raise ValueError("Databricks server hostname not configured")
        if not self.access_token:
            raise ValueError("Databricks access token not configured")

    def _connect(self):
        return sql.connect(
            server_hostname=self.server_hostname,
            http_path=self.http_path,
            access_token=self.access_token,
            timeout=30,
        )
    def ensure_table_exists(self, table_name: str = "upskilling_plans"):
        """Create the upskilling table if it does not exist."""
        if table_name == "mentor_requests":
            create_sql_unqualified = f"""
CREATE TABLE IF NOT EXISTS {table_name} (
  id STRING,
  mentee_email STRING,
  mentee_name STRING,
  mentor_email STRING,
  mentor_name STRING,
  status STRING,
  created_at TIMESTAMP,
  responded_at TIMESTAMP,
  notes STRING
)
USING DELTA
"""
        elif table_name == "notifications":
            create_sql_unqualified = f"""
CREATE TABLE IF NOT EXISTS {table_name} (
  id STRING,
  recipient_email STRING,
  recipient_name STRING,
  type STRING,
  title STRING,
  message STRING,
  related_id STRING,
  created_at TIMESTAMP,
  read_at TIMESTAMP,
  is_read BOOLEAN
)
USING DELTA
"""
        else:
            # upskilling_plans table
            create_sql_unqualified = f"""
CREATE TABLE IF NOT EXISTS {table_name} (
  id STRING,
  email STRING,
  mentee_name STRING,
  created_at TIMESTAMP,
  plan STRING,
  progress INT,
  notes STRING,
  last_updated TIMESTAMP
)
USING DELTA
"""

        create_sql_default = f"""
CREATE TABLE IF NOT EXISTS default.{table_name} (
  id STRING,
  email STRING,
  mentee_name STRING,
  created_at TIMESTAMP,
  plan STRING,
  progress INT,
  notes STRING,
  last_updated TIMESTAMP
)
USING DELTA
"""

        # We'll attempt to create a schema (if configured or inferred) and then
        # create the table fully-qualified inside that schema ONLY when
        # `DATABRICKS_ALLOW_SCHEMA_CREATE` is True. Otherwise we try a safe
        # read to check if table exists; if that fails we fall back to local CSV
        # persistence.
        with self._connect() as conn:
            with conn.cursor() as cursor:
                # Determine effective catalog/schema to use.
                # Prefer the configured catalog if available (it's explicit and user-tested).
                # Fall back to session current_catalog/current_schema.
                try:
                    cursor.execute("SELECT current_catalog(), current_schema()")
                    row = cursor.fetchone()
                    if row and len(row) >= 2:
                        current_catalog = row[0]
                        current_schema = row[1]
                    else:
                        current_catalog = None
                        current_schema = None
                except Exception:
                    current_catalog = None
                    current_schema = None

                # Prefer configured values (which user has tested/approved)
                # over session values (which may be problematic or inaccessible)
                catalog_to_use = self.catalog or current_catalog
                schema_to_use = self.schema or current_schema

                def q(*parts):
                    return ".".join([f"`{p}`" for p in parts if p])

                # If creation allowed, try to create schema and qualified table.
                if catalog_to_use and schema_to_use and DATABRICKS_ALLOW_SCHEMA_CREATE:
                    try:
                        create_schema_sql = f"CREATE SCHEMA IF NOT EXISTS {q(catalog_to_use, schema_to_use)}"
                        cursor.execute(create_schema_sql)
                    except Exception:
                        pass

                    qualified_table = q(catalog_to_use, schema_to_use, table_name)
                    create_sql_qualified = create_sql_unqualified.replace(table_name, qualified_table)
                    try:
                        cursor.execute(create_sql_qualified)
                        self._qualified_table = qualified_table
                        self.catalog = catalog_to_use
                        self.schema = schema_to_use
                        return
                    except Exception:
                        pass

                # If creation not allowed, try a lightweight existence check
                if catalog_to_use and schema_to_use and not DATABRICKS_ALLOW_SCHEMA_CREATE:
                    qualified_table = q(catalog_to_use, schema_to_use, table_name)
                    try:
                        cursor.execute(f"SELECT id FROM {qualified_table} LIMIT 1")
                        self._qualified_table = qualified_table
                        self.catalog = catalog_to_use
                        self.schema = schema_to_use
                        return
                    except Exception:
                        # mark SQL unavailable and fall back to CSV
                        self._available = False
                        return

                # If creation allowed, try unqualified/default creations. If those
                # fail, mark SQL unavailable so callers will fallback.
                if DATABRICKS_ALLOW_SCHEMA_CREATE:
                    try:
                        cursor.execute(create_sql_unqualified)
                        self._qualified_table = table_name
                        return
                    except Exception:
                        try:
                            cursor.execute(create_sql_default)
                            self._qualified_table = f"default.{table_name}"
                            return
                        except Exception:
                            self._available = False
                            return
                else:
                    # no creation rights, and no qualified table found earlier
                    self._available = False
                    return

    def _add_missing_columns(self, table_name: str = "upskilling_plans"):
        """Add missing columns to existing tables."""
        if not self._available:
            return
        
        target = getattr(self, "_qualified_table", f"default.{table_name}")
        
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    # Try to add mentee_name column if it doesn't exist
                    if table_name == "upskilling_plans":
                        try:
                            cursor.execute(f"ALTER TABLE {target} ADD COLUMN mentee_name STRING")
                        except Exception:
                            # Column might already exist, ignore
                            pass
        except Exception:
            # If we can't add columns, just continue
            pass

    def insert_plan(self, email: str, plan_text: str, mentee_name: str = "", progress: int = 0, notes: str = "") -> str:
        """Insert a new upskilling plan and return the record id."""
        rid = str(uuid.uuid4())
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        # Escape single quotes in plan_text and notes
        safe_plan = plan_text.replace("'", "''")
        safe_notes = notes.replace("'", "''")
        safe_name = mentee_name.replace("'", "''")

        # Ensure table exists (this will set self._qualified_table or mark SQL unavailable)
        self.ensure_table_exists()
        # Try to add missing columns
        self._add_missing_columns()
        
        if getattr(self, "_available", True) is False:
            # fallback to CSV persistence
            return self._csv_insert(rid, email, safe_name, now, plan_text, progress, notes)

        target = getattr(self, "_qualified_table", f"default.upskilling_plans")
        insert_sql = (
            f"INSERT INTO {target} (id, email, mentee_name, created_at, plan, progress, notes, last_updated) "
            f"VALUES ('{rid}', '{email}', '{safe_name}', '{now}', '{safe_plan}', {int(progress)}, '{safe_notes}', '{now}')"
        )
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(insert_sql)
        return rid

    def get_plans_by_email(self, email: str):
        """Return a list of dict records for the given email."""
        # Ensure we know the qualified table to query
        self.ensure_table_exists()
        if getattr(self, "_available", True) is False:
            return self._csv_get(email)

        target = getattr(self, "_qualified_table", f"default.upskilling_plans")
        
        # Try with mentee_name column first, fall back if it doesn't exist
        try:
            query = f"SELECT id, email, mentee_name, created_at, plan, progress, notes, last_updated FROM {target} WHERE email = '{email}' ORDER BY created_at DESC"
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    rows = cursor.fetchall()
                    cols = [c[0] for c in cursor.description]
        except Exception:
            # Fall back to query without mentee_name
            query = f"SELECT id, email, created_at, plan, progress, notes, last_updated FROM {target} WHERE email = '{email}' ORDER BY created_at DESC"
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    rows = cursor.fetchall()
                    cols = [c[0] for c in cursor.description]

        results = []
        for r in rows:
            rec = {cols[i]: r[i] for i in range(len(cols))}
            results.append(rec)
        return results

    def get_plans_by_name(self, mentee_name: str):
        """Return a list of dict records for the given mentee name."""
        # Ensure we know the qualified table to query
        self.ensure_table_exists()
        if getattr(self, "_available", True) is False:
            return self._csv_get_by_name(mentee_name)

        target = getattr(self, "_qualified_table", f"default.upskilling_plans")
        safe_name = mentee_name.replace("'", "''")
        
        try:
            query = f"SELECT id, email, mentee_name, created_at, plan, progress, notes, last_updated FROM {target} WHERE mentee_name = '{safe_name}' ORDER BY created_at DESC"
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    rows = cursor.fetchall()
                    cols = [c[0] for c in cursor.description]
        except Exception:
            # mentee_name column may not exist yet, return empty list
            return []

        results = []
        for r in rows:
            rec = {cols[i]: r[i] for i in range(len(cols))}
            results.append(rec)
        return results

    def update_progress(self, record_id: str, progress: int, notes: str = ""):
        """Update progress and notes for a given record id."""
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        safe_notes = notes.replace("'", "''")
        self.ensure_table_exists()
        if getattr(self, "_available", True) is False:
            return self._csv_update(record_id, progress, notes)

        target = getattr(self, "_qualified_table", f"default.upskilling_plans")
        update_sql = (
            f"UPDATE {target} "
            f"SET progress = {int(progress)}, notes = '{safe_notes}', last_updated = '{now}' "
            f"WHERE id = '{record_id}'"
        )
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(update_sql)

    # --- CSV fallback helpers ---
    def _csv_path(self):
        """Return the path to the CSV file for plan persistence."""
        base = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
        os.makedirs(base, exist_ok=True)
        return os.path.join(base, "upskilling_plans.csv")

    def _csv_insert(self, rid, email, mentee_name, now, plan_text, progress, notes):
        """Append a new plan record to the CSV file."""
        path = self._csv_path()
        headers = ["id", "email", "mentee_name", "created_at", "plan", "progress", "notes", "last_updated"]
        row = {"id": rid, "email": email, "mentee_name": mentee_name, "created_at": now, "plan": plan_text, "progress": int(progress), "notes": notes, "last_updated": now}
        write_header = not os.path.exists(path)
        with open(path, "a", newline='', encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            if write_header:
                writer.writeheader()
            writer.writerow(row)
        return rid

    def _csv_get(self, email):
        """Fetch all plans for a given email from the CSV file."""
        path = self._csv_path()
        if not os.path.exists(path):
            return []
        results = []
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                if r.get("email") == email:
                    # coerce progress to int
                    r["progress"] = int(r.get("progress") or 0)
                    results.append(r)
        # sort by created_at descending
        results.sort(key=lambda x: x.get("created_at") or "", reverse=True)
        return results

    def _csv_get_by_name(self, mentee_name):
        """Fetch all plans for a given mentee name from the CSV file."""
        path = self._csv_path()
        if not os.path.exists(path):
            return []
        results = []
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                if r.get("mentee_name") == mentee_name:
                    # coerce progress to int
                    r["progress"] = int(r.get("progress") or 0)
                    results.append(r)
        # sort by created_at descending
        results.sort(key=lambda x: x.get("created_at") or "", reverse=True)
        return results

    def _csv_update(self, record_id, progress, notes):
        """Update progress and notes for a record in the CSV file."""
        path = self._csv_path()
        if not os.path.exists(path):
            return False
        updated = False
        rows = []
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                if r.get("id") == record_id:
                    r["progress"] = str(int(progress))
                    r["notes"] = notes
                    r["last_updated"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                    updated = True
                rows.append(r)
        if updated and rows:
            with open(path, "w", newline='', encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
        return updated

    # --- Mentor Request Management ---
    def create_mentor_request(self, mentee_email: str, mentee_name: str, mentor_email: str, mentor_name: str) -> str:
        """Create a new mentor connection request."""
        rid = str(uuid.uuid4())
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        
        self.ensure_table_exists("mentor_requests")
        if getattr(self, "_available", True) is False:
            # Fallback to CSV for mentor requests
            return self._csv_insert_mentor_request(rid, mentee_email, mentee_name, mentor_email, mentor_name)
        
        # Use the qualified table name set during ensure_table_exists
        target = self._qualified_table if hasattr(self, "_qualified_table") else "`hackathon`.`default`.`mentor_requests`"
        safe_notes = "Connection request sent".replace("'", "''")
        
        insert_sql = (
            f"INSERT INTO {target} (id, mentee_email, mentee_name, mentor_email, mentor_name, status, created_at, notes) "
            f"VALUES ('{rid}', '{mentee_email}', '{mentee_name}', '{mentor_email}', '{mentor_name}', 'pending', '{now}', '{safe_notes}')"
        )
        
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(insert_sql)
        except Exception:
            # Fallback
            return self._csv_insert_mentor_request(rid, mentee_email, mentee_name, mentor_email, mentor_name)
        
        return rid

    def get_mentor_requests(self, mentor_email: str, status: str = None):
        """Get mentor requests for a specific mentor."""
        self.ensure_table_exists("mentor_requests")
        
        if getattr(self, "_available", True) is False:
            return self._csv_get_mentor_requests(mentor_email, status)
        
        # Use the qualified table name set during ensure_table_exists
        target = self._qualified_table if hasattr(self, "_qualified_table") else "`hackathon`.`default`.`mentor_requests`"
        
        if status:
            query = f"SELECT * FROM {target} WHERE mentor_email = '{mentor_email}' AND status = '{status}' ORDER BY created_at DESC"
        else:
            query = f"SELECT * FROM {target} WHERE mentor_email = '{mentor_email}' ORDER BY created_at DESC"
        
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    rows = cursor.fetchall()
                    cols = [c[0] for c in cursor.description]
            
            results = []
            for r in rows:
                rec = {cols[i]: r[i] for i in range(len(cols))}
                results.append(rec)
            return results
        except Exception:
            return self._csv_get_mentor_requests(mentor_email, status)

    def update_mentor_request(self, request_id: str, status: str, notes: str = ""):
        """Update status of a mentor request (accept/reject)."""
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        safe_notes = notes.replace("'", "''")
        
        self.ensure_table_exists("mentor_requests")
        if getattr(self, "_available", True) is False:
            return self._csv_update_mentor_request(request_id, status, notes)
        
        # Use the qualified table name set during ensure_table_exists
        target = self._qualified_table if hasattr(self, "_qualified_table") else "`hackathon`.`default`.`mentor_requests`"
        
        update_sql = (
            f"UPDATE {target} "
            f"SET status = '{status}', responded_at = '{now}', notes = '{safe_notes}' "
            f"WHERE id = '{request_id}'"
        )
        
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(update_sql)
        except Exception:
            return self._csv_update_mentor_request(request_id, status, notes)

    # --- CSV Mentor Request Fallback ---
    def _csv_insert_mentor_request(self, rid, mentee_email, mentee_name, mentor_email, mentor_name):
        """Save mentor request to CSV."""
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "mentor_requests.csv")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        headers = ["id", "mentee_email", "mentee_name", "mentor_email", "mentor_name", "status", "created_at", "responded_at", "notes"]
        row = {
            "id": rid,
            "mentee_email": mentee_email,
            "mentee_name": mentee_name,
            "mentor_email": mentor_email,
            "mentor_name": mentor_name,
            "status": "pending",
            "created_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            "responded_at": "",
            "notes": "Connection request sent"
        }
        
        write_header = not os.path.exists(path)
        with open(path, "a", newline='', encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            if write_header:
                writer.writeheader()
            writer.writerow(row)
        
        return rid

    def _csv_get_mentor_requests(self, mentor_email, status=None):
        """Get mentor requests from CSV."""
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "mentor_requests.csv")
        if not os.path.exists(path):
            return []
        
        results = []
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                if r.get("mentor_email") == mentor_email:
                    if status is None or r.get("status") == status:
                        results.append(r)
        
        results.sort(key=lambda x: x.get("created_at") or "", reverse=True)
        return results

    def _csv_update_mentor_request(self, request_id, status, notes):
        """Update mentor request in CSV."""
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "mentor_requests.csv")
        if not os.path.exists(path):
            return False
        
        updated = False
        rows = []
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                if r.get("id") == request_id:
                    r["status"] = status
                    r["responded_at"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                    r["notes"] = notes
                    updated = True
                rows.append(r)
        
        if updated and rows:
            with open(path, "w", newline='', encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
        
        return updated

    # --- Notifications System ---
    def create_notification(self, recipient_email: str, recipient_name: str, notification_type: str, 
                           title: str, message: str, related_id: str = None) -> str:
        """Create a notification for a user."""
        nid = str(uuid.uuid4())
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        
        self.ensure_table_exists("notifications")
        if getattr(self, "_available", True) is False:
            return self._csv_create_notification(nid, recipient_email, recipient_name, notification_type, title, message, related_id)
        
        target = self._qualified_table if hasattr(self, "_qualified_table") else "`hackathon`.`default`.`notifications`"
        safe_message = message.replace("'", "''")
        safe_title = title.replace("'", "''")
        
        insert_sql = (
            f"INSERT INTO {target} (id, recipient_email, recipient_name, type, title, message, related_id, created_at, is_read) "
            f"VALUES ('{nid}', '{recipient_email}', '{recipient_name}', '{notification_type}', '{safe_title}', '{safe_message}', '{related_id or ''}', '{now}', false)"
        )
        
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(insert_sql)
        except Exception:
            return self._csv_create_notification(nid, recipient_email, recipient_name, notification_type, title, message, related_id)
        
        return nid

    def get_notifications(self, recipient_email: str, unread_only: bool = False):
        """Get notifications for a user."""
        self.ensure_table_exists("notifications")
        
        if getattr(self, "_available", True) is False:
            return self._csv_get_notifications(recipient_email, unread_only)
        
        target = self._qualified_table if hasattr(self, "_qualified_table") else "`hackathon`.`default`.`notifications`"
        
        if unread_only:
            query = f"SELECT * FROM {target} WHERE recipient_email = '{recipient_email}' AND is_read = false ORDER BY created_at DESC"
        else:
            query = f"SELECT * FROM {target} WHERE recipient_email = '{recipient_email}' ORDER BY created_at DESC"
        
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    rows = cursor.fetchall()
                    cols = [c[0] for c in cursor.description]
            
            results = []
            for r in rows:
                rec = {cols[i]: r[i] for i in range(len(cols))}
                results.append(rec)
            return results
        except Exception:
            return self._csv_get_notifications(recipient_email, unread_only)

    def mark_notification_read(self, notification_id: str):
        """Mark a notification as read."""
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        
        self.ensure_table_exists("notifications")
        if getattr(self, "_available", True) is False:
            return self._csv_mark_notification_read(notification_id)
        
        target = self._qualified_table if hasattr(self, "_qualified_table") else "`hackathon`.`default`.`notifications`"
        
        update_sql = (
            f"UPDATE {target} SET is_read = true, read_at = '{now}' WHERE id = '{notification_id}'"
        )
        
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(update_sql)
        except Exception:
            return self._csv_mark_notification_read(notification_id)

    # --- CSV Notification Fallback ---
    def _csv_create_notification(self, nid, recipient_email, recipient_name, notification_type, title, message, related_id):
        """Save notification to CSV."""
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "notifications.csv")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        headers = ["id", "recipient_email", "recipient_name", "type", "title", "message", "related_id", "created_at", "read_at", "is_read"]
        row = {
            "id": nid,
            "recipient_email": recipient_email,
            "recipient_name": recipient_name,
            "type": notification_type,
            "title": title,
            "message": message,
            "related_id": related_id or "",
            "created_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            "read_at": "",
            "is_read": "false"
        }
        
        write_header = not os.path.exists(path)
        with open(path, "a", newline='', encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            if write_header:
                writer.writeheader()
            writer.writerow(row)
        
        return nid

    def _csv_get_notifications(self, recipient_email, unread_only=False):
        """Get notifications from CSV."""
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "notifications.csv")
        if not os.path.exists(path):
            return []
        
        results = []
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                if r.get("recipient_email") == recipient_email:
                    if unread_only and r.get("is_read") == "true":
                        continue
                    results.append(r)
        
        results.sort(key=lambda x: x.get("created_at") or "", reverse=True)
        return results

    def _csv_mark_notification_read(self, notification_id):
        """Mark notification as read in CSV."""
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "notifications.csv")
        if not os.path.exists(path):
            return False
        
        updated = False
        rows = []
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                if r.get("id") == notification_id:
                    r["is_read"] = "true"
                    r["read_at"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                    updated = True
                rows.append(r)
        
        if updated and rows:
            with open(path, "w", newline='', encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
        
        return updated
