from services.api import start_assessment, submit_assessment
import streamlit as st
import pandas as pd
import plotly.express as px

def render_learning_dashboard():
    st.title("Learning Dashboard")
    st.progress(65, text="Overall Progress - 65%")
    st.subheader("Current Modules")
    st.write("- Introduction to Machine Learning (In Progress - 40%)")
    st.write("- Data Visualization (Completed)")

def render_skill_assessment():
    st.title("📝 Skill Assessment")
    
    if 'assessment_state' not in st.session_state:
        st.session_state['assessment_state'] = 'selection'
    if 'assessment_id' not in st.session_state:
        st.session_state['assessment_id'] = None
    if 'assessment_result' not in st.session_state:
        st.session_state['assessment_result'] = None
    
    if st.session_state['assessment_state'] == 'selection':
        st.subheader("Select Assessment Category")
        col1, col2 = st.columns(2)
        with col1:
            category = st.selectbox("Category", ["Reading", "Writing", "Mathematics", "English", "Digital Literacy", "Life Skills"])
        with col2:
            difficulty = st.selectbox("Difficulty Level", ["Beginner", "Intermediate", "Advanced"])
            
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Start Assessment", type="primary"):
            with st.spinner("Starting assessment..."):
                res = start_assessment(category, difficulty)
                if "error" in res:
                    st.error("Error connecting to backend: " + res["error"])
                else:
                    st.session_state['assessment_id'] = res.get("assessment_id", 101)
                    st.session_state['assessment_state'] = 'taking'
                    st.rerun()
            
    elif st.session_state['assessment_state'] == 'taking':
        c1, c2 = st.columns([3, 1])
        c1.subheader("Question 1 of 10")
        c2.info("⏱ Time Remaining: 14:23")
        
        st.progress(10, text="Progress: 10%")
        st.markdown("---")
        st.markdown("### Which of the following is the correct answer?")
        
        ans = st.radio("Select your answer:", [
            "Option A: Correct answer here.",
            "Option B: Incorrect answer.",
            "Option C: Another incorrect answer.",
            "Option D: None of the above."
        ], index=None)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        nav1, nav2, nav3 = st.columns([1, 6, 3])
        nav1.button("⬅ Previous")
        if nav3.button("Submit Assessment ✅", type="primary"):
            if not ans:
                st.warning("Please select an answer.")
            else:
                with st.spinner("Grading..."):
                    # Send submission to backend
                    answers = {"q1": ans}
                    res = submit_assessment(st.session_state['assessment_id'], answers)
                    if "error" in res:
                        st.error("Error: " + res["error"])
                    else:
                        st.session_state['assessment_result'] = res
                        st.session_state['assessment_state'] = 'results'
                        st.rerun()
            
    elif st.session_state['assessment_state'] == 'results':
        st.subheader("📊 Assessment Results")
        result = st.session_state['assessment_result']
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Score", f"{result['score']}%")
        c2.metric("Status", "Passed" if result['passed'] else "Needs Practice")
        c3.metric("Feedback", result['feedback'])
        
        st.markdown("---")
        
        # Radar Chart
        categories = ['Reading', 'Writing', 'Mathematics', 'English', 'Digital Literacy', 'Life Skills']
        # Mock varied scores for visualization
        scores = [result['score'], 82, 65, 80, 90, 85]
        
        df_radar = pd.DataFrame(dict(Score=scores, Skill=categories))
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

