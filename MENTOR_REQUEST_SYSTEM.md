# Mentor Request System - Implementation Complete ✅

## Overview

The mentor request system has been fully implemented with persistent Databricks SQL storage and a complete UI workflow for mentees to request mentor connections and mentors to accept/reject them.

## Features Implemented

### 1. **Mentor Request Management (DatabricksSQLClient)**

Three new methods added to `src/databricks_sql.py`:

#### `create_mentor_request(mentee_email, mentee_name, mentor_email, mentor_name) → request_id`
- Creates a new mentor connection request in `hackathon.default.mentor_requests` table
- Status: `pending` (default)
- Returns unique request ID (UUID)
- Falls back to CSV (`data/mentor_requests.csv`) if SQL unavailable

#### `get_mentor_requests(mentor_email, status=None)`
- Retrieves all requests for a specific mentor
- Optional `status` filter: `pending`, `accepted`, or `rejected`
- Returns list of dictionaries with fields:
  - `id`: UUID
  - `mentee_email`: Requester's email
  - `mentee_name`: Requester's name
  - `mentor_email`: Mentor's email
  - `mentor_name`: Mentor's name
  - `status`: Current status (pending/accepted/rejected)
  - `created_at`: Request creation timestamp
  - `responded_at`: When mentor responded (null for pending)
  - `notes`: Mentor's response/notes

#### `update_mentor_request(request_id, status, notes="")`
- Updates request status to `accepted` or `rejected`
- Records `responded_at` timestamp
- Stores optional mentor notes/response message
- Supports CSV fallback

### 2. **Databricks SQL Table Schema**

**Table:** `hackathon.default.mentor_requests`

```sql
CREATE TABLE mentor_requests (
  id STRING,                -- UUID
  mentee_email STRING,      -- Requester's email
  mentee_name STRING,       -- Requester's name
  mentor_email STRING,      -- Mentor's email
  mentor_name STRING,       -- Mentor's name
  status STRING,            -- pending|accepted|rejected
  created_at TIMESTAMP,     -- Request creation time
  responded_at TIMESTAMP,   -- When mentor responded
  notes STRING              -- Mentor response message
)
USING DELTA
```

### 3. **UI Components**

#### **Mentee Interface (Existing with Enhancement)**
- **Location:** `render_mentee_chatbot()` in `app.py`
- **Feature:** "🤝 Connect with Mentor" button next to each recommended mentor
- **Behavior:**
  - Mentee clicks button → connection request sent to mentor
  - Request persisted to Databricks SQL (or CSV fallback)
  - Success message and balloons animation
  - Uses mentee's name from profile and mentor's email from recommendations

#### **Mentor Dashboard (NEW)**
- **Location:** `render_mentor_dashboard()` in `app.py`
- **Sections:**
  1. **Profile Card:** Shows mentor name, email, role
  2. **Statistics Metrics:**
     - Pending Requests count
     - Accepted Mentees count
  3. **Pending Mentee Requests Section:**
     - List of all pending connection requests
     - For each request shows: Mentee name, email, request timestamp
     - Action buttons: ✅ Accept | ❌ Reject
     - Clicking Accept/Reject updates status in database with timestamp
  4. **Active Mentee Connections Section:**
     - List of all accepted connections
     - Shows mentee name, email, acceptance timestamp
     - Read-only display of active relationships

### 4. **CSV Fallback**

All mentor request operations have CSV fallback implementation:

- **File:** `data/mentor_requests.csv`
- **Location:** Parallel structure to upskilling plans fallback
- **Fields:** Same as SQL table schema
- **Auto-creation:** CSV file created on first write if unavailable
- **Behavior:** Activated when SQL connections fail

## Testing

### Test Files Created

#### `test_mentor_requests.py`
Tests individual CRUD operations:
- ✅ Create mentor request
- ✅ Get all requests for mentor
- ✅ Get pending requests with filter
- ✅ Update request status to accepted
- ✅ Verify status change

**Result:** All 5 tests PASSED

#### `test_e2e_workflow.py`
Complete end-to-end integration test simulating real user workflow:

**Steps Tested:**
1. ✅ Mentee creates upskilling plan
2. ✅ Mentee sends connection request to mentor
3. ✅ Mentor views pending requests
4. ✅ Mentor accepts connection request
5. ✅ Status change verified (pending → accepted)
6. ✅ Request rejection workflow tested
7. ✅ Mentor statistics verified

**Result:** All 7 workflow steps PASSED

## How to Use

### For Mentees

1. Log in as mentee (e.g., `jane_mentee` / `password`)
2. Follow the chatbot steps to generate an upskilling plan
3. View recommended mentors at the end of the conversation
4. Click "🤝 Connect with Mentor" button next to desired mentor
5. See confirmation: "✅ Connection request sent to [Mentor Name]!"
6. Request is saved to Databricks SQL with timestamp

### For Mentors

1. Log in as mentor (e.g., `john_mentor` / `password`)
2. Go to Mentor Dashboard (auto-shown if logged in as mentor)
3. View pending requests in "🔔 Pending Mentee Requests" section
4. For each request, see:
   - Mentee name and email
   - Request timestamp
   - Accept/Reject buttons
5. Click "✅ Accept" to accept a mentee
   - Status changes to "accepted"
   - Moved to "✅ Active Mentee Connections" section
6. Click "❌ Reject" to decline
   - Status changes to "rejected"
   - Removed from pending list

### Data Storage

- **Primary:** Databricks SQL (`hackathon.default.mentor_requests`)
- **Fallback:** Local CSV (`data/mentor_requests.csv`)
- **Selection:** Automatic - SQL used if available, CSV used if SQL fails
- **Persistence:** All data persisted between sessions

## Architecture & Integration

### Files Modified

1. **`src/databricks_sql.py`**
   - Added 3 new public methods for mentor requests
   - Added 3 CSV fallback helper methods
   - Integrated with existing `ensure_table_exists()` for table creation
   - Supports both SQL and CSV persistence

2. **`app.py`**
   - Updated `render_mentor_dashboard()` - complete rewrite with request management UI
   - Enhanced "🤝 Connect with Mentor" button to call `sql_client.create_mentor_request()`
   - Mentor dashboard auto-shows when mentor user logs in

3. **`data/mentors_sample.csv`** (Previously updated)
   - Password column set to "pwd" for all mentors for authentication

### No Breaking Changes
- All existing functionality preserved
- Mentee chatbot workflow unchanged
- Upskilling plan persistence unchanged
- Authentication system unchanged
- CSV fallback mechanism maintained

## Database Schema Details

### Mentor Requests Table

```
Column Name    | Type      | Notes
---------------|-----------|------
id             | STRING    | UUID, primary identifier
mentee_email   | STRING    | Unique requester identifier
mentee_name    | STRING    | Display name
mentor_email   | STRING    | Request recipient
mentor_name    | STRING    | Recipient display name
status         | STRING    | pending/accepted/rejected
created_at     | TIMESTAMP | Request creation timestamp
responded_at   | TIMESTAMP | When mentor responded (null if pending)
notes          | STRING    | Mentor's response message
```

### Example Data Flow

```
Mentee: jane_mentee@example.com (Jane Doe)
Action: Clicks "Connect" for mentor john_mentor@example.com (John Smith)

Created Row:
{
  id: "550e8400-e29b-41d4-a716-446655440000",
  mentee_email: "jane_mentee@example.com",
  mentee_name: "Jane Doe",
  mentor_email: "john_mentor@example.com",
  mentor_name: "John Smith",
  status: "pending",
  created_at: "2026-01-28 21:46:56+00:00",
  responded_at: null,
  notes: "Connection request sent"
}

After mentor accepts:
{
  ...same fields...
  status: "accepted",
  responded_at: "2026-01-28 21:47:03+00:00",
  notes: "I'd be happy to help you learn Python!"
}
```

## Performance Considerations

- **SQL Queries:** Indexed by mentor_email; limited result sets with status filter
- **CSV Fallback:** O(n) read/write but suitable for demo/testing use
- **Scalability:** Databricks SQL scales to millions of requests; CSV suitable for <1000 records
- **Timestamps:** Stored as TIMESTAMP; UI formats for display

## Future Enhancements (Optional)

1. **Notifications:** Email/SMS when request status changes
2. **Messaging:** Direct message channel between mentor-mentee pairs
3. **Scheduling:** Meeting scheduler for accepted mentorship relationships
4. **Reviews:** Mentees rate mentors after mentorship completion
5. **Analytics:** Dashboard showing mentorship metrics and outcomes
6. **Profile Customization:** Mentors set availability, bio, mentee capacity limits

## Troubleshooting

### "Could not send request - database unavailable"
- Check Databricks credentials in `.env`
- Verify `DATABRICKS_CATALOG=hackathon` setting
- SQL client will automatically fall back to CSV
- Check `data/mentor_requests.csv` for fallback data

### Requests not appearing for mentor
- Verify mentor email matches exactly in requests (case-sensitive)
- Check database connection: run `test_mentor_requests.py`
- Try logging out and back in to refresh data

### Timestamps showing in ISO format
- App displays raw TIMESTAMP values; can be formatted in future enhancement
- All timestamps stored in UTC for consistency

## Validation Checklist

- ✅ SQL client initializes without errors
- ✅ Mentor request table created in `hackathon.default`
- ✅ create_mentor_request() creates row with unique ID
- ✅ get_mentor_requests() retrieves with status filtering
- ✅ update_mentor_request() changes status and timestamp
- ✅ CSV fallback works when SQL unavailable
- ✅ Mentee UI button calls SQL method with correct parameters
- ✅ Mentor dashboard displays pending requests
- ✅ Accept/Reject buttons update status in database
- ✅ Accepted connections move to separate section
- ✅ End-to-end workflow test passes all 7 steps
- ✅ No syntax errors in Python files
- ✅ No breaking changes to existing features

## Summary

The mentor request system is fully functional and integrated. Mentees can now request mentor connections which are persisted in Databricks SQL, and mentors have a dedicated dashboard to view, accept, and reject those requests. The system includes automatic CSV fallback for resilience and has been thoroughly tested with both unit and end-to-end tests.
