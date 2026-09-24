import streamlit as st
from streamlit_option_menu import option_menu

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

from styles.main import local_css
from pages.home import render_home
from pages.profile import render_profile
from pages.learning import render_learning_dashboard, render_skill_assessment, render_personalized_learning_path, render_learning_modules, render_practice_quiz
from pages.ai_tools import render_ai_tutor, render_writing_evaluation, render_ai_recommendations
from pages.analytics import render_progress_analytics, render_certificates
from pages.admin import render_teacher_dashboard, render_admin_dashboard
from pages.settings import render_notifications, render_settings, render_logout

local_css()
from pages.auth_page import render_auth_gateway

# --- Session State Management ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ''
if 'notifications' not in st.session_state:
    st.session_state['notifications'] = 3
if 'access_token' not in st.session_state:
    st.session_state['access_token'] = None


# --- Auth Gateway ---
if not st.session_state['logged_in']:
    render_auth_gateway()
else:
    # --- Sidebar Navigation ---
    st.sidebar.title("🎓 EduDash")
    st.sidebar.markdown("---")
    
    # User Profile Snippet in Sidebar
    st.sidebar.markdown(f"**👤 {st.session_state['username']}**")
    st.sidebar.markdown(f"🔔 Notifications: {st.session_state['notifications']}")
    st.sidebar.markdown("---")
    
    with st.sidebar:
        selection = option_menu(
            menu_title="Navigation",
            options=["Home", "Profile", "Learning Dashboard", "Skill Assessment", "Personalized Learning Path", "Learning Modules", "AI Tutor", "Writing Evaluation", "Practice Quiz", "AI Recommendations", "Notifications", "Progress Analytics", "Certificates", "Teacher Dashboard", "Admin Dashboard", "Settings", "Logout"],
            icons=["house", "person", "book", "pencil-square", "compass", "book-half", "robot", "pen", "check-circle", "lightbulb", "bell", "graph-up", "award", "person-workspace", "gear-wide-connected", "gear", "box-arrow-right"],
            menu_icon="cast",
            default_index=0,
        )
    
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
    if selection == "Home":
        render_home()
    elif selection == "Profile":
        render_profile()
    elif selection == "Learning Dashboard":
        render_learning_dashboard()
    elif selection == "Skill Assessment":
        render_skill_assessment()
    elif selection == "Personalized Learning Path":
        render_personalized_learning_path()
    elif selection == "Learning Modules":
        render_learning_modules()
    elif selection == "AI Tutor":
        render_ai_tutor()
    elif selection == "Writing Evaluation":
        render_writing_evaluation()
    elif selection == "Practice Quiz":
        render_practice_quiz()
    elif selection == "AI Recommendations":
        render_ai_recommendations()
    elif selection == "Notifications":
        render_notifications()
    elif selection == "Progress Analytics":
        render_progress_analytics()
    elif selection == "Certificates":
        render_certificates()
    elif selection == "Teacher Dashboard":
        render_teacher_dashboard()
    elif selection == "Admin Dashboard":
        render_admin_dashboard()
    elif selection == "Settings":
        render_settings()
    elif selection == "Logout":
            st.session_state['logged_in'] = False
            st.session_state['access_token'] = None
            st.session_state['username'] = ''
            st.rerun()
    
    # --- Footer ---
    st.markdown("""
        <div class="footer">
            © 2026 EduDash Learning Platform. All rights reserved.
        </div>
    """, unsafe_allow_html=True)
    