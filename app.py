"""Main Streamlit application for SkillBridge - Career Coaching with Data Exploration."""
import streamlit as st
import pandas as pd
from src.auth import AuthenticationManager
from src.azure_client import AzureOpenAIClient
from src.databricks_llm_client import DatabricksLLMClient
from src.mock_llm_client import MockLLMClient
from src.databricks_client import DatabricksClient
from src.databricks_sql import DatabricksSQLClient
from src.utils import calculate_skill_match_percentage
from src.catalog_explorer_ui import (
    render_catalog_explorer,
    render_data_preview,
    render_charts,
)


def setup_page_config():
    """Setup Streamlit page configuration."""
    st.set_page_config(
        page_title="SkillBridge - Career Guidance",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="collapsed",
    )


def render_login_page():
    """Render login page."""
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.title("🧠 SkillBridge")
        st.markdown("**Your Personal Career Coaching Assistant**")
        st.divider()

        with st.form("login_form", border=False):
            st.write("### Sign In")

            email_or_username = st.text_input(
                "Email or Username",
                placeholder="john_mentor or jane_mentee",
            )

            password = st.text_input("Password", type="password", placeholder="password")

            submit_button = st.form_submit_button("Sign In", use_container_width=True)

            if submit_button:
                if not email_or_username or not password:
                    st.error("Please enter both email/username and password.")
                else:
                    if AuthenticationManager.login(email_or_username, password):
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials. Please try again.")
        
        st.divider()
        st.markdown("""
        **Demo Credentials:**
        - Username: `jane_mentee` | Password: `password`
        - Username: `john_mentor` | Password: `password`
        """)


def initialize_session_state():
    """Initialize session state variables."""
    AuthenticationManager.initialize_session()
    
    if "mentee_profile" not in st.session_state:
        st.session_state.mentee_profile = {
            "name": None,
            "age": None,
            "skills": [],
            "interests": None,
        }
    
    if "chat_step" not in st.session_state:
        st.session_state.chat_step = 0  # 0=name, 1=age, 2=skills, 3=interests, 4=confirmation, 5=results
    
    if "recommendations" not in st.session_state:
        st.session_state.recommendations = None
    
    if "existing_plans" not in st.session_state:
        st.session_state.existing_plans = []

def render_mentor_dashboard():
    """Render mentor dashboard."""
    user = st.session_state.user
    
    st.title(f"👋 Welcome, {user['name']}")
    st.markdown("### Mentor Dashboard")
    
    # Try to initialize Databricks SQL client for mentor requests
    sql_client = None
    try:
        sql_client = DatabricksSQLClient()
    except Exception:
        sql_client = None
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 Your Profile")
        st.write(f"**Name:** {user['name']}")
        st.write(f"**Email:** {user['email']}")
        st.write(f"**Role:** Mentor")
    
    with col2:
        st.subheader("📈 Statistics")
        if sql_client:
            all_requests = sql_client.get_mentor_requests(user['email'])
            pending = [r for r in all_requests if r.get('status') == 'pending']
            accepted = [r for r in all_requests if r.get('status') == 'accepted']
            
            st.metric("Pending Requests", len(pending))
            st.metric("Accepted", len(accepted))
        else:
            st.metric("Pending Requests", "N/A")
            st.metric("Accepted", "N/A")
    
    st.divider()
    
    # Show pending mentee requests
    st.subheader("🔔 Pending Mentee Requests")
    
    if sql_client:
        try:
            requests = sql_client.get_mentor_requests(user['email'], status='pending')
            
            if not requests:
                st.info("No pending requests at this time.")
            else:
                for req in requests:
                    with st.container(border=True):
                        col1, col2, col3 = st.columns([3, 1, 1])
                        
                        with col1:
                            st.markdown(f"### 👤 {req.get('mentee_name', 'Unknown')}")
                            st.write(f"📧 Email: `{req.get('mentee_email')}`")
                            created_at = req.get('created_at', 'N/A')
                            st.write(f"📅 Requested: {created_at}")
                        
                        with col2:
                            if st.button("✅ Accept", key=f"accept_{req.get('id')}", use_container_width=True):
                                sql_client.update_mentor_request(
                                    req.get('id'),
                                    'accepted',
                                    f"Accepted connection request from {req.get('mentee_name')}"
                                )
                                # Create notifications for both mentor and mentee
                                sql_client.create_notification(
                                    recipient_email=req.get('mentee_email'),
                                    recipient_name=req.get('mentee_name'),
                                    notification_type='mentor_accepted',
                                    title=f"✅ {user['name']} Accepted Your Request",
                                    message=f"Great news! {user['name']} has accepted your mentorship request. Please meet them at Better Youth Office. 📍",
                                    related_id=req.get('id')
                                )
                                st.success(f"✅ Accepted request from {req.get('mentee_name')}!")
                                st.rerun()
                        
                        with col3:
                            if st.button("❌ Reject", key=f"reject_{req.get('id')}", use_container_width=True):
                                sql_client.update_mentor_request(
                                    req.get('id'),
                                    'rejected',
                                    f"Declined connection request from {req.get('mentee_name')}"
                                )
                                # Create notification for mentee about rejection
                                sql_client.create_notification(
                                    recipient_email=req.get('mentee_email'),
                                    recipient_name=req.get('mentee_name'),
                                    notification_type='mentor_rejected',
                                    title=f"❌ {user['name']} Declined Your Request",
                                    message=f"{user['name']} has declined your mentorship request. Don't worry - keep exploring other opportunities!",
                                    related_id=req.get('id')
                                )
                                st.info(f"Request from {req.get('mentee_name')} declined.")
                                st.rerun()
        except Exception as e:
            st.error(f"Error loading requests: {str(e)}")
    else:
        st.warning("⚠️ Could not connect to database. Requests may be stored locally.")
    
    st.divider()
    
    # Show accepted connections with progress pie chart
    st.subheader("✅ Active Mentee Connections & Progress")
    
    if sql_client:
        try:
            accepted = sql_client.get_mentor_requests(user['email'], status='accepted')
            
            if not accepted:
                st.info("No active connections yet. Accept a pending request to get started!")
            else:
                # Get mentee progress data
                mentee_progress = []
                total_progress = 0
                
                for req in accepted:
                    mentee_email = req.get('mentee_email')
                    mentee_name = req.get('mentee_name', 'Unknown')
                    
                    # Get mentee's upskilling plans to calculate progress
                    try:
                        plans = sql_client.get_plans_by_email(mentee_email)
                        if plans:
                            # Calculate average progress across all mentee's plans
                            avg_progress = sum([int(p.get('progress', 0)) for p in plans]) / len(plans)
                            total_progress += avg_progress
                            mentee_progress.append({
                                'name': mentee_name,
                                'email': mentee_email,
                                'progress': int(avg_progress),
                                'accepted_at': req.get('responded_at', 'N/A'),
                                'num_plans': len(plans)
                            })
                    except Exception:
                        # If no plans yet, show 0% progress
                        mentee_progress.append({
                            'name': mentee_name,
                            'email': mentee_email,
                            'progress': 0,
                            'accepted_at': req.get('responded_at', 'N/A'),
                            'num_plans': 0
                        })
                
                if mentee_progress:
                    # Create pie chart columns
                    col1, col2 = st.columns([1.2, 1.8])
                    
                    with col1:
                        # Pie chart showing progress distribution
                        progress_values = [mp['progress'] for mp in mentee_progress]
                        mentee_names = [mp['name'] for mp in mentee_progress]
                        
                        # Create pie chart data
                        import plotly.graph_objects as go
                        
                        fig = go.Figure(data=[go.Pie(
                            labels=mentee_names,
                            values=progress_values,
                            marker=dict(
                                colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8'][:len(mentee_names)]
                            ),
                            hovertemplate='<b>%{label}</b><br>Progress: %{value}%<extra></extra>',
                            textposition='auto',
                            textinfo='label+percent'
                        )])
                        
                        fig.update_layout(
                            title="📊 Mentee Progress Distribution",
                            height=400,
                            showlegend=True,
                            margin=dict(l=0, r=0, t=40, b=0)
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        st.markdown("### 📈 Mentee Progress Details")
                        
                        for mp in mentee_progress:
                            progress_pct = mp['progress']
                            
                            # Color coding based on progress
                            if progress_pct >= 100:
                                icon = "🟢"
                                color = "green"
                            elif progress_pct >= 75:
                                icon = "🟠"
                                color = "orange"
                            elif progress_pct >= 50:
                                icon = "🟡"
                                color = "gold"
                            elif progress_pct > 0:
                                icon = "🔴"
                                color = "red"
                            else:
                                icon = "⚫"
                                color = "gray"
                            
                            with st.container(border=True):
                                st.markdown(f"{icon} **{mp['name']}**")
                                st.write(f"📧 `{mp['email']}`")
                                st.progress(progress_pct / 100, text=f"Progress: {progress_pct}%")
                                
                                col_a, col_b = st.columns(2)
                                with col_a:
                                    st.metric("Plans Created", mp['num_plans'])
                                with col_b:
                                    st.metric("Avg Progress", f"{progress_pct}%")
                                
                                st.caption(f"Accepted: {mp['accepted_at']}")
                else:
                    st.info("Loading mentee progress data...")
                    
        except Exception as e:
            st.error(f"Error loading connections: {str(e)}")
    else:
        st.info("Active connections will appear here once you accept a request.")
    
    st.divider()
    
    # Add Catalog Explorer Tab
    st.subheader("📊 Data Insights & Catalog Explorer")
    
    with st.expander("🔍 Explore Databricks Catalog", expanded=False):
        try:
            catalog, schema, table, df = render_catalog_explorer("main")
            
            if catalog and schema and table and df is not None:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("📁 Catalog", catalog)
                with col2:
                    st.metric("📋 Schema", schema)
                with col3:
                    st.metric("📊 Table", table)
                
                st.divider()
                
                tab1, tab2 = st.tabs(["📋 Data Preview", "📈 Visualization"])
                
                with tab1:
                    st.write(f"**Rows:** {len(df)} | **Columns:** {len(df.columns)}")
                    st.dataframe(df, use_container_width=True)
                
                with tab2:
                    render_charts(df, "mentor_explorer")
            else:
                st.info("Select a catalog, schema, and table from the sidebar to explore data")
        except Exception as e:
            st.warning(f"Catalog exploration not available: {e}")


def get_job_recommendations(mentee_profile: dict, jobs_df: pd.DataFrame) -> pd.DataFrame:
    """Get job recommendations based on mentee skills."""
    if jobs_df.empty or not mentee_profile["skills"]:
        return pd.DataFrame()
    
    jobs_df = jobs_df.copy()
    jobs_df["skill_match"] = jobs_df["required_skills"].apply(
        lambda x: calculate_skill_match_percentage(mentee_profile["skills"], x)
    )
    
    # Filter jobs with at least some skill match, sort by match percentage
    recommended = jobs_df[jobs_df["skill_match"] > 0].sort_values("skill_match", ascending=False)
    return recommended.head(5)


def get_mentor_recommendations(mentee_profile: dict, mentors_df: pd.DataFrame) -> pd.DataFrame:
    """Get mentor recommendations based on mentee interests."""
    if mentors_df.empty or not mentee_profile["interests"]:
        return pd.DataFrame()
    
    mentors_df = mentors_df.copy()
    interests_lower = mentee_profile["interests"].lower()
    
    # Simple matching: check if mentor expertise contains mentee interests
    def expertise_match(expertise):
        if pd.isna(expertise):
            return 0
        return len([skill for skill in interests_lower.split(",") 
                   if skill.strip().lower() in str(expertise).lower()])
    
    mentors_df["match_score"] = mentors_df["expertise"].apply(expertise_match)
    recommended = mentors_df[mentors_df["match_score"] > 0].sort_values("match_score", ascending=False)
    return recommended.head(3)


def render_mentee_chatbot():
    """Render mentee chatbot interface."""
    user = st.session_state.user
    profile = st.session_state.mentee_profile
    step = st.session_state.chat_step
    
    # Try to initialize Databricks SQL client for persistence (optional)
    sql_client = None
    try:
        sql_client = DatabricksSQLClient()
    except Exception:
        sql_client = None
    
    st.title(f"👋 Welcome, {user['name']}")
    st.markdown("### SkillBridge Career Guidance")
    
    # Progress indicator
    progress = min((step + 1) / 6, 1.0)
    st.progress(progress)
    
    # Chatbot interface
    st.markdown("---")

    # NOTE: Previous plans are NOT shown on initial login
    # They will only be queried and displayed after mentee enters their full name in the profile form
    # This improves UX and prevents showing unrelated plans
    
    # Initialize step-based chatbot flow
    st.markdown("---")
    
    if step == 0:
        # Check if we need to show form or review
        show_form = not profile["name"]
        
        if show_form:
            st.write("**Step 1-4 of 5: Tell me about yourself** (All at once!)")
            st.info("Fill in all the information below and click 'Confirm & Continue' to save - just one database write!")
            
            # Create form for input
            form_col = st.container(border=True)
            with form_col:
                st.write("### Your Profile Information")
                
                # Name input
                name = st.text_input(
                    "What's your full name?",
                    value=profile["name"] or "",
                    placeholder="e.g., John Doe",
                    key="form_name"
                )
                
                # Age input
                age = st.number_input(
                    "How old are you?",
                    min_value=18,
                    max_value=100,
                    value=profile["age"] or 25,
                    key="form_age"
                )
                
                # Skills input
                st.write("**Your skills** (comma-separated)")
                skills_input = st.text_area(
                    "List your technical and professional skills",
                    value=", ".join(profile["skills"]) if profile["skills"] else "",
                    height=80,
                    placeholder="Python, JavaScript, SQL, AWS, Machine Learning...",
                    key="form_skills",
                    help="Enter multiple skills separated by commas"
                )
                
                # Interests input
                interests = st.text_input(
                    "What are your career interests or target roles?",
                    value=profile["interests"] or "",
                    placeholder="Data Science, Web Development, Cloud Architecture...",
                    key="form_interests",
                    help="e.g., Data Science, Product Management, DevOps"
                )
                
                # Submit button
                col1, col2 = st.columns([1, 1])
                with col1:
                    submit_button = st.button("✅ Confirm & Continue", use_container_width=True, key="submit_form")
                
                with col2:
                    pass  # placeholder for alignment
                
                if submit_button:
                    # Validate all inputs
                    errors = []
                    if not name.strip():
                        errors.append("Please enter your name")
                    if not skills_input.strip():
                        errors.append("Please enter at least one skill")
                    if not interests.strip():
                        errors.append("Please enter your career interests")
                    
                    if errors:
                        st.error("\n".join(f"❌ {e}" for e in errors))
                    else:
                        # Bulk update all at once (single action) - NO RERUN
                        skills = [s.strip() for s in skills_input.split(",")]
                        st.session_state.mentee_profile["name"] = name.strip()
                        st.session_state.mentee_profile["age"] = age
                        st.session_state.mentee_profile["skills"] = skills
                        st.session_state.mentee_profile["interests"] = interests.strip()
                        
                        # Check if this mentee already has upskilling plans
                        existing_plans = []
                        if sql_client:
                            try:
                                existing_plans = sql_client.get_plans_by_name(name.strip())
                            except Exception:
                                pass
                        
                        # Store existing plans in session state
                        st.session_state.existing_plans = existing_plans
                        st.session_state.profile_confirmed = True
                        st.success("✅ Profile saved! Scroll down to see your review...")
        
        # Show review if profile has been confirmed (no rerun needed!)
        if st.session_state.get("profile_confirmed") or profile["name"]:
            st.divider()
            st.write("**Step 5 of 5: Review your profile**")
            st.info("Your profile has been saved successfully!")
            
            # Show existing plans if any
            existing_plans = st.session_state.get("existing_plans", [])
            if existing_plans:
                st.info(f"📚 Found {len(existing_plans)} previous upskilling plan(s) for {profile['name']}!")
                for idx, plan in enumerate(existing_plans):
                    with st.expander(f"📋 Plan {idx + 1} - {plan.get('created_at', 'Unknown date')}", expanded=idx == 0):
                        col_plan, col_progress = st.columns([3, 1])
                        with col_plan:
                            st.markdown("**Upskilling Plan:**")
                            st.write(plan.get('plan', 'No plan text'))
                        with col_progress:
                            st.metric("Current Progress", f"{plan.get('progress', 0)}%")
                        
                        if plan.get('notes'):
                            st.markdown("**Notes:**")
                            st.write(plan.get('notes'))
            
            st.divider()
            st.markdown(f"""
            ### 👤 Your Profile Summary
            
            **Name:** {profile["name"]}
            **Age:** {profile["age"]} years old
            **Skills:** {", ".join(profile["skills"]) if profile["skills"] else "Not specified"}
            **Career Interests:** {profile["interests"] if profile["interests"] else "Not specified"}
            """)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("👈 Edit Profile", key="btn_back", use_container_width=True):
                    st.session_state.profile_confirmed = False
                    st.session_state.mentee_profile = {
                        "name": None,
                        "age": None,
                        "skills": [],
                        "interests": None,
                    }
                    st.rerun()
            
            with col2:
                if st.button("✅ Get Recommendations", key="btn_submit", use_container_width=True):
                    st.session_state.chat_step = 5
                    st.rerun()
    
    elif step == 5:
        st.write("### 🎯 Your Personalized Recommendations")
        
        # Debug: Show which profile is loaded
        with st.expander("🔍 Debug: Profile Data"):
            st.json(profile)
        
        try:
            # Load data
            db_client = DatabricksClient()
            jobs_df = db_client.get_job_openings_data()
            mentors_df = db_client.get_mentors_data()
            
            # Get recommendations
            job_recs = get_job_recommendations(profile, jobs_df)
            mentor_recs = get_mentor_recommendations(profile, mentors_df)
            
            # Display recommendations
            if not job_recs.empty:
                st.subheader("💼 Matching Job Opportunities")
                st.markdown(f"*Jobs matching {profile['name']}'s skills:*")
                for idx, job in job_recs.iterrows():
                    match_pct = int(job.get("skill_match", 0))
                    
                    # Color code based on match percentage
                    if match_pct >= 80:
                        match_icon = "🟢"
                    elif match_pct >= 60:
                        match_icon = "🟡"
                    else:
                        match_icon = "🔴"
                    
                    with st.container(border=True):
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown(f"### {match_icon} {job['title']}")
                            st.markdown(f"🏢 **{job['company']}** | 📍 {job['location']}")
                            st.write(f"_{job['description'][:100]}..._")
                        with col2:
                            st.metric("Skill Match", f"{match_pct}%")
                        
                        col_sal, col_link = st.columns([1, 1])
                        with col_sal:
                            st.write(f"💰 **{job['salary']}**")
                        with col_link:
                            if pd.notna(job['job_url']):
                                st.markdown(f"[🔗 View Job]({job['job_url']})")
            else:
                st.info("💡 No jobs with direct skill matches found. See upskilling recommendations below to improve your skills!")
            
            # Upskilling recommendations via AI
            st.subheader("📚 Upskilling Recommendations")
            
            upskill_prompt = f"""Based on this mentee's profile:
- Name: {profile['name']}
- Current Skills: {', '.join(profile['skills'])}
- Career Interests: {profile['interests']}
- Age: {profile['age']}

Provide a concise upskilling plan (max 200 words) with:
1. Top 3 skills to learn next
2. Recommended learning path (short-term, medium-term, long-term)
3. Estimated time commitment

Keep it practical and actionable."""
            
            system_prompt = "You are a career coach. Provide practical, personalized career advice."
            
            with st.spinner("Generating upskilling plan..."):
                response = None
                error_messages = []
                llm_service = None
                
                st.info("🔄 Attempting to generate with: Databricks LLM → Azure OpenAI → Mock LLM")
                
                # Try Databricks LLM first
                try:
                    st.write("📍 Trying Databricks LLM...")
                    llm_client = DatabricksLLMClient()
                    response = llm_client.get_response(system_prompt, upskill_prompt)
                    llm_service = "Databricks LLM"
                    st.success("✅ Databricks LLM succeeded")
                except Exception as db_error:
                    st.warning(f"❌ Databricks LLM failed: {str(db_error)}")
                    error_messages.append(f"Databricks: {str(db_error)}")
                    
                    # Fallback to Azure OpenAI
                    if not response:
                        try:
                            st.write("📍 Trying Azure OpenAI...")
                            azure_client = AzureOpenAIClient()
                            response = azure_client.get_response(system_prompt, upskill_prompt)
                            llm_service = "Azure OpenAI"
                            st.success("✅ Azure OpenAI succeeded")
                        except Exception as azure_error:
                            st.warning(f"❌ Azure OpenAI failed: {str(azure_error)}")
                            error_messages.append(f"Azure: {str(azure_error)}")
                            
                            # Fallback to Mock LLM for demo purposes
                            if not response:
                                try:
                                    st.write("📍 Trying Mock LLM...")
                                    mock_client = MockLLMClient()
                                    response = mock_client.get_response(system_prompt, upskill_prompt)
                                    llm_service = "Mock LLM (Demo Mode)"
                                    st.success("✅ Mock LLM succeeded")
                                except Exception as mock_error:
                                    st.warning(f"❌ Mock LLM failed: {str(mock_error)}")
                                    error_messages.append(f"Mock: {str(mock_error)}")
                
                if response:
                    if llm_service != "Mock LLM (Demo Mode)":
                        st.success(f"✅ Generated with {llm_service}")
                    else:
                        st.info(f"ℹ️ Generated with {llm_service} - Configure real credentials for production")
                    
                    # Display plan in a nice container
                    with st.container(border=True):
                        st.markdown(f"### 📚 Upskilling Plan for {profile['name']} (Mentee)")
                        st.write(response)
                    
                    # Persist upskilling plan to Databricks SQL if available
                    if sql_client is not None:
                        try:
                            sql_client.ensure_table_exists()
                            record_id = sql_client.insert_plan(user.get("email"), response, mentee_name=profile.get("name", ""), progress=0, notes="")
                            st.success(f"✅ Plan saved to Databricks SQL for {profile['name']}")
                        except Exception as e:
                            st.warning(f"Could not save plan to Databricks: {e}")
                else:
                    st.error("Could not generate AI recommendations")
                    st.info("**Configuration needed for production:**")
                    st.code("""
# Option 1: Add Databricks credentials to .env
DATABRICKS_TOKEN=dapi...
DATABRICKS_LLM_ENDPOINT=https://...

# Option 2: Add Azure credentials to .env
AZURE_ENDPOINT=https://...
AZURE_API_KEY=...

Note: Demo mode is currently active with mock responses.
""", language="env")
                    
                    # Show debug info in expander
                    with st.expander("Debug Info"):
                        for msg in error_messages:
                            st.write(f"- {msg}")
            
            # Mentor recommendations
            if not mentor_recs.empty:
                st.subheader("👨‍🏫 Recommended Mentors")
                st.markdown(f"*Based on {profile['name']}'s interests and skills, here are mentors who can guide you:*")
                
                for idx, mentor in mentor_recs.iterrows():
                    with st.container(border=True):
                        col1, col2, col3 = st.columns([2, 1, 1])
                        
                        with col1:
                            st.markdown(f"### 👤 {mentor['name']} (Mentor)")
                            st.markdown(f"🎯 **Expertise:** {mentor['expertise']}")
                            st.write(f"{mentor['bio'][:100]}...")
                        
                        with col2:
                            st.metric("Experience", f"{mentor['experience_years']} years")
                        
                        with col3:
                            st.metric("Match Score", f"{mentor.get('match_score', 0)}")
                        
                        if st.button("🤝 Connect with Mentor", key=f"mentor_{idx}", use_container_width=True):
                            try:
                                if sql_client is not None:
                                    request_id = sql_client.create_mentor_request(
                                        mentee_email=user.get("email"),
                                        mentee_name=profile.get("name", "Unknown"),
                                        mentor_email=mentor.get("email"),
                                        mentor_name=mentor.get("name")
                                    )
                                    st.success(f"✅ Connection request sent to {mentor['name']}!")
                                    st.balloons()
                                else:
                                    st.warning("Could not send request - database unavailable. Please try again.")
                            except Exception as e:
                                st.error(f"Error sending request: {str(e)}")
            else:
                st.info("💡 No mentors found matching your interests yet. Try adding more skills or interests!")
            
            # Reset button
            st.divider()
            if st.button("🔄 Start Over", key="btn_reset"):
                st.session_state.chat_step = 0
                st.session_state.mentee_profile = {
                    "name": None,
                    "age": None,
                    "skills": [],
                    "interests": None,
                }
                st.rerun()
        
        except Exception as e:
            st.error(f"Error loading recommendations: {str(e)}")
    
    # Add Catalog Explorer for Mentee
    st.divider()
    st.subheader("📊 Explore Job Market Data & Insights")
    
    with st.expander("🔍 Databricks Catalog Explorer", expanded=False):
        st.write("Browse and visualize job market data, skills trending, and mentor information from the Databricks catalog.")
        try:
            catalog, schema, table, df = render_catalog_explorer("main")
            
            if catalog and schema and table and df is not None:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("📁 Catalog", catalog)
                with col2:
                    st.metric("📋 Schema", schema)
                with col3:
                    st.metric("📊 Table", table)
                
                st.divider()
                
                tab1, tab2 = st.tabs(["📋 Data Preview", "📈 Visualization"])
                
                with tab1:
                    st.write(f"**Rows:** {len(df)} | **Columns:** {len(df.columns)}")
                    st.dataframe(df, use_container_width=True)
                
                with tab2:
                    render_charts(df, "mentee_explorer")
            else:
                st.info("Select a catalog, schema, and table from the sidebar to explore market data")
        except Exception as e:
            st.warning(f"Catalog exploration not available: {e}")


def render_notifications_ui():
    """Render notifications UI in sidebar."""
    if not AuthenticationManager.is_authenticated():
        return
    
    user = st.session_state.user
    
    try:
        sql_client = DatabricksSQLClient()
        notifications = sql_client.get_notifications(user.get("email"), unread_only=False)
        
        with st.sidebar:
            st.divider()
            st.markdown("### 🔔 Notifications")
            
            if not notifications:
                st.caption("No notifications yet")
            else:
                # Show unread count
                unread_count = sum(1 for n in notifications if not n.get('is_read'))
                if unread_count > 0:
                    st.markdown(f"**Unread: {unread_count}**")
                
                # Display notifications
                for notif in notifications[:5]:  # Show latest 5
                    is_read = notif.get('is_read', False)
                    notif_id = notif.get('id')
                    title = notif.get('title', 'Notification')
                    message = notif.get('message', '')
                    created_at = notif.get('created_at', 'Just now')
                    
                    # Format notification display
                    bg_color = "" if is_read else "background: rgba(59, 130, 246, 0.1);"
                    
                    with st.container(border=True):
                        col1, col2 = st.columns([4, 1])
                        
                        with col1:
                            st.markdown(f"**{title}**")
                            st.caption(message[:80] + ("..." if len(message) > 80 else ""))
                            st.caption(f"_{created_at}_")
                        
                        with col2:
                            if not is_read:
                                if st.button("✓", key=f"mark_read_{notif_id}", help="Mark as read"):
                                    sql_client.mark_notification_read(notif_id)
                                    st.rerun()
                
                if len(notifications) > 5:
                    st.caption(f"... and {len(notifications) - 5} more notifications")
    
    except Exception:
        # Silently fail if notifications not available
        pass


def render_logout_button():
    """Render logout button in sidebar."""
    with st.sidebar:
        if st.session_state.get("authenticated", False):
            st.divider()
            if st.button("🚪 Logout", use_container_width=True):
                AuthenticationManager.logout()
                st.rerun()


def main():
    """Main application entry point."""
    setup_page_config()
    initialize_session_state()
    
    # Check authentication
    if not AuthenticationManager.is_authenticated():
        render_login_page()
    else:
        # Authenticated user
        user = AuthenticationManager.get_current_user()
        
        if AuthenticationManager.is_mentor():
            render_mentor_dashboard()
        else:  # Mentee
            render_mentee_chatbot()
        
        render_notifications_ui()
        render_logout_button()


if __name__ == "__main__":
    main()
