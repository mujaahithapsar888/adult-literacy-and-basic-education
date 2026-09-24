import streamlit as st
import pandas as pd
import plotly.express as px

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

