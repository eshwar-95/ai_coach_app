# Quick Test Guide - New Features

## 🔔 Testing Notifications System

### Prerequisites
- Ensure both mentee and mentor accounts exist
- Demo accounts: `jane_mentee` (password) and `john_mentor` (password)

### Test Flow

#### Step 1: Send Mentor Request (Mentee)
1. Login as: `jane_mentee` / `password`
2. Navigate to "Recommended Mentors" section (bottom of chat)
3. Click "🤝 Connect with Mentor" on john_mentor's card
4. Confirm: Should see "✅ Connection request sent to John Mentor!"

#### Step 2: Accept/Reject Request (Mentor)
1. Login as: `john_mentor` / `password`
2. See "📨 Pending Requests" section in mentor dashboard
3. Click either:
   - ✅ Accept → Creates "mentor_accepted" notification
   - ❌ Reject → Creates "mentor_rejected" notification

#### Step 3: Receive Notification (Mentee)
1. Login back as: `jane_mentee` / `password`
2. Look at **sidebar on the right**
3. Check "🔔 Notifications" section
4. Should see notification:
   - ✅ If accepted: "✅ John Mentor Accepted Your Request" + "Meet at Better Youth Office"
   - ❌ If rejected: "❌ John Mentor Declined Your Request"

#### Step 4: Mark as Read
1. In the notification, click the ✓ button
2. Notification should fade/mark as read
3. Unread count should decrease

---

## ⚡ Testing Performance Optimization

### Before vs After Comparison

#### Profile Input Speed
1. Login as: `jane_mentee` / `password`
2. If first time, start at Step 1 (profile input)
3. **NEW**: All fields (name, age, skills, interests) are on **ONE PAGE**
4. Fill in all fields:
   - Name: "Jane Test"
   - Age: 28
   - Skills: "Python, SQL, AWS"
   - Interests: "Data Science"
5. Click **"✅ Confirm & Continue"**
6. Should transition directly to review page (no intermediate steps)

**Expected Performance:**
- No step-by-step transitions
- Single database write (not 4)
- Noticeably faster page transitions

---

## 📊 Testing Plotly Pie Chart

### Pie Chart Display
1. Login as: `john_mentor` / `password`
2. Scroll to "👥 Your Mentees" section
3. **Verify pie chart displays** showing mentee progress distribution
4. Should show:
   - ✅ No "No module named 'plotly'" error
   - ✅ Colored pie chart with percentages
   - ✅ Legend showing mentee names
   - ✅ Hover shows exact percentages
5. Below chart should see "📈 Mentee Progress Details" with:
   - Color-coded progress bars
   - Progress percentages
   - Accept dates

---

## 🗂️ Database Verification

### Check Notifications Stored
1. Check `data/notifications.csv` if SQL fails:
   ```
   id,recipient_email,recipient_name,type,title,message,related_id,created_at,read_at,is_read
   ```

2. If using Databricks SQL, verify `notifications` table created:
   ```sql
   SELECT * FROM notifications LIMIT 10
   ```

### Check Profile Updates (Bulk Save)
1. Check `data/upskilling_plans.csv` or SQL
2. Should see mentee profile with all fields in one entry
3. Timestamps should show single write (not 4 separate writes)

---

## ✅ Checklist for Full Testing

- [ ] Notifications created when mentor accepts request
- [ ] Notifications created when mentor rejects request
- [ ] Mentee can see notifications in sidebar
- [ ] Mentee can mark notifications as read
- [ ] Unread count updates in real-time
- [ ] Profile input is consolidated on one page
- [ ] "Confirm & Continue" button works without errors
- [ ] Pie chart displays without module errors
- [ ] Mentee progress shows with color coding
- [ ] All features work with both SQL and CSV fallback

---

## 🐛 Troubleshooting

### Issue: Notifications not appearing
**Solution:**
1. Check sidebar (might be collapsed)
2. Ensure user is logged in with email matching recipient_email
3. Check `data/notifications.csv` exists and has data
4. Try refreshing browser (Ctrl+F5)

### Issue: Pie chart still shows error
**Solution:**
1. Verify Plotly installed: `pip show plotly`
2. If not installed: `pip install plotly`
3. Restart Streamlit app: `streamlit run app.py`

### Issue: Profile input shows old step-by-step flow
**Solution:**
1. Clear browser cache
2. Press Ctrl+Shift+R to hard refresh
3. Check that app.py was properly updated (search for "profile_form")

### Issue: Bulk update doesn't save
**Solution:**
1. Check that SQL connection is working (mentee requests should work too)
2. Check `data/mentee_profiles.csv` if SQL fails
3. Ensure email is valid and non-empty

---

## 📞 Support Info

For issues with:
- **Plotly**: Check requirements.txt includes "plotly"
- **Notifications**: Check DatabricksSQLClient methods exist
- **Performance**: Verify form uses st.form() not individual buttons
- **General**: Check CHANGES_SUMMARY.md for detailed documentation

