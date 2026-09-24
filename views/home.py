import streamlit as st
import pandas as pd
import plotly.express as px

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

