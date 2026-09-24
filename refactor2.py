import os

# 1. Update frontend/app.py
with open(r'frontend/app.py', 'r', encoding='utf-8') as f:
    app_code = f.read()

app_code = app_code.replace('from views.', 'from pages.')
app_code = app_code.replace('from utils.styling', 'from styles.main')

# Replace the sidebar code with option_menu
import_option_menu = "from streamlit_option_menu import option_menu\n"
app_code = app_code.replace('import streamlit as st', 'import streamlit as st\n' + import_option_menu)

old_sidebar = """menu_options = {
    "Home": "🏠 Home",
    "Profile": "👤 Profile",
    "Learning Dashboard": "📚 Learning Dashboard",
    "Skill Assessment": "📝 Skill Assessment",
    "Personalized Learning Path": "🎯 Personalized Learning Path",
    "Learning Modules": "📖 Learning Modules",
    "AI Tutor": "🧠 AI Tutor",
    "Writing Evaluation": "✍ Writing Evaluation",
    "Practice Quiz": "📝 Practice Quiz",
    "AI Recommendations": "🤖 AI Recommendations",
    "Notifications": "🔔 Notifications",
    "Progress Analytics": "📈 Progress Analytics",
    "Certificates": "🏆 Certificates",
    "Teacher Dashboard": "👨‍🏫 Teacher Dashboard",
    "Admin Dashboard": "⚙ Admin Dashboard",
    "Settings": "⚙ User Settings",
    "Logout": "🚪 Logout"
}

selection = st.sidebar.radio("Navigation", list(menu_options.values()))"""

new_sidebar = """with st.sidebar:
    selection = option_menu(
        menu_title="Navigation",
        options=["Home", "Profile", "Learning Dashboard", "Skill Assessment", "Personalized Learning Path", "Learning Modules", "AI Tutor", "Writing Evaluation", "Practice Quiz", "AI Recommendations", "Notifications", "Progress Analytics", "Certificates", "Teacher Dashboard", "Admin Dashboard", "Settings", "Logout"],
        icons=["house", "person", "book", "pencil-square", "compass", "book-half", "robot", "pen", "check-circle", "lightbulb", "bell", "graph-up", "award", "person-workspace", "gear-wide-connected", "gear", "box-arrow-right"],
        menu_icon="cast",
        default_index=0,
    )"""

app_code = app_code.replace(old_sidebar, new_sidebar)

# The routing in app.py uses `menu_options["Home"]` etc. We need to just use the raw strings since selection returns the string from `options`.
app_code = app_code.replace('selection == menu_options["Home"]', 'selection == "Home"')
app_code = app_code.replace('selection == menu_options["Profile"]', 'selection == "Profile"')
app_code = app_code.replace('selection == menu_options["Learning Dashboard"]', 'selection == "Learning Dashboard"')
app_code = app_code.replace('selection == menu_options["Skill Assessment"]', 'selection == "Skill Assessment"')
app_code = app_code.replace('selection == menu_options["Personalized Learning Path"]', 'selection == "Personalized Learning Path"')
app_code = app_code.replace('selection == menu_options["Learning Modules"]', 'selection == "Learning Modules"')
app_code = app_code.replace('selection == menu_options["AI Tutor"]', 'selection == "AI Tutor"')
app_code = app_code.replace('selection == menu_options["Writing Evaluation"]', 'selection == "Writing Evaluation"')
app_code = app_code.replace('selection == menu_options["Practice Quiz"]', 'selection == "Practice Quiz"')
app_code = app_code.replace('selection == menu_options["AI Recommendations"]', 'selection == "AI Recommendations"')
app_code = app_code.replace('selection == menu_options["Notifications"]', 'selection == "Notifications"')
app_code = app_code.replace('selection == menu_options["Progress Analytics"]', 'selection == "Progress Analytics"')
app_code = app_code.replace('selection == menu_options["Certificates"]', 'selection == "Certificates"')
app_code = app_code.replace('selection == menu_options["Teacher Dashboard"]', 'selection == "Teacher Dashboard"')
app_code = app_code.replace('selection == menu_options["Admin Dashboard"]', 'selection == "Admin Dashboard"')
app_code = app_code.replace('selection == menu_options["Settings"]', 'selection == "Settings"')
app_code = app_code.replace('selection == menu_options["Logout"]', 'selection == "Logout"')

with open(r'frontend/app.py', 'w', encoding='utf-8') as f:
    f.write(app_code)

# 2. Update Teacher Dashboard to use aggrid
with open(r'frontend/pages/admin.py', 'r', encoding='utf-8') as f:
    admin_code = f.read()
    
admin_code = admin_code.replace("import streamlit as st\n", "import streamlit as st\nfrom st_aggrid import AgGrid, GridOptionsBuilder\n")
admin_code = admin_code.replace("st.dataframe(df_students.style.map(color_status, subset=['Status']), use_container_width=True, hide_index=True)", 
"""gb = GridOptionsBuilder.from_dataframe(df_students)
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_side_bar()
    gb.configure_selection('multiple', use_checkbox=True)
    gridOptions = gb.build()
    AgGrid(df_students, gridOptions=gridOptions, enable_enterprise_modules=True, width='100%', fit_columns_on_grid_load=True)""")

with open(r'frontend/pages/admin.py', 'w', encoding='utf-8') as f:
    f.write(admin_code)

# 3. Rename utils/styling.py to styles/main.py (or styles/main.css if refactoring deeper, but python string is fine)
os.rename(r'frontend/utils/styling.py', r'frontend/styles/main.py')

# 4. Create services/api.py
api_service = """import requests

# This represents the future connection to FastAPI
BASE_URL = "http://localhost:8000/api"

def fetch_student_data(student_id: str):
    # try:
    #     response = requests.get(f"{BASE_URL}/students/{student_id}")
    #     return response.json()
    # except Exception as e:
    #     print("API Error:", e)
    
    # Mock fallback for now until FastAPI is built
    return {
        "name": "Student User",
        "email": "student@edudash.com",
        "level": 12,
        "streak": 7
    }
"""
with open(r'frontend/services/api.py', 'w', encoding='utf-8') as f:
    f.write(api_service)
