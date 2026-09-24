import streamlit as st
import time

def render_login():
    # Inject custom CSS for the login page
    st.markdown("""
        <style>
        /* Gradient background for the whole page */
        .stApp {
            background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
        }
        
        [data-theme="dark"] .stApp {
            background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
        }

        /* Glassmorphism card for the login form */
        div[data-testid="stForm"] {
            background: rgba(20, 20, 20, 0.8);
            border-radius: 16px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 2rem;
        }
        
        [data-theme="dark"] div[data-testid="stForm"] {
            background: rgba(20, 20, 20, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        /* Header styling */
        .login-header {
            text-align: center;
            font-family: 'Inter', sans-serif;
            font-weight: 700;
            color: #fff;
            margin-bottom: 0.5rem;
        }

        .login-subtitle {
            text-align: center;
            color: #dbe4ee;
            margin-bottom: 2rem;
        }
        
        /* Make tabs visible over the dark background */
        div[data-baseweb="tab-list"] button {
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Empty columns to center the login form
    col1, col2, col3 = st.columns([1.5, 2, 1.5])
    
    with col2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("<h1 class='login-header'>🎓 Welcome to EduDash</h1>", unsafe_allow_html=True)
        st.markdown("<p class='login-subtitle'>Professional Learning Platform</p>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Sign In", "Create Account"])
        
        with tab1:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🌐 Continue with Google", key="google_login", use_container_width=True):
                st.session_state['logged_in'] = True
                st.session_state['username'] = "Google User"
                st.session_state['role'] = "student"
                st.success("Google Login successful! Redirecting...")
                time.sleep(0.5)
                st.rerun()
                
            st.markdown("<p style='text-align: center; color: #888; font-size: 0.9em; margin: 10px 0;'>────── OR ──────</p>", unsafe_allow_html=True)
            
            with st.form("login_form", clear_on_submit=False):
                st.markdown("### Sign In with Email")
                username = st.text_input("Username", placeholder="Enter your username")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                submit_button = st.form_submit_button("Login", use_container_width=True)
                
                if submit_button:
                    users_db = st.session_state.get('users_db', {})
                    if username in users_db and users_db[username]['password'] == password:
                        st.session_state['logged_in'] = True
                        st.session_state['username'] = users_db[username]['name']
                        st.session_state['role'] = users_db[username]['role']
                        st.success("Login successful! Redirecting...")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                        
        with tab2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🌐 Sign up with Google", key="google_signup", use_container_width=True):
                st.session_state['logged_in'] = True
                st.session_state['username'] = "Google User"
                st.session_state['role'] = "student"
                st.success("Google Sign-Up successful! Redirecting...")
                time.sleep(0.5)
                st.rerun()
                
            st.markdown("<p style='text-align: center; color: #888; font-size: 0.9em; margin: 10px 0;'>────── OR ──────</p>", unsafe_allow_html=True)
            
            with st.form("signup_form", clear_on_submit=True):
                st.markdown("### Create an Account with Email")
                new_name = st.text_input("Full Name")
                new_username = st.text_input("Username")
                new_password = st.text_input("Password", type="password")
                role_choice = st.selectbox("Role", ["Student", "Admin"])
                signup_button = st.form_submit_button("Sign Up", use_container_width=True)
                
                if signup_button:
                    if not new_name or not new_username or not new_password:
                        st.error("Please fill in all fields.")
                    elif new_username in st.session_state['users_db']:
                        st.error("Username already exists. Please choose another one.")
                    else:
                        st.session_state['users_db'][new_username] = {
                            'password': new_password,
                            'role': role_choice.lower(),
                            'name': new_name
                        }
                        st.success(f"Account created successfully for {new_username}! You can now sign in.")
