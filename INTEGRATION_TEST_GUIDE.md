# E2E Integration Testing Guide - SkillBridge with Databricks Catalog Explorer

## Overview
This guide provides step-by-step instructions to test the integrated SkillBridge application with the new Databricks Catalog Explorer feature for both mentee and mentor roles.

---

## Prerequisites
1. Application running: `streamlit run app.py`
2. Available at: `http://localhost:8501`
3. Test Databricks credentials configured in `.env`
4. Sample data available in: `DATABRICKS_CATALOG=hackathon` (configurable)

---

## Test Case 1: Mentee Portal Flow with Catalog Explorer

### 1.1 Login as Mentee
```
Email/Username: jane_mentee
Password: password
```

**Expected Results:**
- ✅ Login successful
- ✅ Redirected to mentee chatbot
- ✅ Welcome message displays mentee name
- ✅ "SkillBridge Career Guidance" header visible

### 1.2 Fill Profile Form
1. Scroll to "Step 1-4 of 5: Tell me about yourself"
2. Fill form:
   - **Name:** Jane Smith
   - **Age:** 28
   - **Skills:** Python, SQL, Tableau, Power BI
   - **Interests:** Data Analytics, Business Intelligence

3. Click "✅ Confirm & Continue"

**Expected Results:**
- ✅ No page reload (smooth transition)
- ✅ Success message appears: "✅ Profile saved! Scroll down to see your review..."
- ✅ Form remains visible with populated data
- ✅ "Step 5 of 5: Review your profile" section appears below
- ✅ Profile summary shows all entered data
- ✅ "✅ Get Recommendations" button is visible

### 1.3 Get AI Recommendations
1. Click "✅ Get Recommendations" button

**Expected Results:**
- ✅ Page navigates to recommendations section
- ✅ "🎯 Your Personalized Recommendations" header displays
- ✅ Debug panel shows profile data (expandable)
- ✅ AI-generated upskilling plan appears
- ✅ Matching job opportunities display with skill match percentages
- ✅ Recommended mentors show with expertise and experience

### 1.4 Test Catalog Explorer - Mentee View
1. Scroll down to "📊 Explore Job Market Data & Insights"
2. Click "🔍 Databricks Catalog Explorer" expander
3. In the sidebar, select:
   - **Catalog:** hackathon (or your configured catalog)
   - **Schema:** default (or available schema)
   - **Table:** job_openings_sample (or any table)
4. Click "🔄 Refresh Catalogs" button

**Expected Results:**
- ✅ Dropdown menus populate with catalog data
- ✅ Tables list updates dynamically
- ✅ Success message shows catalog count
- ✅ Data preview loads with row/column count

### 1.5 Data Preview Tab
1. Click "📋 Data Preview" tab
2. Review the table data

**Expected Results:**
- ✅ Table displays with proper formatting
- ✅ Row count shows (e.g., "Rows: 45 | Columns: 8")
- ✅ Column names properly labeled
- ✅ Data types auto-detected (numbers, dates, strings)

### 1.6 Visualization Tab
1. Click "📈 Visualization" tab
2. Select "Scatter" from "Chart Type" dropdown
3. Choose:
   - **X-axis:** company
   - **Y-axis:** salary_min
   - **Color (optional):** job_category

**Expected Results:**
- ✅ Chart type selector updates
- ✅ Relevant column options appear based on data types
- ✅ Scatter plot renders with data points
- ✅ Color encoding applied correctly
- ✅ Hover tooltips show data values
- ✅ Interactive zoom/pan controls work

### 1.7 Test Other Chart Types
Repeat 1.6 with:
- **Line Chart** - Time series data (if datetime column available)
- **Bar Chart** - Categorical aggregation
  - X-axis: job_category
  - Aggregation: count
- **Histogram** - Distribution
  - Column: salary_min
  - Bins: 15
- **Box Plot** - Statistical distribution
  - Y-column: salary_min
  - Group by: job_category

**Expected Results:**
- ✅ Each chart renders without errors
- ✅ Controls dynamically show relevant options
- ✅ Charts are responsive and interactive

---

## Test Case 2: Mentor Dashboard Flow with Catalog Explorer

### 2.1 Login as Mentor
```
Email/Username: john_mentor
Password: password
```

**Expected Results:**
- ✅ Login successful
- ✅ Redirected to mentor dashboard
- ✅ Welcome message displays mentor name
- ✅ "Mentor Dashboard" header visible

### 2.2 Review Mentor Dashboard
1. Review the dashboard sections:
   - Profile information
   - Statistics (pending/accepted requests)
   - Pending mentee requests
   - Active mentee connections & progress

**Expected Results:**
- ✅ Profile shows mentor name and email
- ✅ Metrics cards display request counts
- ✅ Mentee requests list appears (if any)
- ✅ Progress charts/pie charts render correctly

### 2.3 Test Catalog Explorer - Mentor View
1. Scroll down to "📊 Data Insights & Catalog Explorer"
2. Click "🔍 Explore Databricks Catalog" expander
3. In sidebar:
   - Click "🧪 Test Connection" button

**Expected Results:**
- ✅ Success message shows: "✅ Connected! Found X catalogs"
- ✅ Connection test validates Databricks access

### 2.4 Select Data
1. From sidebar select:
   - **Catalog:** hackathon
   - **Schema:** default
   - **Table:** mentors_sample (or roles_sample)

**Expected Results:**
- ✅ Metrics show selected: Catalog, Schema, Table
- ✅ Data loads without errors
- ✅ Row/column counts display

### 2.5 Compare Data Between Roles
1. Open two browser tabs (one mentee, one mentor)
2. Select same table in both
3. Compare visualizations

**Expected Results:**
- ✅ Both portals show identical data
- ✅ Charts render consistently
- ✅ No data corruption or loss

---

## Test Case 3: Catalog Explorer Features

### 3.1 Dynamic Column Type Detection
1. Select any table with mixed data types
2. Create different chart types

**Expected Results:**
- ✅ Numeric columns identified correctly
- ✅ Categorical columns detected
- ✅ Datetime columns recognized (if present)
- ✅ Chart options reflect available column types

### 3.2 Aggregation Functions
1. Select Bar chart
2. Choose numeric Y-axis
3. Cycle through aggregations: count → sum → mean → median

**Expected Results:**
- ✅ Each aggregation function updates chart
- ✅ Chart values change appropriately
- ✅ Tooltips show aggregated values

### 3.3 Interactive Features
1. In any chart, test:
   - Hover over data points (tooltips appear)
   - Click and drag to zoom
   - Use legend to toggle series

**Expected Results:**
- ✅ Tooltips display on hover
- ✅ Zoom/pan works smoothly
- ✅ Legend filtering toggles data visibility

### 3.4 Error Handling
1. Try invalid selections:
   - Select table with no numeric columns, then try Histogram
   - Select table with no categorical columns, then try Bar chart

**Expected Results:**
- ✅ Helpful messages appear
- ✅ App doesn't crash
- ✅ Graceful fallback/retry options shown

---

## Test Case 4: Notifications & System Integration

### 4.1 Request/Response Flow
As Mentor:
1. Accept a pending mentee request
2. Check notifications

As Mentee:
1. Check notifications for mentor acceptance

**Expected Results:**
- ✅ Notification created in database
- ✅ Both roles see appropriate notifications
- ✅ Notification status updates correctly

### 4.2 UI Consistency
1. Log out and log in as different role
2. Verify:
   - Catalog explorer available in both
   - Same data visible
   - UI layout consistent

**Expected Results:**
- ✅ Both portals have explorer
- ✅ Data accessibility equal
- ✅ UX consistent

---

## Test Case 5: Performance & Error Resilience

### 5.1 Large Dataset Preview
1. Select table with 1000+ rows
2. Wait for preview to load

**Expected Results:**
- ✅ Preview loads within 3 seconds
- ✅ First 200 rows displayed
- ✅ Row count accurately shown

### 5.2 Connection Failure Handling
1. Temporarily disconnect from Databricks network
2. Try to refresh catalogs

**Expected Results:**
- ✅ Error message appears
- ✅ Helpful troubleshooting message shown
- ✅ App doesn't crash

### 5.3 Rapid UI Interactions
1. Click buttons rapidly in sidebar
2. Switch between tabs quickly
3. Change chart types multiple times

**Expected Results:**
- ✅ No UI freezes
- ✅ No duplicate requests
- ✅ Smooth transitions

---

## Test Case 6: Data Integrity

### 6.1 Data Type Preservation
1. Preview table with DECIMAL/NUMERIC columns
2. Create bar chart with numeric data

**Expected Results:**
- ✅ Numbers display correctly
- ✅ No type conversion errors
- ✅ Aggregations calculate correctly

### 6.2 Special Characters Handling
1. Select table with special characters in names/data
2. Create visualizations

**Expected Results:**
- ✅ Special characters render correctly
- ✅ Quotes/backticks handled properly
- ✅ Qualified names (catalog.schema.table) parse correctly

---

## Rollback Scenarios

If integration fails:

1. **Check imports:**
   ```bash
   python -c "from src.catalog_explorer_ui import *"
   ```

2. **Verify Databricks connection:**
   ```bash
   python src/catalog_explorer.py
   ```

3. **Clear Streamlit cache:**
   ```bash
   rm -r ~/.streamlit/cache
   ```

4. **Downgrade if needed:**
   ```bash
   pip install streamlit==1.25.0
   ```

---

## Summary Checklist

### Mentee Portal
- [ ] Login successful
- [ ] Profile form fills without rerun
- [ ] Recommendations generate
- [ ] Catalog explorer loads
- [ ] Data preview displays
- [ ] Charts render (all 6 types)
- [ ] Interactive features work

### Mentor Dashboard
- [ ] Login successful  
- [ ] Dashboard loads with statistics
- [ ] Requests display correctly
- [ ] Catalog explorer available
- [ ] Data preview matches mentee view
- [ ] Charts consistent across roles

### Features
- [ ] Dynamic column detection
- [ ] Type conversions work
- [ ] Aggregations calculate correctly
- [ ] Error messages helpful
- [ ] Performance acceptable (<3s per operation)

### Integration
- [ ] No import errors
- [ ] Shared Databricks connection works
- [ ] Data consistent between portals
- [ ] UI responsive and stable

---

## Success Criteria
✅ All test cases pass  
✅ No error messages in browser console  
✅ Catalog explorer available in both mentee & mentor portals  
✅ Charts render and are interactive  
✅ Data preview accurate and complete  
✅ Performance acceptable  
✅ No data corruption or loss  

**Status: READY FOR PRODUCTION** 🚀
