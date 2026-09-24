import streamlit as st

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

