import streamlit as st
from datetime import datetime

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

