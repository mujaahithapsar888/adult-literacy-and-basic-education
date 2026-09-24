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
