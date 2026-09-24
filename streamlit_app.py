import streamlit as st
import time
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta

# --- Page Configuration ---
st.set_page_config(
    page_title="EduDash - Professional Learning Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

from utils.styling import local_css
from views.home import render_home
from views.profile import render_profile
from views.learning import render_learning_dashboard, render_skill_assessment, render_personalized_learning_path, render_learning_modules, render_practice_quiz
from views.ai_tools import render_ai_tutor, render_writing_evaluation, render_ai_recommendations
from views.analytics import render_progress_analytics, render_certificates
from views.admin import render_teacher_dashboard, render_admin_dashboard
from views.settings import render_notifications, render_settings, render_logout
from views.login import render_login

local_css()
# --- Session State Management ---
if 'users_db' not in st.session_state:
    st.session_state['users_db'] = {
        'student': {'password': 'student', 'role': 'student', 'name': 'Student User'},
        'admin': {'password': 'admin', 'role': 'admin', 'name': 'Admin User'}
    }
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'notifications' not in st.session_state:
    st.session_state['notifications'] = 3

if not st.session_state['logged_in']:
    render_login()
    st.stop()

# --- Sidebar Navigation ---
st.sidebar.title("🎓 EduDash")
st.sidebar.markdown("---")

# User Profile Snippet in Sidebar
st.sidebar.markdown(f"**👤 {st.session_state['username']}**")
st.sidebar.markdown(f"🔔 Notifications: {st.session_state['notifications']}")
st.sidebar.markdown("---")

menu_options = {
    "Home": "🏠 Home",
    "Profile": "👤 Profile",
    "Learning Dashboard": "📚 Learning Dashboard",
    "Skill Assessment": "📝 Skill Assessment",
    "Personalized Learning Path": "🎯 Personalized Learning Path",
    "Learning Modules": "📖 Learning Modules",
    "AI Tutor": "🧠 AI Tutor",
    "Writing Evaluation": "✍ Writing Evaluation",
    "Practice Quiz": "📝 Practice Quiz",
    "AI Recommendations": "🤖 AI Recommendations",
    "Notifications": "🔔 Notifications",
    "Progress Analytics": "📈 Progress Analytics",
    "Certificates": "🏆 Certificates",
    "Teacher Dashboard": "👨‍🏫 Teacher Dashboard",
    "Admin Dashboard": "⚙ Admin Dashboard",
    "Settings": "⚙ User Settings",
    "Logout": "🚪 Logout"
}

if st.session_state.get('role') != 'admin':
    del menu_options["Teacher Dashboard"]
    del menu_options["Admin Dashboard"]

selection = st.sidebar.radio("Navigation", list(menu_options.values()))

# --- Top Bar (Search & Quick Actions) ---
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    search_query = st.text_input("🔍 Search courses, modules, or skills...", placeholder="Type to search...")
with col2:
    st.write("") # Padding
with col3:
    st.write("")
    st.markdown(f"<div style='text-align: right; padding-top: 10px;'>Dark/Light theme follows system settings.</div>", unsafe_allow_html=True)

st.markdown("---")


# Route to the selected page
if selection == menu_options["Home"]:
    render_home()
elif selection == menu_options["Profile"]:
    render_profile()
elif selection == menu_options["Learning Dashboard"]:
    render_learning_dashboard()
elif selection == menu_options["Skill Assessment"]:
    render_skill_assessment()
elif selection == menu_options["Personalized Learning Path"]:
    render_personalized_learning_path()
elif selection == menu_options["Learning Modules"]:
    render_learning_modules()
elif selection == menu_options["AI Tutor"]:
    render_ai_tutor()
elif selection == menu_options["Writing Evaluation"]:
    render_writing_evaluation()
elif selection == menu_options["Practice Quiz"]:
    render_practice_quiz()
elif selection == menu_options["AI Recommendations"]:
    render_ai_recommendations()
elif selection == menu_options["Notifications"]:
    render_notifications()
elif selection == menu_options["Progress Analytics"]:
    render_progress_analytics()
elif selection == menu_options["Certificates"]:
    render_certificates()
elif selection == menu_options["Teacher Dashboard"]:
    render_teacher_dashboard()
elif selection == menu_options["Admin Dashboard"]:
    render_admin_dashboard()
elif selection == menu_options["Settings"]:
    render_settings()
elif selection == menu_options["Logout"]:
    render_logout()

# --- Footer ---
st.markdown("""
    <div class="footer">
        © 2026 EduDash Learning Platform. All rights reserved.
    </div>
""", unsafe_allow_html=True)
