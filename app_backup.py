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

# --- Custom CSS for Styling ---
def local_css():
    st.markdown("""
        <style>
        /* Modern aesthetic colors and styling */
        :root {
            --primary-color: #4361ee;
            --secondary-color: #3f37c9;
            --background-color: #f8f9fa;
            --text-color: #2b2d42;
            --card-bg: #ffffff;
        }
        
        [data-theme="dark"] {
            --background-color: #121212;
            --text-color: #e0e0e0;
            --card-bg: #1e1e1e;
        }

        /* Metric Cards */
        div.css-1r6slb0.e1tzin5v2 {
            background-color: var(--card-bg);
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        div.css-1r6slb0.e1tzin5v2:hover {
            transform: translateY(-5px);
        }

        /* Top Bar Styling */
        .top-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid #ddd;
            margin-bottom: 20px;
        }
        
        /* Footer */
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: var(--card-bg);
            color: var(--text-color);
            text-align: center;
            padding: 10px;
            font-size: 14px;
            border-top: 1px solid #ddd;
            z-index: 999;
        }
        </style>
    """, unsafe_allow_html=True)

local_css()

# --- Session State Management ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = True
if 'username' not in st.session_state:
    st.session_state['username'] = 'Student User'
if 'notifications' not in st.session_state:
    st.session_state['notifications'] = 3

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

# --- Page Content Renders ---

def render_home():
    # --- Welcome Card ---
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)); 
                    padding: 30px; border-radius: 15px; color: white; margin-bottom: 25px;">
            <h1 style="color: white; margin-bottom: 0;">Welcome back, {st.session_state['username']}! 🚀</h1>
            <h4 style="color: #e0e0e0; font-weight: 300;">Level 12 • Data Science Enthusiast</h4>
            <div style="margin-top: 20px; background: rgba(255,255,255,0.2); padding: 15px; border-radius: 10px;">
                <strong>🎯 Today's Goal:</strong> Complete 'Advanced Python Decorators' module
                <br>
                <strong>🔥 Learning Streak:</strong> 7 Days
                <br>
                <div style="margin-top: 10px;">
                    Course Completion: 65%
                    <div style="background: rgba(255,255,255,0.3); height: 8px; border-radius: 4px; margin-top: 5px;">
                        <div style="background: #4cc9f0; width: 65%; height: 100%; border-radius: 4px;"></div>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # --- Quick Statistics Cards ---
    st.subheader("📊 Quick Statistics")
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Completed Lessons", "42", "3 this week")
    c2.metric("Current Course", "Python", "65% done")
    c3.metric("Quiz Accuracy", "92%", "4% ↑")
    c4.metric("Weekly Progress", "8/10", "tasks")
    c5.metric("Learning Hours", "124h", "5h ↑")
    c6.metric("Certificates", "3", "1 new")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Charts Section ---
    st.subheader("📈 Learning Analytics")
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # Weekly Progress Chart
        st.markdown("**Weekly Progress (Hours)**")
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        hours = [2.5, 3.0, 1.5, 4.0, 2.0, 5.0, 3.5]
        df_weekly = pd.DataFrame({'Day': days, 'Hours': hours})
        fig1 = px.bar(df_weekly, x='Day', y='Hours', color_discrete_sequence=['#4361ee'])
        fig1.update_layout(margin=dict(l=20, r=20, t=20, b=20), height=300)
        st.plotly_chart(fig1, use_container_width=True)
        
    with chart_col2:
        # Score Trend Chart
        st.markdown("**Score Trend (%)**")
        weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5']
        scores = [75, 82, 80, 88, 92]
        df_scores = pd.DataFrame({'Week': weeks, 'Score': scores})
        fig2 = px.line(df_scores, x='Week', y='Score', markers=True, color_discrete_sequence=['#f72585'])
        fig2.update_layout(margin=dict(l=20, r=20, t=20, b=20), height=300)
        st.plotly_chart(fig2, use_container_width=True)

    # --- Recent Activity & Upcoming Lessons ---
    st.markdown("<br>", unsafe_allow_html=True)
    act_col1, act_col2 = st.columns(2)
    
    with act_col1:
        st.subheader("🕒 Recent Activity")
        st.info("✅ Completed Quiz: Pandas DataFrames (Score: 95%)")
        st.info("✅ Watched Video: Intro to Neural Networks")
        st.info("✅ Earned Badge: Consistent Learner")
        
    with act_col2:
        st.subheader("📅 Upcoming Lessons")
        st.warning("⏳ Advanced Python Decorators (Due Tomorrow)")
        st.warning("⏳ Machine Learning Math Basics (Due in 3 days)")
        st.warning("⏳ Group Project Discussion (Friday 10:00 AM)")

def render_profile():
    st.title("👤 Student Profile")
    
    # Profile Completion Bar
    st.markdown("**Profile Completion**")
    st.progress(85, text="85% Complete")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Profile Picture")
        # Placeholder for profile picture (using Dicebear API for a modern avatar)
        st.image("https://api.dicebear.com/7.x/avataaars/svg?seed=Student", width=200)
        st.file_uploader("Upload Profile Picture", type=['png', 'jpg', 'jpeg'])
        
        st.markdown("---")
        st.subheader("Edit Profile")
        if st.button("✏️ Edit Details", use_container_width=True):
            st.toast("Edit mode enabled!", icon="✏️")
    
    with col2:
        st.subheader("Personal Information")
        with st.container(border=True):
            c1, c2 = st.columns(2)
            c1.text_input("Full Name", value=st.session_state['username'])
            c2.text_input("Email", value="student@edudash.com")
            c1.text_input("Phone", value="+1 (555) 123-4567")
            c2.text_input("Location", value="New York, USA")
        
        st.subheader("Learning Preferences")
        with st.container(border=True):
            st.selectbox("Highest Education", ["High School", "Bachelor's Degree", "Master's Degree", "PhD"], index=1)
            st.multiselect("Language", ["English", "Spanish", "French", "German", "Mandarin"], default=["English", "Spanish"])
            
            c3, c4 = st.columns(2)
            c3.selectbox("Learning Goal", ["Career Switch", "Upskilling", "Hobby", "Academic Requirements"])
            c4.select_slider("Current Skill Level", options=["Beginner", "Intermediate", "Advanced", "Expert"], value="Intermediate")
            
            st.time_input("Preferred Learning Time", value=datetime.strptime('18:00', '%H:%M').time())
            
        st.button("Save Profile Changes", type="primary")

def render_learning_dashboard():
    st.title("Learning Dashboard")
    st.progress(65, text="Overall Progress - 65%")
    st.subheader("Current Modules")
    st.write("- Introduction to Machine Learning (In Progress - 40%)")
    st.write("- Data Visualization (Completed)")

def render_skill_assessment():
    st.title("📝 Skill Assessment")
    
    # Initialize state variables
    if 'assessment_state' not in st.session_state:
        st.session_state['assessment_state'] = 'selection'
    
    if st.session_state['assessment_state'] == 'selection':
        st.subheader("Select Assessment Category")
        
        col1, col2 = st.columns(2)
        with col1:
            category = st.selectbox("Category", ["Reading", "Writing", "Mathematics", "English", "Digital Literacy", "Life Skills"])
        with col2:
            difficulty = st.selectbox("Difficulty Level", ["Beginner", "Intermediate", "Advanced"])
            
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Start Assessment", type="primary"):
            st.session_state['assessment_state'] = 'taking'
            st.rerun()
            
    elif st.session_state['assessment_state'] == 'taking':
        # Header info
        c1, c2 = st.columns([3, 1])
        c1.subheader("Question 1 of 10")
        c2.info("⏱ Time Remaining: 14:23")
        
        st.progress(10, text="Progress: 10%")
        
        st.markdown("---")
        st.markdown("### Which of the following is the correct answer?")
        
        st.radio("Select your answer:", [
            "Option A: Correct answer here.",
            "Option B: Incorrect answer.",
            "Option C: Another incorrect answer.",
            "Option D: None of the above."
        ], index=None)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        nav1, nav2, nav3 = st.columns([1, 6, 3])
        nav1.button("⬅ Previous")
        if nav3.button("Submit Assessment ✅", type="primary"):
            st.session_state['assessment_state'] = 'results'
            st.rerun()
            
    elif st.session_state['assessment_state'] == 'results':
        st.subheader("📊 Assessment Results")
        
        # Display Requirements
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Reading", "75%")
        c2.metric("Writing", "82%")
        c3.metric("Math", "65%")
        c4.metric("Overall", "74%")
        
        st.markdown("---")
        
        # Radar Chart
        categories = ['Reading', 'Writing', 'Mathematics', 'English', 'Digital Literacy', 'Life Skills']
        scores = [75, 82, 65, 80, 90, 85]
        
        df_radar = pd.DataFrame(dict(
            Score=scores,
            Skill=categories
        ))
        
        fig = px.line_polar(df_radar, r='Score', theta='Skill', line_close=True, markers=True, color_discrete_sequence=['#4361ee'])
        fig.update_traces(fill='toself', fillcolor='rgba(67, 97, 238, 0.3)')
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), margin=dict(l=20, r=20, t=20, b=20), height=400)
        
        st.plotly_chart(fig, use_container_width=True)
        
        if st.button("🔄 Retake Assessment"):
            st.session_state['assessment_state'] = 'selection'
            st.rerun()

def render_personalized_learning_path():
    st.title("🎯 Personalized Learning Path")
    st.markdown("Your **AI-Generated Roadmap**, tailored to your learning goals and recent assessments.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Path Data
    roadmap = [
        {"title": "Beginner Level", "time": "N/A", "difficulty": "N/A", "status": "Completed", "ai": "Assessment placed you directly here."},
        {"title": "Alphabet", "time": "2 Hours", "difficulty": "Beginner", "status": "Completed", "ai": "Mastered foundational letters quickly."},
        {"title": "Words", "time": "4 Hours", "difficulty": "Beginner", "status": "In Progress", "ai": "Focus on common sight words to boost fluency."},
        {"title": "Sentences", "time": "6 Hours", "difficulty": "Intermediate", "status": "Locked", "ai": "Will unlock upon completing 'Words'. Connects sight words."},
        {"title": "Paragraphs", "time": "8 Hours", "difficulty": "Intermediate", "status": "Locked", "ai": "Essential for building sustained reading comprehension."},
        {"title": "Story Reading", "time": "10 Hours", "difficulty": "Advanced", "status": "Locked", "ai": "Culminating exercise combining all previous modules."},
        {"title": "Assessment", "time": "1 Hour", "difficulty": "Advanced", "status": "Locked", "ai": "Final check before awarding certification."},
        {"title": "Certificate", "time": "N/A", "difficulty": "N/A", "status": "Locked", "ai": "Official proof of reading proficiency."}
    ]
    
    for i, step in enumerate(roadmap):
        # Determine card border color based on status
        border_color = "var(--primary-color)" if step["status"] == "In Progress" else ("#198754" if step["status"] == "Completed" else "#6c757d")
        icon = "✅" if step["status"] == "Completed" else ("⏳" if step["status"] == "In Progress" else "🔒")
        
        st.markdown(f"""
            <div style="border-left: 5px solid {border_color}; background: var(--card-bg); 
                        padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 5px;">
                <h3 style="margin: 0; color: var(--text-color);">{icon} {step['title']}</h3>
                <div style="color: var(--text-color); margin-top: 12px; font-size: 15px;">
                    <strong>⏱ Est. Time:</strong> {step['time']} &nbsp;&nbsp;|&nbsp;&nbsp; 
                    <strong>📊 Difficulty:</strong> {step['difficulty']} &nbsp;&nbsp;|&nbsp;&nbsp; 
                    <strong>📌 Status:</strong> <span style="color: {border_color}; font-weight: bold;">{step['status']}</span>
                </div>
                <div style="margin-top: 15px; padding: 12px; background: rgba(67, 97, 238, 0.1); 
                            border-radius: 8px; font-style: italic; color: var(--text-color);">
                    🤖 <strong>AI Recommendation:</strong> {step['ai']}
                </div>
            </div>
        """, unsafe_allow_html=True)
            
        if i < len(roadmap) - 1:
            st.markdown("<div style='text-align: center; font-size: 28px; color: #888; margin: 10px 0;'>↓</div>", unsafe_allow_html=True)

def render_learning_modules():
    st.title("📖 Learning Modules")
    st.markdown("Select a category and start your interactive lessons.")
    
    categories = ["English", "Mathematics", "Reading", "Writing", "Life Skills", "Digital Literacy"]
    tabs = st.tabs(categories)
    
    for i, tab in enumerate(tabs):
        with tab:
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Layout: Sidebar-like column for lesson selection, Main area for content
            col1, col2 = st.columns([1, 3])
            
            with col1:
                st.markdown("### 📚 Lessons")
                # Using a container with border to act as a sidebar menu
                with st.container(border=True):
                    selected_lesson = st.radio(
                        "Course Curriculum",
                        [
                            f"1. Introduction to {categories[i]}", 
                            f"2. Core Concepts & Foundations", 
                            f"3. Advanced Topics",
                            f"4. Practical Applications",
                            f"5. Final Review"
                        ],
                        key=f"lesson_select_{i}"
                    )
                
                st.progress(40, text="Course Progress: 40%")
                
            with col2:
                with st.container(border=True):
                    # Lesson Header and Actions
                    head_col, action_col = st.columns([2, 1])
                    with head_col:
                        st.markdown(f"<h2>{selected_lesson}</h2>", unsafe_allow_html=True)
                    with action_col:
                        st.markdown("<br>", unsafe_allow_html=True)
                        act1, act2 = st.columns(2)
                        act1.button("🔖 Bookmark", key=f"bm_{i}", use_container_width=True)
                        act2.button("⬇️ PDF", key=f"dl_{i}", use_container_width=True)
                    
                    st.markdown("---")
                    
                    # Video Placeholder (Using a generic placeholder image to represent a video player if no video url is handy, 
                    # but we can use a sample youtube video for demonstration)
                    st.video("https://www.youtube.com/watch?v=D-UmfqFjpl0") 
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Content Tabs
                    lesson_tabs = st.tabs(["📝 Notes", "💡 Examples", "✍ Exercises"])
                    
                    with lesson_tabs[0]:
                        st.markdown("#### Comprehensive Notes")
                        st.write(f"Welcome to the notes for **{selected_lesson}**. In this section, you will learn the foundational principles that govern this topic.")
                        st.info("💡 **Tip:** You can download these notes as a PDF using the button in the top right corner.")
                        st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.")
                        
                    with lesson_tabs[1]:
                        st.markdown("#### Practical Examples")
                        st.write("Here are some real-world examples demonstrating the concepts from the notes.")
                        st.code("Example 1:\nStep 1: Identify the problem.\nStep 2: Apply the concept.\nStep 3: Solve and verify.")
                        st.success("Correct Application Example shown above.")
                        
                    with lesson_tabs[2]:
                        st.markdown("#### Practice Exercises")
                        st.write("Test your understanding of the material.")
                        st.radio("Question 1: Which of the following is the best approach?", 
                                 ["Option A", "Option B", "Option C"], key=f"q1_{i}", index=None)
                        st.button("Check Answer", key=f"check_{i}")
                    
                    st.markdown("---")
                    
                    # Completion Button
                    c_btn_col1, c_btn_col2 = st.columns([3, 1])
                    with c_btn_col2:
                        if st.button("✅ Mark as Complete", type="primary", key=f"complete_{i}", use_container_width=True):
                            st.success("Lesson Complete! 🎉")

def render_ai_tutor():
    st.title("🧠 AI Tutor")
    st.markdown("Your personal AI assistant to help you understand concepts, practice skills, and navigate your coursework.")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I am your AI Tutor. How can I help you today?"}
        ]
        
    # Suggested Questions / Quick Buttons
    st.markdown("##### Quick Questions")
    quick_cols = st.columns(4)
    suggested_q = None
    if quick_cols[0].button("Explain Fractions", use_container_width=True):
        suggested_q = "Explain Fractions"
    if quick_cols[1].button("Teach Alphabet", use_container_width=True):
        suggested_q = "Teach Alphabet"
    if quick_cols[2].button("Help with Grammar", use_container_width=True):
        suggested_q = "Help with Grammar"
    if quick_cols[3].button("Solve this Question", use_container_width=True):
        suggested_q = "Solve this Question"
        
    st.markdown("---")
    
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Voice Input Placeholder (Visual only for now)
    st.markdown(
        """
        <div style="text-align: right; padding-right: 15px; margin-bottom: -15px; position: relative; z-index: 10;">
            <span style="font-size: 20px; cursor: pointer; color: #888;" title="Voice Input (Placeholder)">🎤</span>
        </div>
        """, 
        unsafe_allow_html=True
    )

    # React to user input
    user_q = st.chat_input("Ask your AI tutor or click the microphone above to speak...")
    
    # Handle both quick buttons and chat input
    prompt = user_q or suggested_q
    
    if prompt:
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # Simulated typing animation response
            mock_response = f"I'd be happy to help you with **{prompt}**! As an AI tutor, I can explain concepts step-by-step, provide examples, or test your knowledge. What specific part are you struggling with?"
            for chunk in mock_response.split(" "):
                full_response += chunk + " "
                time.sleep(0.05)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
            
            # Final response without cursor
            message_placeholder.markdown(full_response)
            
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})

def render_writing_evaluation():
    st.title("✍️ Writing Evaluation")
    st.markdown("Practice your writing skills. Enter your text below and get instant AI-powered feedback on grammar, vocabulary, and structure.")
    
    # Input Area
    user_text = st.text_area("Your text:", height=200, placeholder="Start typing your essay or paragraph here...")
    
    if st.button("🔍 Evaluate Text", type="primary"):
        if not user_text.strip():
            st.warning("Please enter some text to evaluate.")
        else:
            with st.spinner("Analyzing your writing..."):
                time.sleep(1.5) # Simulate processing delay
                
            st.success("Evaluation Complete!")
            st.markdown("---")
            
            # Top-level Charts (Gauge and Circle)
            chart_col1, chart_col2 = st.columns(2)
            
            with chart_col1:
                st.subheader("Overall Score")
                # Gauge Meter using Plotly Graph Objects
                fig_gauge = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = 85,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Writing Proficiency"},
                    gauge = {'axis': {'range': [None, 100]},
                             'bar': {'color': "#4361ee"},
                             'steps': [
                                 {'range': [0, 50], 'color': "#ff9999"},
                                 {'range': [50, 75], 'color': "#ffcc99"},
                                 {'range': [75, 100], 'color': "#99ff99"}],
                             'threshold': {
                                 'line': {'color': "red", 'width': 4},
                                 'thickness': 0.75,
                                 'value': 90}}
                ))
                fig_gauge.update_layout(height=250, margin=dict(l=10, r=10, t=30, b=10))
                st.plotly_chart(fig_gauge, use_container_width=True)
                
            with chart_col2:
                st.subheader("Progress Circle")
                # Progress Circle (Donut Chart)
                df_progress = pd.DataFrame({'Category': ['Completed', 'Remaining'], 'Value': [85, 15]})
                fig_circle = px.pie(df_progress, values='Value', names='Category', hole=0.7, 
                                    color='Category', color_discrete_map={'Completed': '#4361ee', 'Remaining': '#e0e0e0'})
                fig_circle.update_layout(showlegend=False, height=250, margin=dict(l=10, r=10, t=10, b=10),
                                         annotations=[dict(text='85%', x=0.5, y=0.5, font_size=30, showarrow=False)])
                st.plotly_chart(fig_circle, use_container_width=True)
                
            # Metrics Row
            st.markdown("### Detailed Metrics")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Grammar Score", "88/100", "+2")
            m2.metric("Vocabulary Score", "76/100", "-1")
            m3.metric("Readability", "Grade 8", "Optimal")
            m4.metric("Sentence Structure", "Good", "85%")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Feedback Details
            col_feed1, col_feed2 = st.columns(2)
            with col_feed1:
                st.error("🚨 Spelling Errors")
                st.write("- 'teh' -> 'the'")
                st.write("- 'recieve' -> 'receive'")
                st.write("- 'alot' -> 'a lot'")
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.warning("💡 Suggestions")
                st.write("- Try using more varied sentence lengths to improve flow.")
                st.write("- Enhance your vocabulary by replacing basic adjectives with stronger ones.")
                
            with col_feed2:
                st.success("✅ Correct Version")
                st.info(f"**Your Text (Corrected):**\n\n{user_text}\n\n*(Note: In a real implementation, this box would display the AI-corrected version of the text you entered above. For now, it mirrors your input.)*")

def render_practice_quiz():
    st.title("📝 Practice Quiz")
    st.markdown("Test your knowledge across different question formats.")
    
    # Quiz Header (Timer and Progress)
    head1, head2 = st.columns([3, 1])
    with head1:
        st.progress(40, text="Quiz Progress: Question 2 of 5")
    with head2:
        st.info("⏱ Time Remaining: 08:45")
        
    st.markdown("---")
    
    # Use tabs to showcase different Question Types
    q_tabs = st.tabs(["MCQ", "Fill in the Blank", "True/False", "Matching", "Reading Comprehension"])
    
    with q_tabs[0]:
        st.subheader("Multiple Choice Question")
        st.markdown("**Q1: What is the primary function of a noun in a sentence?**")
        ans_mcq = st.radio("Select one:", ["To describe an action", "To name a person, place, or thing", "To connect clauses", "To describe a verb"], key="q_mcq", index=None)
        
        if st.button("Submit MCQ", key="sub_mcq"):
            if ans_mcq == "To name a person, place, or thing":
                st.success("Correct! 🎉")
                st.info("💡 **Explanation:** A noun is a naming word. It identifies a person, place, thing, or idea.")
            else:
                st.error("Incorrect. Try again!")
                
    with q_tabs[1]:
        st.subheader("Fill in the Blank")
        st.markdown("**Q2: Complete the following sentence:**")
        st.markdown("The quick brown fox _____ over the lazy dog.")
        ans_fill = st.text_input("Your answer:", key="q_fill")
        
        if st.button("Submit Fill in the Blank", key="sub_fill"):
            if ans_fill.lower().strip() == "jumps":
                st.success("Correct! 🎉")
                st.info("💡 **Explanation:** 'jumps' is the correct verb that completes the classic pangram.")
            else:
                st.error("Incorrect. Hint: It's an action word starting with 'j'.")
                
    with q_tabs[2]:
        st.subheader("True / False")
        st.markdown("**Q3: Water boils at 100 degrees Celsius at sea level.**")
        ans_tf = st.radio("Select True or False:", ["True", "False"], key="q_tf", index=None)
        
        if st.button("Submit True/False", key="sub_tf"):
            if ans_tf == "True":
                st.success("Correct! 🎉")
                st.info("💡 **Explanation:** 100°C is the standard boiling point of water at 1 atmosphere of pressure.")
            else:
                st.error("Incorrect.")
                
    with q_tabs[3]:
        st.subheader("Matching")
        st.markdown("**Q4: Match the word to its synonym:**")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("- **1. Happy**")
            st.markdown("- **2. Fast**")
            st.markdown("- **3. Big**")
        with c2:
            st.selectbox("Match for Happy:", ["Quick", "Joyful", "Large"], key="match1", index=1)
            st.selectbox("Match for Fast:", ["Quick", "Joyful", "Large"], key="match2", index=0)
            st.selectbox("Match for Big:", ["Quick", "Joyful", "Large"], key="match3", index=2)
            
        if st.button("Submit Matching", key="sub_match"):
            st.success("All matches are correct! 🎉")
            st.info("💡 **Explanation:** Happy = Joyful, Fast = Quick, Big = Large.")
            
    with q_tabs[4]:
        st.subheader("Reading Comprehension")
        with st.expander("📖 Read the Passage (Click to expand)", expanded=True):
            st.write("The Amazon rainforest, covering much of northwestern Brazil and extending into Colombia, Peru and other South American countries, is the world's largest tropical rainforest, famed for its biodiversity.")
            
        st.markdown("**Q5: According to the passage, where is the Amazon rainforest primarily located?**")
        ans_rc = st.text_area("Your Answer:", key="q_rc")
        if st.button("Submit Comprehension", key="sub_rc"):
            if ans_rc.strip():
                st.success("Good answer! 🎉")
                st.info("💡 **Explanation:** The passage states it covers much of northwestern Brazil and extends into other South American countries.")
            else:
                st.warning("Please enter an answer.")
            
    st.markdown("---")
    
    # Scoreboard and Leaderboard
    score_col, lead_col = st.columns(2)
    with score_col:
        st.subheader("🏆 Your Scoreboard")
        with st.container(border=True):
            s1, s2 = st.columns(2)
            s1.metric("Current Score", "850 pts", "+50")
            s2.metric("Accuracy", "92%", "↑ 2%")
            st.write("🔥 **Streak:** 5 Quizzes in a row!")
            
    with lead_col:
        st.subheader("👑 Global Leaderboard")
        with st.container(border=True):
            df_leaderboard = pd.DataFrame({
                "Rank": ["🥇 1", "🥈 2", "🥉 3", "4", "5"],
                "Student": ["Alex M.", "Sarah J.", "You", "David K.", "Emma W."],
                "Points": [1200, 950, 850, 800, 750]
            })
            
            # Highlight current user in the dataframe using pandas styling
            def highlight_user(val):
                return 'background-color: #4361ee; color: white' if val == 'You' else ''
            
            st.dataframe(df_leaderboard.style.map(highlight_user, subset=['Student']), hide_index=True, use_container_width=True)

def render_progress_analytics():
    st.title("📈 Progress Analytics")
    st.markdown("Monitor your learning journey with detailed performance metrics and visual analytics.")
    
    # Metric Cards
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Overall Accuracy", "88%", "+3%")
    c2.metric("Total Hours", "142h", "+12h")
    c3.metric("Courses Completed", "14", "+2")
    c4.metric("Current Streak", "12 Days", "🔥")
    
    st.markdown("---")
    
    # Row 1: Line Chart & Pie Chart
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Learning Progress (Over Time)")
        # Line Chart
        df_progress = pd.DataFrame({
            "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"],
            "Score": [60, 65, 70, 78, 82, 85, 90]
        })
        fig_line = px.line(df_progress, x="Month", y="Score", markers=True, color_discrete_sequence=['#4361ee'])
        fig_line.update_layout(height=300, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_line, use_container_width=True)
        
    with col2:
        st.subheader("Completion Rate")
        # Pie Chart
        df_comp = pd.DataFrame({"Status": ["Completed", "In Progress", "Not Started"], "Count": [14, 5, 8]})
        fig_pie = px.pie(df_comp, values="Count", names="Status", hole=0.4,
                         color_discrete_sequence=['#198754', '#ffc107', '#dc3545'])
        fig_pie.update_layout(height=300, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_pie, use_container_width=True)
        
    st.markdown("---")
    
    # Row 2: Bar Chart & Radar Chart
    col3, col4 = st.columns([1, 1])
    
    with col3:
        st.subheader("Daily Learning Time")
        # Bar Chart
        df_daily = pd.DataFrame({
            "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            "Hours": [2, 3.5, 1.5, 4, 2.5, 5, 4.5]
        })
        fig_bar = px.bar(df_daily, x="Day", y="Hours", color="Hours", color_continuous_scale="Blues")
        fig_bar.update_layout(height=350, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with col4:
        st.subheader("Skill Proficiencies (Weak Topics)")
        # Radar Chart
        categories = ['Reading', 'Writing', 'Math', 'Digital Lit.', 'Life Skills', 'English']
        scores = [85, 78, 60, 92, 88, 75]
        df_radar = pd.DataFrame(dict(Score=scores, Skill=categories))
        fig_radar = px.line_polar(df_radar, r='Score', theta='Skill', line_close=True, markers=True, color_discrete_sequence=['#f72585'])
        fig_radar.update_traces(fill='toself', fillcolor='rgba(247, 37, 133, 0.2)')
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), height=350, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_radar, use_container_width=True)
        
    st.markdown("---")
    
    # Row 3: Heatmap (Weekly Activity)
    st.subheader("Weekly Activity Heatmap")
    # Mock heatmap data (Hours spent per day per week)
    z = [
        [1, 3, 2, 4],
        [2, 4, 3, 5],
        [0, 1, 4, 2],
        [3, 2, 5, 4],
        [4, 5, 3, 1],
        [5, 4, 5, 5],
        [3, 3, 2, 4]
    ]
    df_heat = pd.DataFrame(z, columns=["Week 1", "Week 2", "Week 3", "Week 4"], 
                           index=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
    fig_heat = px.imshow(df_heat, labels=dict(x="Week", y="Day", color="Hours"),
                         color_continuous_scale="Greens", aspect="auto")
    fig_heat.update_layout(height=300, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig_heat, use_container_width=True)

def render_certificates():
    st.title("🏆 Certificates & Achievements")
    st.markdown("Celebrate your progress! Here you can view your earned certificates, badges, and learning milestones.")
    
    # Trigger celebration effect once per session
    if 'balloons_shown' not in st.session_state:
        st.balloons()
        st.session_state['balloons_shown'] = True

    # Main Tabs
    cert_tabs = st.tabs(["📜 Certificates", "🏅 Badges & Milestones"])
    
    with cert_tabs[0]:
        st.subheader("Your Completed Courses & Certificates")
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Displaying mock certificates
        cert_col1, cert_col2, cert_col3 = st.columns(3)
        
        with cert_col1:
            with st.container(border=True):
                st.markdown("<h1 style='text-align: center; font-size: 50px;'>📘</h1>", unsafe_allow_html=True)
                st.markdown("<h4 style='text-align: center;'>English 101</h4>", unsafe_allow_html=True)
                st.markdown("<p style='text-align: center; color: #888;'>Completed: May 15, 2026</p>", unsafe_allow_html=True)
                st.download_button("⬇️ Download PDF", "Mock Certificate Data", file_name="English101_Certificate.pdf", key="dl_cert1", use_container_width=True)
                
        with cert_col2:
            with st.container(border=True):
                st.markdown("<h1 style='text-align: center; font-size: 50px;'>📐</h1>", unsafe_allow_html=True)
                st.markdown("<h4 style='text-align: center;'>Basic Math</h4>", unsafe_allow_html=True)
                st.markdown("<p style='text-align: center; color: #888;'>Completed: June 22, 2026</p>", unsafe_allow_html=True)
                st.download_button("⬇️ Download PDF", "Mock Certificate Data", file_name="BasicMath_Certificate.pdf", key="dl_cert2", use_container_width=True)
                
        with cert_col3:
            with st.container(border=True):
                st.markdown("<h1 style='text-align: center; font-size: 50px;'>💻</h1>", unsafe_allow_html=True)
                st.markdown("<h4 style='text-align: center;'>Digital Literacy</h4>", unsafe_allow_html=True)
                st.markdown("<p style='text-align: center; color: #888;'>Completed: July 10, 2026</p>", unsafe_allow_html=True)
                st.download_button("⬇️ Download PDF", "Mock Certificate Data", file_name="DigitalLit_Certificate.pdf", key="dl_cert3", use_container_width=True)
                
    with cert_tabs[1]:
        col_badge, col_mile = st.columns([1, 1])
        
        with col_badge:
            st.subheader("Achievement Badges")
            st.markdown("---")
            b1, b2, b3 = st.columns(3)
            with b1:
                st.markdown("<div style='text-align: center; font-size: 40px;'>🔥</div>", unsafe_allow_html=True)
                st.markdown("<div style='text-align: center; font-weight: bold;'>7-Day Streak</div>", unsafe_allow_html=True)
            with b2:
                st.markdown("<div style='text-align: center; font-size: 40px;'>🎯</div>", unsafe_allow_html=True)
                st.markdown("<div style='text-align: center; font-weight: bold;'>Perfect Quiz</div>", unsafe_allow_html=True)
            with b3:
                st.markdown("<div style='text-align: center; font-size: 40px;'>🦉</div>", unsafe_allow_html=True)
                st.markdown("<div style='text-align: center; font-weight: bold;'>Night Owl</div>", unsafe_allow_html=True)
                
        with col_mile:
            st.subheader("Learning Milestones")
            st.markdown("---")
            st.info("✅ **Milestone 1:** Completed First Module (March 2026)")
            st.info("✅ **Milestone 2:** Reached 50 Learning Hours (April 2026)")
            st.info("✅ **Milestone 3:** Passed Comprehensive Assessment (June 2026)")
            st.warning("⏳ **Milestone 4:** Master 5 Different Subjects (In Progress)")

def render_teacher_dashboard():
    st.title("👨‍🏫 Teacher Dashboard")
    st.markdown("Overview of your classroom, student performance, and administrative actions.")
    
    # Top Actions & Export
    act_col1, act_col2 = st.columns([4, 1])
    with act_col2:
        # Mock download button
        st.download_button("📥 Export Reports (CSV)", "ID,Name,Score\nS101,Alice,88", file_name="student_reports.csv", use_container_width=True)
    
    # KPIs / Metric Cards
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Total Students", "124")
    m2.metric("Active Students", "98", "79%")
    m3.metric("Weak Students", "12", "-3")
    m4.metric("Average Score", "76%", "+2%")
    m5.metric("Attendance", "92%", "Good")
    
    st.markdown("---")
    
    # Charts Row
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.subheader("Performance Trends")
        # Line Chart for Performance
        df_perf = pd.DataFrame({
            "Week": ["W1", "W2", "W3", "W4", "W5"],
            "Avg Score": [70, 72, 75, 74, 76]
        })
        fig_perf = px.line(df_perf, x="Week", y="Avg Score", markers=True, color_discrete_sequence=['#4361ee'])
        fig_perf.update_layout(height=300, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig_perf, use_container_width=True)
        
    with chart_col2:
        st.subheader("Course Completion")
        # Bar Chart for Course Completion
        df_course = pd.DataFrame({
            "Course": ["English", "Math", "Reading", "Life Skills"],
            "Completion Rate": [85, 60, 90, 75]
        })
        fig_course = px.bar(df_course, x="Course", y="Completion Rate", color="Completion Rate", color_continuous_scale="Viridis")
        fig_course.update_layout(height=300, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig_course, use_container_width=True)
        
    st.markdown("---")
    
    # Student Table Section
    st.subheader("📋 Student Directory")
    
    # Search and Filter
    f_col1, f_col2, f_col3 = st.columns([2, 1, 1])
    with f_col1:
        search_query = st.text_input("🔍 Search Student by Name or ID...", placeholder="e.g. Alice")
    with f_col2:
        filter_status = st.selectbox("Status Filter", ["All", "Active", "Inactive", "At Risk"])
    with f_col3:
        filter_course = st.selectbox("Course Filter", ["All", "English", "Math", "Reading"])
        
    # Mock Student Data
    df_students = pd.DataFrame({
        "ID": ["S101", "S102", "S103", "S104", "S105"],
        "Name": ["Alice Smith", "Bob Johnson", "Charlie Davis", "Diana Prince", "Evan Wright"],
        "Status": ["Active", "Active", "At Risk", "Active", "Inactive"],
        "Score": [88, 75, 45, 95, 0],
        "Attendance": ["95%", "85%", "60%", "98%", "10%"],
        "Last Login": ["Today", "Yesterday", "3 Days Ago", "Today", "1 Month Ago"]
    })
    
    # Filtering Logic (Mock implementation)
    if search_query:
        df_students = df_students[df_students['Name'].str.contains(search_query, case=False) | df_students['ID'].str.contains(search_query, case=False)]
    if filter_status != "All":
        df_students = df_students[df_students['Status'] == filter_status]
        
    def color_status(val):
        color = '#198754' if val == 'Active' else ('#dc3545' if val == 'At Risk' else '#6c757d')
        return f'color: {color}; font-weight: bold'
        
    st.dataframe(df_students.style.map(color_status, subset=['Status']), use_container_width=True, hide_index=True)

def render_admin_dashboard():
    st.title("⚙️ Admin Dashboard")
    st.markdown("System administration, content management, and platform configuration.")
    
    # High-level System Statistics
    st.subheader("📊 System Statistics")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Users", "1,245", "+54")
    m2.metric("Active Courses", "32", "+2")
    m3.metric("Platform Uptime", "99.9%", "Optimal")
    m4.metric("Storage Used", "45 GB / 100 GB", "Stable")
    
    st.markdown("---")
    
    # Admin Control Tabs
    admin_tabs = st.tabs([
        "👥 Manage Users & Roles", 
        "📚 Course Management", 
        "📤 Upload Content", 
        "📈 View Reports", 
        "⚙️ Settings"
    ])
    
    with admin_tabs[0]:
        st.subheader("Manage Users & Roles")
        u_col1, u_col2 = st.columns([1, 1])
        with u_col1:
            with st.container(border=True):
                st.markdown("#### User Actions")
                st.text_input("Search User by Email or ID", key="admin_u_search")
                st.selectbox("Select Action", ["Edit User", "Suspend Account", "Reset Password", "Change Role"])
                st.button("Apply Action", type="primary")
        with u_col2:
            with st.container(border=True):
                st.markdown("#### Role Management")
                st.selectbox("Select Role to Edit", ["Student", "Teacher", "Content Creator", "Administrator"])
                st.checkbox("Can create and edit courses", value=False)
                st.checkbox("Can grade assignments", value=True)
                st.checkbox("Can manage other users", value=False)
                st.button("Update Role Permissions")
            
    with admin_tabs[1]:
        st.subheader("Course, Lesson, and Quiz Management")
        st.selectbox("Select Course to Manage", ["English 101", "Basic Mathematics", "Digital Literacy Basics"])
        c_action = st.radio("What would you like to manage?", ["Manage Lessons", "Manage Quizzes", "Edit Course Settings"], horizontal=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if c_action == "Manage Lessons":
            st.info("Drag and drop to reorder lessons, or click below to add new content.")
            st.button("➕ Add New Lesson", type="primary")
        elif c_action == "Manage Quizzes":
            st.info("Build new quizzes or update existing question banks for this course.")
            st.button("➕ Create New Quiz", type="primary")
        else:
            st.info("Update the course title, description, thumbnail, and enrollment settings.")
            st.button("💾 Save Course Settings", type="primary")
            
    with admin_tabs[2]:
        st.subheader("Upload Content")
        st.write("Upload media, PDFs, or bulk CSV data directly to the platform storage.")
        with st.container(border=True):
            st.file_uploader("Select files to upload", accept_multiple_files=True)
            st.selectbox("Assign to Course (Optional)", ["None", "English 101", "Basic Mathematics"])
            st.button("Upload Files", type="primary")
        
    with admin_tabs[3]:
        st.subheader("System Reports")
        st.write("Generate and download platform-wide analytics and audit logs.")
        with st.container(border=True):
            st.date_input("Select Date Range", [])
            st.selectbox("Report Type", ["User Activity Log", "Financial / Subscription", "Overall Course Engagement", "Security Audit"])
            st.download_button("📥 Generate & Download Report", "mock_report_data", file_name="system_report.csv")
        
    with admin_tabs[4]:
        st.subheader("Platform Settings")
        st.write("Configure global platform behavior.")
        with st.container(border=True):
            st.toggle("Enable Maintenance Mode", value=False, help="Restricts access to non-admins.")
            st.toggle("Allow New User Registration", value=True)
            st.toggle("Enable AI Tutor Globally", value=True)
            st.text_input("Support Email Address", value="support@edudash.com")
            st.button("Save Global Settings", type="primary")

def render_ai_recommendations():
    st.title("🤖 AI Recommendations")
    st.markdown("Personalized, ML-generated insights to optimize your learning path.")
    
    # Hero Recommendation Card
    st.subheader("🌟 Top Recommendation for You")
    with st.container(border=True):
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("### 📘 Course: Advanced Reading Comprehension")
            st.markdown("**Next Best Lesson:** Inferring Context from Complex Sentences")
            st.info("💡 **Why this recommendation?** Your recent Practice Quiz scores showed a 65% accuracy in Reading Comprehension, specifically struggling with context clues. This lesson directly targets that weakness.")
        with col2:
            st.metric("Predicted Success Rate", "88%", "+12%")
            st.metric("Confidence Score", "High (94%)")
            st.button("Start Lesson Now 🚀", type="primary", use_container_width=True)
            
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Secondary Insights
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("📉 Identified Weak Skills")
        with st.container(border=True):
            st.markdown("Our ML models have identified the following areas for improvement based on your historical performance:")
            st.error("- **Contextual Inference** (Current proficiency: 45%)")
            st.warning("- **Vocabulary Variation** (Current proficiency: 60%)")
            st.warning("- **Fraction Subtraction** (Current proficiency: 58%)")
            
    with c2:
        st.subheader("📅 Path Projections")
        with st.container(border=True):
            st.markdown("Based on your current learning velocity (avg. 4.5 hours/week):")
            st.success("**Estimated Course Completion:** October 12, 2026")
            st.info("**Next Assessment Due:** Friday, July 17, 2026")
            st.markdown("*Keep up the current pace to meet these targets!*")

def render_notifications():
    st.title("🔔 Notification Center")
    st.markdown("Stay up to date with your learning journey.")
    
    # Action bar
    col_filter, col_mark = st.columns([3, 1])
    with col_filter:
        notif_filter = st.selectbox("Filter Notifications", ["All", "Unread", "Alerts", "Messages", "Achievements"])
    with col_mark:
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("Mark all as read", use_container_width=True)
        
    st.markdown("---")
    
    # Notifications List
    st.subheader("Today")
    
    # Upcoming Lesson
    with st.container(border=True):
        st.markdown("📘 **Upcoming Lesson: Basic Mathematics**")
        st.write("Your live session 'Fractions & Decimals' starts in 45 minutes.")
        st.caption("30 minutes ago")
        
    # Assessment Reminder
    with st.container(border=True):
        st.error("⏰ **Assessment Reminder**")
        st.write("Don't forget to complete your 'Digital Literacy - Week 2' assessment by midnight.")
        st.caption("2 hours ago")
        
    # AI Recommendation
    with st.container(border=True):
        st.info("🤖 **New AI Recommendation**")
        st.write("Based on your recent scores, we recommend you review 'Contextual Inference' in the Reading course.")
        st.caption("4 hours ago")
        
    st.subheader("Earlier this week")
    
    # Achievement
    with st.container(border=True):
        st.success("🏆 **Achievement Unlocked!**")
        st.write("Congratulations! You earned the 'Perfect Quiz' badge.")
        st.caption("Yesterday")
        
    # Teacher Message
    with st.container(border=True):
        st.warning("👨‍🏫 **Message from Instructor Davis**")
        st.write("Great job on your essay submission! I've left some feedback for you in the grading portal.")
        st.caption("2 days ago")
        
    # Announcement
    with st.container(border=True):
        st.markdown("📢 **Platform Announcement**")
        st.write("The platform will undergo scheduled maintenance on Sunday from 2 AM to 4 AM EST.")
        st.caption("3 days ago")

def render_settings():
    st.title("⚙ User Settings")
    st.markdown("Manage your preferences, security, and accessibility options.")
    
    set_tabs = st.tabs(["Appearance & Accessibility", "Notifications", "Security", "Profile"])
    
    with set_tabs[0]:
        st.subheader("Appearance & Accessibility")
        st.selectbox("Theme", ["System Default", "Light Mode", "Dark Mode", "High Contrast"])
        st.selectbox("Language", ["English", "Spanish", "French", "Mandarin", "Hindi"])
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### Accessibility Options")
        st.toggle("Screen Reader Support", value=False)
        st.toggle("Large Text", value=True)
        st.toggle("Reduce Motion", value=False)
        st.button("Save Appearance Settings", type="primary")
        
    with set_tabs[1]:
        st.subheader("Notification Preferences")
        st.write("Choose what you want to be notified about.")
        with st.container(border=True):
            st.checkbox("Upcoming Lessons", value=True)
            st.checkbox("Assessment Reminders", value=True)
            st.checkbox("Achievements & Badges", value=True)
            st.checkbox("AI Recommendations", value=True)
            st.checkbox("Teacher Messages", value=True)
            st.checkbox("Marketing & Offers", value=False)
        st.button("Save Notifications", type="primary")
        
    with set_tabs[2]:
        st.subheader("Security")
        with st.container(border=True):
            st.text_input("Current Password", type="password")
            st.text_input("New Password", type="password")
            st.text_input("Confirm New Password", type="password")
            st.button("Update Password", type="primary")
        
        st.markdown("---")
        st.markdown("#### Danger Zone")
        st.button("Delete Account")
        
    with set_tabs[3]:
        st.subheader("Profile")
        st.info("You can update your personal information, education, and learning goals on the main Profile page.")
        if st.button("Go to Profile Page", type="primary"):
            st.success("Please click on '👤 Profile' in the sidebar menu.")

def render_logout():
    st.title("Logout")
    st.write("Are you sure you want to log out?")
    if st.button("Confirm Logout"):
        st.session_state['logged_in'] = False
        st.success("Logged out successfully.")

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
