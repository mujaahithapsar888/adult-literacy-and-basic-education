import streamlit as st
import pandas as pd
import plotly.express as px

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

