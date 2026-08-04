import os
import sys
import json
import streamlit as st
import plotly.graph_objects as go
from sqlalchemy.orm import Session

# Add the 'backend' directory to Python's sys.path
sys_backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "backend"))
if sys_backend_path not in sys.path:
    sys.path.insert(0, sys_backend_path)

# Universal import block resolving both package structures cleanly
try:
    from backend.app.database import init_db, SessionLocal
    from backend.app.seed_data import seed_sample_questions
    from backend.app import models, auth, sandbox, adaptive, ai_review
except ImportError:
    from app.database import init_db, SessionLocal
    from app.seed_data import seed_sample_questions
    from app import models, auth, sandbox, adaptive, ai_review

# Page Configuration
st.set_page_config(
    page_title="AdaptPrep AI — Adaptive DSA Practice & AI Code Review",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Dark Mode Aesthetics & Glassmorphic Cards
st.markdown("""
<style>
    .stApp {
        background-color: #090d16;
        color: #f1f5f9;
    }
    .main-card {
        background-color: #0f172a;
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #1e293b;
        margin-bottom: 20px;
    }
    .metric-card {
        background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%);
        border: 1px solid #3730a3;
        padding: 16px;
        border-radius: 12px;
        text-align: center;
    }
    .badge-easy { background-color: #064e3b; color: #34d399; padding: 4px 8px; border-radius: 6px; font-weight: bold; }
    .badge-medium { background-color: #78350f; color: #fbbf24; padding: 4px 8px; border-radius: 6px; font-weight: bold; }
    .badge-hard { background-color: #881337; color: #f43f5e; padding: 4px 8px; border-radius: 6px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Initialize Database on Startup
@st.cache_resource
def setup_database():
    init_db()
    db = SessionLocal()
    try:
        seed_sample_questions(db)
    finally:
        db.close()

setup_database()

# Session State Initialization
if "user" not in st.session_state:
    st.session_state.user = None
if "current_question_id" not in st.session_state:
    st.session_state.current_question_id = 1

def get_db_session():
    return SessionLocal()

# --- SIDEBAR AUTH & NAVIGATION ---
st.sidebar.title("⚡ AdaptPrep AI")
st.sidebar.caption("Adaptive DSA Platform for Placement Portfolio")

db = get_db_session()

# User Login / Signup in Sidebar
if not st.session_state.user:
    st.sidebar.subheader("🔑 Authentication")
    auth_mode = st.sidebar.radio("Choose Mode", ["Demo Login", "Login", "Signup"])

    if auth_mode == "Demo Login":
        if st.sidebar.button("🚀 Instant Placement Demo Login", use_container_width=True):
            user = db.query(models.User).filter(models.User.username == "democandidate").first()
            if not user:
                hashed_pwd = auth.get_password_hash("password123")
                user = models.User(username="democandidate", email="candidate@adaptprep.ai", hashed_password=hashed_pwd)
                db.add(user)
                db.commit()
                db.refresh(user)
                for t in ["arrays", "strings", "dp", "graphs", "trees"]:
                    db.add(models.TopicScore(user_id=user.id, topic=t, score=0.5))
                db.commit()
            st.session_state.user = {"id": user.id, "username": user.username, "email": user.email}
            st.rerun()

    elif auth_mode == "Login":
        username = st.sidebar.text_input("Username / Email")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Log In"):
            user = db.query(models.User).filter((models.User.username == username) | (models.User.email == username)).first()
            if user and auth.verify_password(password, user.hashed_password):
                st.session_state.user = {"id": user.id, "username": user.username, "email": user.email}
                st.rerun()
            else:
                st.sidebar.error("Invalid credentials")

    elif auth_mode == "Signup":
        new_user = st.sidebar.text_input("New Username")
        new_email = st.sidebar.text_input("Email")
        new_pwd = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Create Account"):
            if new_user and new_pwd:
                hashed_pwd = auth.get_password_hash(new_pwd)
                user = models.User(username=new_user, email=new_email, hashed_password=hashed_pwd)
                db.add(user)
                db.commit()
                db.refresh(user)
                for t in ["arrays", "strings", "dp", "graphs", "trees"]:
                    db.add(models.TopicScore(user_id=user.id, topic=t, score=0.5))
                db.commit()
                st.session_state.user = {"id": user.id, "username": user.username, "email": user.email}
                st.rerun()

else:
    st.sidebar.success(f"Logged in as: **{st.session_state.user['username']}**")
    if st.sidebar.button("Log Out"):
        st.session_state.user = None
        st.rerun()

    st.sidebar.markdown("---")
    
    # Adaptive Next Question Button
    if st.sidebar.button("✨ Adaptive Next Question", use_container_width=True):
        rec = adaptive.recommend_next_question(db, st.session_state.user["id"])
        if rec and rec["question"]:
            st.session_state.current_question_id = rec["question"].id
            st.session_state.page = "Practice"
            st.rerun()

# Navigation Selection
page = st.sidebar.radio("Navigation", ["Dashboard & Analytics", "Practice & Code Execution", "Question Bank"])

# --- PAGE 1: DASHBOARD & ANALYTICS ---
if page == "Dashboard & Analytics":
    st.title("📊 Candidate Performance & Skill Mastery")
    
    if not st.session_state.user:
        st.warning("Please log in or click 'Demo Login' in the sidebar to view your adaptive analytics.")
    else:
        user_id = st.session_state.user["id"]
        
        # Adaptive Recommendation Banner
        rec = adaptive.recommend_next_question(db, user_id)
        if rec and rec["question"]:
            st.markdown(f"""
            <div class="main-card">
                <h4 style="color: #a78bfa; margin: 0;">✨ Adaptive Recommendation</h4>
                <h3 style="color: #ffffff; margin: 5px 0;">{rec['question'].title} ({rec['recommended_difficulty'].capitalize()})</h3>
                <p style="color: #94a3b8; font-size: 14px;">{rec['reason']}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Solve Recommended Problem Now"):
                st.session_state.current_question_id = rec["question"].id
                st.session_state.page = "Practice & Code Execution"
                st.rerun()

        # Fetch Topic Scores
        scores = db.query(models.TopicScore).filter(models.TopicScore.user_id == user_id).all()
        score_dict = {s.topic: s.score for s in scores}
        
        # Stat Metric Cards
        col1, col2, col3, col4 = st.columns(4)
        avg_score = sum(score_dict.values()) / len(score_dict) if score_dict else 0.5
        total_subs = db.query(models.Submission).filter(models.Submission.user_id == user_id).count()
        passed_subs = db.query(models.Submission).filter(models.Submission.user_id == user_id, models.Submission.passed == True).count()
        
        with col1:
            st.metric("Overall Mastery", f"{round(avg_score * 100)}%")
        with col2:
            st.metric("Total Submissions", total_subs)
        with col3:
            st.metric("Passed Submissions", passed_subs)
        with col4:
            st.metric("Pass Rate", f"{round((passed_subs/total_subs*100) if total_subs else 0)}%")

        st.markdown("---")
        
        # Plotly Radar Chart for Topic Mastery
        st.subheader("🎯 Skill Band Radar Chart (EMA Scores)")
        categories = [t.capitalize() for t in score_dict.keys()]
        values = [round(s * 100) for s in score_dict.values()]

        fig = go.Figure(data=go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            marker=dict(color='#818cf8'),
            name='Topic Mastery %'
        ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100]),
                bgcolor='#0f172a'
            ),
            paper_bgcolor='#090d16',
            font=dict(color='#f8fafc'),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

# --- PAGE 2: PRACTICE & CODE EXECUTION ---
elif page == "Practice & Code Execution":
    st.title("💻 Code Submission & AI Review")
    
    # Question selector dropdown
    all_questions = db.query(models.Question).all()
    q_options = {q.id: f"#{q.id} {q.title} [{q.topic.capitalize()} - {q.difficulty.capitalize()}]" for q in all_questions}
    
    selected_id = st.selectbox(
        "Select Problem to Solve",
        options=list(q_options.keys()),
        format_func=lambda x: q_options[x],
        index=list(q_options.keys()).index(st.session_state.current_question_id) if st.session_state.current_question_id in q_options else 0
    )
    st.session_state.current_question_id = selected_id
    question = db.query(models.Question).filter(models.Question.id == selected_id).first()

    col_left, col_right = st.columns([1, 1])

    # Left Column: Problem Details
    with col_left:
        st.subheader(question.title)
        st.caption(f"Topic: **{question.topic.capitalize()}** | Difficulty: **{question.difficulty.capitalize()}**")
        st.markdown(question.description)
        
        st.markdown("### Sample Test Cases")
        tcs = json.loads(question.test_cases) if question.test_cases else []
        for i, tc in enumerate(tcs[:2], 1):
            st.code(f"Input: {tc['input']}\nExpected Output: {tc['expected']}", language="text")

    # Right Column: Editor & Submission
    with col_right:
        lang = st.radio("Select Language", ["Python", "C++"], horizontal=True)
        lang_key = "python" if lang == "Python" else "cpp"

        starter_dict = json.loads(question.starter_code) if question.starter_code else {}
        default_code = starter_dict.get(lang_key, "")

        code_input = st.text_area("Write Your Solution Code", value=default_code, height=350)

        if st.button("🚀 Submit & Run Tests", type="primary", use_container_width=True):
            if not st.session_state.user:
                st.error("Please log in to submit solutions.")
            else:
                with st.spinner("Executing solution in sandbox & analyzing with LangChain AI..."):
                    # 1. Run Execution Sandbox
                    exec_res = sandbox.execute_submission(lang_key, code_input, tcs)
                    
                    # 2. Update EMA Score
                    new_score = adaptive.update_user_topic_score(
                        db, st.session_state.user["id"], question.topic,
                        exec_res["passed_all"], exec_res["passed_count"], exec_res["total_tests"], exec_res["avg_runtime_ms"]
                    )
                    
                    # 3. LangChain AI Review
                    ai_res = ai_review.analyze_code_with_langchain(
                        question.title, question.description, lang_key, code_input,
                        exec_res["passed_all"], exec_res["passed_count"], exec_res["total_tests"], exec_res["avg_runtime_ms"]
                    )

                    # Display Execution Results
                    if exec_res["passed_all"]:
                        st.success(f"✅ All Test Cases Passed! ({exec_res['passed_count']}/{exec_res['total_tests']}) | Avg Runtime: {exec_res['avg_runtime_ms']} ms")
                    else:
                        st.error(f"❌ Submission Failed ({exec_res['passed_count']}/{exec_res['total_tests']} Passed)")

                    st.caption(f"Updated **{question.topic.capitalize()}** EMA Score: **{round(new_score * 100)}%**")

                    # Display AI Feedback Card
                    st.markdown("### 🤖 LangChain AI Code Review")
                    st.info(f"**Time Complexity**: `{ai_res['time_complexity']}` | **Space Complexity**: `{ai_res['space_complexity']}`")
                    
                    if ai_res.get("bugs"):
                        st.warning("**Bugs Detected**:\n" + "\n".join([f"- {b}" for b in ai_res["bugs"]]))
                    
                    if ai_res.get("optimization_tips"):
                        st.markdown("**Optimization Tips**:\n" + "\n".join([f"- {t}" for t in ai_res["optimization_tips"]]))
                    
                    if ai_res.get("corrected_snippet"):
                        st.markdown("**Suggested Code Fix**:")
                        st.code(ai_res["corrected_snippet"], language=lang_key)

# --- PAGE 3: QUESTION BANK ---
elif page == "Question Bank":
    st.title("📚 Question Bank")
    
    topic_filter = st.selectbox("Filter by Topic", ["All", "Arrays", "Strings", "DP", "Graphs", "Trees"])
    diff_filter = st.selectbox("Filter by Difficulty", ["All", "Easy", "Medium", "Hard"])

    query = db.query(models.Question)
    if topic_filter != "All":
        query = query.filter(models.Question.topic == topic_filter.lower())
    if diff_filter != "All":
        query = query.filter(models.Question.difficulty == diff_filter.lower())

    q_list = query.all()

    st.write(f"Showing **{len(q_list)}** questions")
    for q in q_list:
        with st.expander(f"#{q.id} {q.title} — ({q.topic.capitalize()} | {q.difficulty.capitalize()})"):
            st.write(q.description)
            if st.button(f"Solve #{q.id}", key=f"btn_{q.id}"):
                st.session_state.current_question_id = q.id
                st.session_state.page = "Practice & Code Execution"
                st.rerun()

db.close()
