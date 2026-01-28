# End-to-End Testing Guide: Mentor Dashboard with Progress Tracking

## 📋 Overview

This guide provides step-by-step instructions to test the complete mentor mentoring workflow including:
- Mentee creating upskilling plans with progress tracking
- Mentor accepting connections
- Real-time progress visualization in mentor dashboard
- Pie chart showing mentee progress distribution

## 🎯 Test Objectives

1. ✅ Mentee completes chatbot and generates upskilling plan
2. ✅ Mentee requests mentor connection
3. ✅ Mentor receives and accepts request
4. ✅ Mentor dashboard shows pie chart of mentees and their progress
5. ✅ Progress updates reflect in real-time
6. ✅ Multiple mentees can be mentored simultaneously
7. ✅ Dashboard metrics and visualizations update correctly

## 📅 Test Scenarios

### Scenario 1: Single Mentee Progress Tracking (15 minutes)

**Setup:** One mentee, one mentor, track single mentee's progress

#### Step 1: Start the Application
```bash
cd c:\workspace\ai_coach_app
streamlit run app.py
```
- Wait for Streamlit to start
- Should see login page at http://localhost:8501

#### Step 2: Mentee Creates Upskilling Plan
**User:** jane_mentee / password

1. Login
   - Username: `jane_mentee`
   - Password: `password`
   - Click "Sign In"
   - ✅ Expected: Login successful, redirected to chatbot

2. Complete Chatbot Steps
   - **Step 1 - Name:** Enter "Jane Doe"
   - **Step 2 - Age:** Enter "28"
   - **Step 3 - Skills:** Select Python, Data Analysis (check both)
   - **Step 4 - Interests:** Enter "Machine Learning, Deep Learning"
   - **Step 5 - Confirmation:** Click "Confirm & Continue"
   - ✅ Expected: Progress bar fills to Step 5

3. Generate Upskilling Plan
   - Click "Generate Upskilling Plan" button
   - ✅ Expected: AI-generated plan appears in a container
   - ✅ Plan shows: "Upskilling Plan for Jane Doe (Mentee)"
   - ✅ Can see generated content
   - Note down plan progress (should be 0%)

4. View Mentor Recommendations
   - Scroll down to "👨‍🏫 Recommended Mentors" section
   - Should see: John Smith, Sarah Chen, etc.
   - ✅ Expected: 3 mentor recommendations with match scores

#### Step 3: Mentee Updates Plan Progress
1. Scroll back to "📊 Your Previous Plans" section
2. Find the plan you just created
3. Use the progress slider to increase progress to 25%
   - ✅ Expected: Slider updates, progress shows "🟡 25%"
   - ✅ Database updates with new progress
   - Note: This simulates mentee work on the upskilling plan

#### Step 4: Mentee Requests Mentor Connection
1. Scroll to "👨‍🏫 Recommended Mentors" section
2. Find "John Smith" (Data Science & ML mentor)
3. Click "🤝 Connect with Mentor" button
   - ✅ Expected: Success message "✅ Connection request sent to John Smith!"
   - ✅ Balloons animation appears
   - ✅ Request saved to database

4. Update progress one more time (25% → 50%)
   - Scroll to "Your Previous Plans"
   - Move slider to 50%
   - ✅ Expected: Progress updates to 🟠 50%

#### Step 5: Mentor Reviews Dashboard
**User:** john_mentor / password

1. Logout mentee
   - Click logout button (if visible) or just navigate away
   - Or open new browser tab/window

2. Login as Mentor
   - Username: `john_mentor`
   - Password: `password`
   - Click "Sign In"
   - ✅ Expected: Mentor dashboard loads (not chatbot)

3. View Pending Requests
   - Look for "🔔 Pending Mentee Requests" section
   - ✅ Expected: See "Jane Doe" request with:
     - Name: Jane Doe
     - Email: jane_mentee@example.com
     - Request timestamp
     - Accept/Reject buttons

4. Accept Request
   - Click "✅ Accept" button next to Jane's request
   - ✅ Expected: Message "✅ Accepted request from Jane Doe!"
   - ✅ Page reloads
   - ✅ Jane's request moves from "Pending" to "Active Mentee Connections"

#### Step 6: View Progress in Mentor Dashboard
1. Mentor scrolls to "✅ Active Mentee Connections & Progress" section
   - ✅ Expected: Pie chart appears showing:
     - Jane Doe's name in pie chart
     - 50% progress (blue/gray slice)
     - Color coding: 🟠 (50% = orange/yellow range)

2. Check Progress Details
   - Look at right side metrics:
     - **Plans Created:** 1
     - **Avg Progress:** 50%
     - **Accepted:** [timestamp]
   - ✅ Expected: All metrics match data from mentee's actions

3. Visual Verification
   - Pie chart shows "Jane Doe 50%"
   - Progress bar shows filled to 50%
   - Color indicator shows 🟠 (orange/yellow)

#### Step 7: Back to Mentee - Increase Progress Further
**User:** jane_mentee / password (new session)

1. Login again as jane_mentee
2. Go to "Your Previous Plans" section
3. Update progress to 75%
   - ✅ Expected: Slider moves, shows 🟠 75%

4. Logout (or just note the change)

#### Step 8: Mentor Refreshes and Sees Updated Progress
**User:** john_mentor / password (refresh or relogin)

1. Refresh the page (F5) or logout/login
2. View "✅ Active Mentee Connections & Progress" section again
   - ✅ Expected: Progress shows 75% now
   - ✅ Pie chart shows Jane Doe 75%
   - ✅ Progress bar fills to 75%
   - ✅ Color updates to 🟠 (still orange/yellow at 75%)

**Test 1 Result:** ✅ Single mentee progress tracking working

---

### Scenario 2: Multiple Mentees Progress Distribution (20 minutes)

**Setup:** Multiple mentees, same mentor, pie chart distribution

#### Step 1: Create Second Mentee's Plan
**User:** alice_mentee / password

1. Login as alice_mentee (or another mentee user)
   - If alice_mentee doesn't exist, use jane_mentee in different session
   - Note: You'll need another mentee account - for now, simulate by creating another plan with jane_mentee

2. Complete chatbot:
   - Name: "Alice Johnson"
   - Age: "32"
   - Skills: Web Development, React (check both)
   - Interests: "Frontend Development, React Best Practices"
   - Click "Confirm & Continue"

3. Generate Plan
   - Click "Generate Upskilling Plan"
   - ✅ Expected: New plan generated for Alice

4. Set Progress to 20%
   - Find plan in "Your Previous Plans"
   - Move slider to 20%
   - ✅ Expected: Shows 🔴 20%

5. Request Mentor
   - Scroll to "👨‍🏫 Recommended Mentors"
   - Find "Emily Watson" (Frontend Development)
   - Click "🤝 Connect with Mentor"
   - ✅ Expected: Request sent

#### Step 2: Multiple Mentor Scenario (If you have multiple mentor accounts)

**Alternative:** Have both Jane and Alice request the same mentor (John Smith)

1. **Jane:** Request John Smith (already done from Scenario 1)
   - Progress: 75%

2. **Alice:** Request John Smith
   - Follow steps above but select John Smith instead of Emily
   - Progress: 20%

#### Step 3: View Pie Chart with Multiple Mentees
**User:** john_mentor / password

1. Logout jane/alice and login as john_mentor
2. Refresh page
3. View "✅ Active Mentee Connections & Progress" section
   - ✅ Expected: Pie chart shows TWO slices
   - ✅ Jane Doe: 75%
   - ✅ Alice Johnson: 20%
   - ✅ Pie chart has different colors for each mentee

4. View Progress Details (right panel)
   - ✅ Expected: Both mentees listed with:
     - Individual progress bars
     - Plans created count
     - Average progress %
     - Color-coded indicators

5. Hover over pie chart slices
   - ✅ Expected: Tooltip shows mentee name and progress %

#### Step 4: Update Progress and Observe Pie Chart Changes
**User:** jane_mentee / password

1. Login as jane_mentee
2. Update progress to 100%
   - ✅ Expected: Shows 🟢 100%

3. Logout

**User:** john_mentor / password

1. Refresh mentor dashboard
2. View pie chart
   - ✅ Expected: Jane's slice grows to 100%
   - ✅ Color changes to 🟢 (green) for completion
   - ✅ Alice's slice remains at 20%

**Test 2 Result:** ✅ Multiple mentee distribution working

---

### Scenario 3: Edge Cases & Error Handling (10 minutes)

#### Test 3.1: Mentor with No Active Connections
1. Login as different mentor (e.g., sarah_chen)
   - If doesn't exist in roles, create one or skip
   - Or logout john_mentor and relogin

2. View dashboard
   - ✅ Expected: "No active connections yet. Accept a pending request..."
   - ✅ No pie chart shown
   - ✅ No error messages

#### Test 3.2: Mentee with No Plans Yet
1. Have mentee request mentor but don't create plan
   - Create new chatbot session
   - Go to mentor recommendations
   - Request mentor WITHOUT generating plan first

2. Mentor accepts
3. View mentor dashboard
   - ✅ Expected: Mentee shows 0% progress
   - ✅ Pie chart shows mentee at 0%
   - ✅ "Plans Created: 0"
   - ✅ No error messages

#### Test 3.3: Database Unavailable (CSV Fallback)
1. Temporarily disable Databricks (rename .env or invalidate credentials)
2. Repeat mentee → mentor → progress update workflow
   - ✅ Expected: System works with CSV fallback
   - ✅ All data persists
   - ✅ Pie chart still displays

3. Re-enable Databricks

**Test 3 Result:** ✅ Edge cases handled

---

## 📊 Verification Checklist

### Chatbot & Plan Creation
- ✅ Chatbot progresses through 5 steps
- ✅ Upskilling plan generated by AI
- ✅ Plan shown with mentee name
- ✅ Plan progress slider works
- ✅ Progress updates database

### Mentor Request System
- ✅ "Connect with Mentor" button creates request
- ✅ Request appears in mentor's pending section
- ✅ Mentor can accept/reject
- ✅ Status changes in database
- ✅ UI updates after accept/reject

### Mentor Dashboard - Pie Chart
- ✅ Pie chart appears when mentee connections exist
- ✅ Each mentee shown as pie slice
- ✅ Slice size proportional to progress
- ✅ Color-coded (different colors per mentee)
- ✅ Hover tooltip shows mentee name + progress %
- ✅ Legend shows mentee names
- ✅ Title "📊 Mentee Progress Distribution"

### Mentor Dashboard - Progress Details
- ✅ Right panel shows all mentees
- ✅ Progress bar for each mentee
- ✅ Color indicators (🟢 100%, 🟠 50-75%, 🟡 25-50%, 🔴 0-25%, ⚫ 0%)
- ✅ "Plans Created" metric
- ✅ "Avg Progress" metric
- ✅ Accepted timestamp
- ✅ Each mentee in container with border

### Real-time Updates
- ✅ Pie chart updates when progress changes
- ✅ Progress bars update on refresh
- ✅ Metrics update correctly
- ✅ Colors change based on progress thresholds
- ✅ No page crashes during updates

### Data Integrity
- ✅ Progress values correct (match mentee actions)
- ✅ Plans created count accurate
- ✅ Timestamps recorded correctly
- ✅ Multiple mentees tracked independently
- ✅ Data persists between sessions

### Visual Design
- ✅ Pie chart colors distinct and visible
- ✅ Layout responsive (1-2 column layout)
- ✅ Text readable and well-formatted
- ✅ Icons used appropriately (📊, 🟢, 📧, etc.)
- ✅ Containers have proper spacing

---

## 🔍 Expected Results Summary

| Component | Single Mentee | Multiple Mentees |
|-----------|---------------|------------------|
| Pie Chart | 1 slice at progress % | N slices, proportional sizes |
| Colors | Single color | Different colors per mentee |
| Details Panel | 1 mentee entry | N mentee entries |
| Progress Bars | Shows progress | Shows each mentee's progress |
| Metrics | Plans/Progress accurate | Each mentee tracked |
| Updates | Real-time on refresh | All mentees update correctly |

---

## 🚀 Quick Test Run (5 minutes - minimal)

If you just want to quickly verify everything works:

1. **Start app:** `streamlit run app.py`

2. **Mentee:** jane_mentee / password
   - Complete 1 chatbot session (skip details, just fill fields)
   - Generate plan
   - Move progress slider to 50%
   - Click "Connect with Mentor" for John Smith
   - Logout

3. **Mentor:** john_mentor / password
   - Accept pending request from Jane
   - Scroll to "Active Mentee Connections"
   - ✅ Verify: Pie chart shows "Jane Doe 50%"
   - ✅ Verify: Progress details show 50% with 1 plan
   - ✅ Verify: Color is 🟡 or 🟠

4. **Result:** If pie chart displays and progress matches mentee action → ✅ WORKING

---

## 📝 Test Report Template

Use this to document your test results:

```
TEST REPORT: Mentor Dashboard Progress Visualization
Date: [Date]
Tester: [Name]

SCENARIO 1: Single Mentee
- Mentee created plan: ✅ / ❌
- Progress set to 50%: ✅ / ❌
- Mentor request sent: ✅ / ❌
- Mentor accepted request: ✅ / ❌
- Pie chart shows 1 slice: ✅ / ❌
- Progress bar shows 50%: ✅ / ❌
- Color indicator correct: ✅ / ❌

SCENARIO 2: Multiple Mentees
- Second plan created: ✅ / ❌
- Pie chart shows 2 slices: ✅ / ❌
- Colors distinct: ✅ / ❌
- Details panel shows both mentees: ✅ / ❌

SCENARIO 3: Edge Cases
- No connections message: ✅ / ❌
- Zero progress handled: ✅ / ❌
- CSV fallback works: ✅ / ❌

Overall Result: ✅ PASS / ❌ FAIL
Issues Found: [List any issues]
```

---

## 🐛 Troubleshooting

### Pie Chart Not Appearing
1. Check mentor has accepted at least one request
2. Refresh page
3. Check console for errors (F12 → Console)
4. Verify mentee has created a plan

### Progress Not Updating
1. Make sure you're updating progress as mentee, not mentor
2. Refresh mentor dashboard after mentee updates progress
3. Check database connection in console

### Colors Not Showing Correctly
1. Verify Plotly is installed: `pip install plotly`
2. Check progress percentages (0%, 50%, 100%, etc.)
3. Clear browser cache and refresh

### No Mentees Showing in Dashboard
1. Check requests were accepted (status = 'accepted')
2. Check mentee has created at least one plan
3. Verify mentor email matches in requests

---

## ✅ All Tests Passed Checklist

After completing all scenarios:

- ✅ Pie chart displays correctly
- ✅ Progress bars show accurate data
- ✅ Colors reflect progress levels
- ✅ Multiple mentees handled properly
- ✅ Real-time updates working
- ✅ Edge cases handled
- ✅ No errors or crashes
- ✅ Database persists data
- ✅ CSV fallback functional
- ✅ Visual design clean and professional

**Status:** Ready for Deployment ✅

