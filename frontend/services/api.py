import requests
import streamlit as st

BASE_URL = "http://localhost:8000"

def get_headers():
    token = st.session_state.get('access_token')
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}

def login(email, password):
    try:
        response = requests.post(f"{BASE_URL}/auth/login", data={"username": email, "password": password})
        if response.status_code == 200:
            return response.json()
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

def start_assessment(category, difficulty):
    try:
        res = requests.post(f"{BASE_URL}/assessment/start", params={"category": category, "difficulty": difficulty}, headers=get_headers())
        if res.status_code == 200:
            return res.json()
        return {"error": res.text}
    except Exception as e:
        return {"error": str(e)}

def submit_assessment(assessment_id, answers):
    try:
        res = requests.post(
            f"{BASE_URL}/assessment/submit", 
            json={"assessment_id": assessment_id, "answers": answers}, 
            headers=get_headers()
        )
        if res.status_code == 200:
            return res.json()
        return {"error": res.text}
    except Exception as e:
        return {"error": str(e)}
