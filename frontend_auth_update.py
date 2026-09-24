import os

def rewrite(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

# 1. Update frontend/services/api.py
rewrite("frontend/services/api.py", """
import requests

BASE_URL = "http://localhost:8000"

def login(email, password):
    # FastAPI OAuth2PasswordRequestForm expects form data
    try:
        response = requests.post(f"{BASE_URL}/auth/login", data={"username": email, "password": password})
        if response.status_code == 200:
            return response.json() # contains access_token, refresh_token
        return {"error": response.json().get("detail", "Login failed")}
    except Exception as e:
        return {"error": str(e)}

def register(email, password, role="Student"):
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json={"email": email, "password": password, "role": role})
        if response.status_code == 200:
            return response.json()
        return {"error": response.json().get("detail", "Registration failed")}
    except Exception as e:
        return {"error": str(e)}

def forgot_password(email):
    try:
        response = requests.post(f"{BASE_URL}/auth/forgot-password", json={"email": email})
        if response.status_code == 200:
            return response.json()
        return {"error": response.json().get("detail", "Failed")}
    except Exception as e:
        return {"error": str(e)}

def fetch_student_data(student_id: str):
    return {
        "name": "Student User",
        "email": "student@edudash.com",
        "level": 12,
        "streak": 7
    }
""")

# 2. Create frontend/pages/auth_page.py
rewrite("frontend/pages/auth_page.py", """
import streamlit as st
from services.api import login, register, forgot_password

def render_auth_gateway():
    st.markdown("<h1 style='text-align: center; color: var(--primary-color);'>🎓 EduDash</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #888;'>AI-Powered Personalized Learning</h3>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.container(border=True):
            tabs = st.tabs(["🔒 Login", "📝 Register", "🔑 Forgot Password"])
            
            with tabs[0]:
                st.subheader("Welcome Back")
                login_email = st.text_input("Email", key="login_email")
                login_pass = st.text_input("Password", type="password", key="login_pass")
                if st.button("Login", type="primary", use_container_width=True):
                    if not login_email or not login_pass:
                        st.error("Please fill in all fields")
                    else:
                        with st.spinner("Authenticating..."):
                            res = login(login_email, login_pass)
                            if "error" in res:
                                st.error(res["error"])
                            else:
                                st.session_state['logged_in'] = True
                                st.session_state['access_token'] = res["access_token"]
                                st.session_state['refresh_token'] = res["refresh_token"]
                                st.session_state['username'] = login_email.split('@')[0].capitalize()
                                st.success("Login successful!")
                                st.rerun()
                                
            with tabs[1]:
                st.subheader("Create an Account")
                reg_email = st.text_input("Email", key="reg_email")
                reg_pass = st.text_input("Password", type="password", key="reg_pass")
                reg_role = st.selectbox("Role", ["Student", "Teacher"], key="reg_role")
                if st.button("Register", type="primary", use_container_width=True):
                    if not reg_email or not reg_pass:
                        st.error("Please fill in all fields")
                    else:
                        with st.spinner("Registering..."):
                            res = register(reg_email, reg_pass, reg_role)
                            if "error" in res:
                                st.error(res["error"])
                            else:
                                st.success("Account created successfully! Please login in the previous tab.")
                                
            with tabs[2]:
                st.subheader("Reset Password")
                forgot_email = st.text_input("Email to send reset link", key="forgot_email")
                if st.button("Send Reset Link", type="primary", use_container_width=True):
                    if not forgot_email:
                        st.error("Please provide an email")
                    else:
                        with st.spinner("Sending link..."):
                            res = forgot_password(forgot_email)
                            if "error" in res:
                                st.error(res["error"])
                            else:
                                st.success(res["msg"])
""")

# 3. Update frontend/app.py to use auth page
with open("frontend/app.py", "r", encoding="utf-8") as f:
    app_code = f.read()

# Replace the session state initialization
old_session = """# --- Session State Management ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = True
if 'username' not in st.session_state:
    st.session_state['username'] = 'Student User'
if 'notifications' not in st.session_state:
    st.session_state['notifications'] = 3"""

new_session = """from pages.auth_page import render_auth_gateway

# --- Session State Management ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ''
if 'notifications' not in st.session_state:
    st.session_state['notifications'] = 3
if 'access_token' not in st.session_state:
    st.session_state['access_token'] = None
"""
app_code = app_code.replace(old_session, new_session)

# Wrap the rest in a check for logged_in
app_code = app_code.replace("# --- Sidebar Navigation ---", """# --- Auth Gateway ---
if not st.session_state['logged_in']:
    render_auth_gateway()
else:
    # --- Sidebar Navigation ---""")

app_code = app_code.replace('selection == "Logout":\n    render_logout()', """selection == "Logout":
        st.session_state['logged_in'] = False
        st.session_state['access_token'] = None
        st.session_state['username'] = ''
        st.rerun()""")

# We need to indent everything under the else statement. This is a bit tricky with string replacement.
# Let's write a small logic to indent from "# --- Sidebar Navigation ---" onwards.
lines = app_code.split("\n")
new_lines = []
indenting = False
for line in lines:
    if line == "    # --- Sidebar Navigation ---":
        indenting = True
    
    if indenting and line != "    # --- Sidebar Navigation ---":
        new_lines.append("    " + line)
    else:
        new_lines.append(line)

with open("frontend/app.py", "w", encoding="utf-8") as f:
    f.write("\n".join(new_lines))
