import streamlit as st

def local_css():
    st.markdown("""
        <style>
        /* Modern aesthetic colors and styling */
        :root {
            --primary-color: #4361ee;
            --secondary-color: #3f37c9;
            --background-color: #f8f9fa;
            --text-color: #2b2d42;
            --card-bg: #ffffff;
        }
        
        [data-theme="dark"] {
            --background-color: #121212;
            --text-color: #e0e0e0;
            --card-bg: #1e1e1e;
        }

        /* Metric Cards */
        div.css-1r6slb0.e1tzin5v2 {
            background-color: var(--card-bg);
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        div.css-1r6slb0.e1tzin5v2:hover {
            transform: translateY(-5px);
        }

        /* Top Bar Styling */
        .top-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid #ddd;
            margin-bottom: 20px;
        }
        
        /* Footer */
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: var(--card-bg);
            color: var(--text-color);
            text-align: center;
            padding: 10px;
            font-size: 14px;
            border-top: 1px solid #ddd;
            z-index: 999;
        }
        </style>
    """, unsafe_allow_html=True)

local_css()
