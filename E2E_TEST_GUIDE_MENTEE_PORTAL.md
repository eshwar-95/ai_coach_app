# Comprehensive E2E Test Guide - Mentee Portal

## Overview
This document provides step-by-step instructions to test the complete mentee portal functionality including:
1. Loading existing upskilling plans by name
2. Progress tracking with proper timestamps and visualization
3. Mentee recommendation system
4. Full E2E workflow from profile to recommendations

---

## Part 1: Database Integration Tests ✅

### Status: All 4 Tests Passed
- ✅ Load existing plans by name
- ✅ Progress tracking with timestamps
- ✅ CSV fallback
- ✅ Multiple plans per mentee

### To Run Tests
```bash
cd c:\workspace\ai_coach_app
python test_mentee_portal.py
```

---

## Part 2: Mentee Portal UI E2E Test

### Test Scenario 1: New Mentee (First Time)

**Prerequisites:**
- AI Coach app running: `streamlit run app.py`
- Demo mentee account ready: jane_mentee / password

**Steps:**

1. **Start App**
   ```bash
   cd c:\workspace\ai_coach_app
   streamlit run app.py
   ```
   - Opens at http://localhost:8501

2. **Login as Mentee**
   - Username: `jane_mentee`
   - Password: `password`
   - Click "Sign In"
   - Expected: Redirected to mentee chatbot interface

3. **Fill Profile Form (NEW IMPLEMENTATION)**
   - Step should now be "Step 1-4 of 5: Tell me about yourself"
   - **NEW**: All fields on ONE page (name, age, skills, interests)
   - Fill in:
     - Name: `Jane Smith` (different from username)
     - Age: `26`
     - Skills: `Python, SQL, AWS, Machine Learning`
     - Interests: `Data Science, AI/ML`
   - Click "✅ Confirm & Continue"
   - Expected: Single page transition, no intermediate steps

4. **Review Profile & Check for Existing Plans**
   - Step should be "Step 5 of 5: Review your profile"
   - **NEW**: Check for message: "📚 Found X previous upskilling plan(s) for Jane Smith!"
   - Since Jane Smith is new, this should NOT appear
   - Review profile:
     - Name: Jane Smith
     - Age: 26
     - Skills: Python, SQL, AWS, Machine Learning
     - Interests: Data Science, AI/ML
   - Click "✅ Get Recommendations"
   - Expected: Transition to recommendations step

5. **View AI-Generated Recommendations**
   - Should see "🎯 Your Personalized Recommendations"
   - **NEW Progress Chart**: "📈 Progress Over Time"
     - Should show a Plotly chart with:
       - X-axis: "Last Updated (Date & Time)"
       - Y-axis: "Progress (%)"
       - Single point at 0% (initial state)
       - Hover shows date/time and percentage
   - See job recommendations and mentor recommendations
   - Click "🤝 Connect with Mentor" for john_mentor
   - Expected: Success message "✅ Connection request sent to John Mentor!"

6. **Check Notifications (In Sidebar)**
   - Look at right sidebar
   - Should NOT see mentor notification yet (john_mentor hasn't responded)
   - Scroll down to view sidebar completely

---

### Test Scenario 2: Returning Mentee (Existing Plans)

**Prerequisites:**
- Previous test completed (Jane Smith has upskilling plan)
- App still running

**Steps:**

1. **Logout & Login Again**
   - Click "🚪 Logout"
   - Login as jane_mentee again

2. **Fill Profile Form with Same Name**
   - Name: `Jane Smith` (SAME as before)
   - Age: 27 (can change)
   - Skills: `Python, SQL, AWS, React` (can change)
   - Interests: `Data Science`
   - Click "✅ Confirm & Continue"

3. **Review Profile with Existing Plans (NEW FEATURE)**
   - Should now see: "📚 Found 1 previous upskilling plan(s) for Jane Smith!"
   - Expandable section showing:
     - Previous plan text
     - Progress: 0% (hasn't been updated yet)
     - Created date
   - **NEW Progress Chart** should show:
     - Single data point at 0%
   - Click "✅ Get Recommendations"

4. **New Recommendations Generated**
   - New upskilling plan created (separate from previous)
   - Progress chart now shows TWO plans if you go back
   - Can see progress over time comparing multiple plan generations

---

### Test Scenario 3: Progress Tracking & Updates

**Prerequisites:**
- Have existing upskilling plans for a mentee
- App running

**Steps:**

1. **Login and Navigate to Plans**
   - Login as jane_mentee
   - Should see "📂 Previous Upskilling Plans" section on profile step
   - Should list all previous plans

2. **Update Progress on a Plan**
   - In the plan expander, find the progress slider
   - Move slider from 0% to 50%
   - Add notes: "Completed Python basics course"
   - Click "💾 Save Update"
   - Expected: "✅ Progress updated to 50%"

3. **Verify Progress Chart Updates**
   - Look at the "📈 Progress Over Time" chart
   - **NEW**: Chart now shows:
     - X-axis: Updated timestamps
     - Y-axis: Progress values (0 to 100%)
     - Multiple data points if multiple updates
     - Hover shows exact date/time and %

---

### Test Scenario 4: Mentor Notifications

**Prerequisites:**
- Two browser tabs/windows or two machines
- Tab 1: Mentee (jane_mentee) with pending mentor request
- Tab 2: Mentor (john_mentor)

**Steps:**

1. **Tab 2 - Mentor Receives Request**
   - Login as john_mentor
   - See "📨 Pending Requests" section
   - Should see Jane Smith's request with:
     - Name: Jane Smith
     - Email: jane@mentee.com
     - Request date
     - ✅ Accept button
     - ❌ Reject button

2. **Tab 2 - Mentor Accepts Request**
   - Click "✅ Accept"
   - Expected: "✅ Accepted request from Jane Smith!"
   - **NEW**: Notification created for Jane

3. **Tab 1 - Mentee Receives Notification**
   - Check sidebar "🔔 Notifications"
   - Should see new notification:
     - ✅ John Mentor Accepted Your Request
     - Message: "Meet at Better Youth Office 📍"
     - Show as unread (highlighted)

4. **Tab 1 - Mark Notification as Read**
   - Click ✓ button next to notification
   - Notification should fade/mark as read
   - Unread count should decrease

---

### Test Scenario 5: Bulk Update Performance

**Expected Behavior:**
- Before: Name, age, skills, interests = 4 separate DB writes
- After: All fields = 1 DB write

**To Verify:**
1. Fill profile form with all fields
2. Click "✅ Confirm & Continue"
3. Should transition immediately to review step
4. Check database logs (if using Databricks SQL)
5. Should see only 1 INSERT operation, not 4

---

## Part 3: Integration Points to Verify

### ✅ 1. Profile Form Consolidation
- [ ] All 4 fields (name, age, skills, interests) on one page
- [ ] Single "Confirm & Continue" button
- [ ] Validation for all fields before save
- [ ] Session state updated once per form submission

### ✅ 2. Existing Plans Loading
- [ ] Mentee name used to query database
- [ ] Plans appear in review step if name matches
- [ ] No plans appear for new names
- [ ] Multiple plans displayed for same mentee name

### ✅ 3. Progress Chart with Proper Axes
- [ ] Plotly chart renders (no "No module named 'plotly'" error)
- [ ] X-axis labeled: "Last Updated (Date & Time)"
- [ ] Y-axis labeled: "Progress (%)"
- [ ] Y-axis range: 0 to 100%
- [ ] Tooltip shows: "Date: [date], Progress: [%]"
- [ ] Multiple data points show progression

### ✅ 4. Notifications System
- [ ] Accept button creates mentor_accepted notification
- [ ] Reject button creates mentor_rejected notification
- [ ] Message includes "Better Youth Office"
- [ ] Notification appears in sidebar
- [ ] Unread count updates
- [ ] Mark as read button works

### ✅ 5. Mentor Recommendations
- [ ] Mentor matching works based on skills/interests
- [ ] "Connect with Mentor" button creates request
- [ ] Request appears in mentor dashboard
- [ ] Request can be accepted/rejected

---

## Part 4: Database Verification

### Check Upskilling Plans Table

**SQL Query:**
```sql
SELECT id, email, mentee_name, created_at, plan, progress, notes, last_updated 
FROM upskilling_plans 
ORDER BY created_at DESC
LIMIT 10;
```

**Expected Columns:**
- [ ] id (UUID)
- [ ] email (mentee email)
- [ ] mentee_name (NEW - mentee full name)
- [ ] created_at (timestamp)
- [ ] plan (text)
- [ ] progress (0-100)
- [ ] notes (text)
- [ ] last_updated (timestamp)

### Check CSV Fallback

**Location:** `data/upskilling_plans.csv`

**Expected Format:**
```
id,email,mentee_name,created_at,plan,progress,notes,last_updated
uuid-1,jane@mentee.com,Jane Smith,2026-01-28 22:18:41,AI/ML Path...,0,,2026-01-28 22:18:41
```

---

## Part 5: Troubleshooting

### Issue: "No module named 'plotly'"
**Solution:**
```bash
pip install plotly
```

### Issue: Progress chart not showing
**Solution:**
1. Check that Plotly is installed
2. Verify mentee has previous plans
3. Check browser console for errors
4. Try refreshing page (Ctrl+F5)

### Issue: Existing plans not loading
**Solution:**
1. Verify mentee_name is stored in database
2. Check that names match exactly (case-sensitive)
3. Try logging in with different name to see new vs existing

### Issue: Notifications not appearing
**Solution:**
1. Check sidebar is visible (might be collapsed)
2. Verify you're logged in as mentee
3. Check that mentor actually accepted/rejected
4. Refresh page (Ctrl+F5)

### Issue: Profile form still shows step-by-step
**Solution:**
1. Clear browser cache (Ctrl+Shift+Delete)
2. Do hard refresh (Ctrl+Shift+R)
3. Verify app.py was properly updated (check for st.form)
4. Restart streamlit server

---

## Part 6: Expected Test Results

### All Tests Should Pass
```
🧪 AI Coach App - E2E Test Suite
======================================================================
✅ PASS: Load existing plans by name
✅ PASS: Progress tracking with timestamps
✅ PASS: CSV fallback
✅ PASS: Multiple plans per mentee
======================================================================
Total: 4/4 tests passed
```

### No Errors in App
- ✅ No "No module named" errors
- ✅ No SQL exceptions (unless intentionally fallback to CSV)
- ✅ No JavaScript errors in browser console
- ✅ All charts render properly

---

## Final Verification Checklist

- [ ] New mentee can fill profile and get recommendations
- [ ] Returning mentee sees existing plans by name
- [ ] Progress chart displays with proper axis labels
- [ ] Progress updates change timestamps
- [ ] Mentor accepts/rejects create notifications
- [ ] Notifications appear in sidebar
- [ ] Notifications can be marked as read
- [ ] Bulk form reduces database operations
- [ ] Mentor recommendations work
- [ ] All features work with both SQL and CSV fallback

---

## Ready to Deploy ✅

Once all tests pass, the mentee portal is production-ready with:
1. **Performance**: 75% fewer database writes on profile input
2. **Data Persistence**: Mentee names tracked for history
3. **Progress Tracking**: Proper timestamps and visualization
4. **Notifications**: Real-time alerts for mentor responses
5. **Recommendations**: Smart mentor matching and plan generation

