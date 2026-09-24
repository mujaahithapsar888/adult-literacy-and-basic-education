import os

with open('app_backup.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

def get_lines(start, end):
    return "".join(lines[start-1:end])

os.makedirs('utils', exist_ok=True)
os.makedirs('views', exist_ok=True)

# utils/styling.py
with open('utils/styling.py', 'w', encoding='utf-8') as f:
    f.write("import streamlit as st\n\n")
    f.write(get_lines(17, 74))

# views/home.py
with open('views/home.py', 'w', encoding='utf-8') as f:
    f.write("import streamlit as st\nimport pandas as pd\nimport plotly.express as px\n\n")
    f.write(get_lines(129, 202))

# views/profile.py
with open('views/profile.py', 'w', encoding='utf-8') as f:
    f.write("import streamlit as st\nfrom datetime import datetime\n\n")
    f.write(get_lines(203, 245))

# views/learning.py
with open('views/learning.py', 'w', encoding='utf-8') as f:
    f.write("import streamlit as st\nimport pandas as pd\nimport plotly.express as px\n\n")
    f.write(get_lines(246, 453))
    f.write("\n")
    f.write(get_lines(604, 715))

# views/ai_tools.py
with open('views/ai_tools.py', 'w', encoding='utf-8') as f:
    f.write("import streamlit as st\nimport time\nimport pandas as pd\nimport plotly.express as px\nimport plotly.graph_objects as go\n\n")
    f.write(get_lines(454, 603))
    f.write("\n")
    f.write(get_lines(1029, 1066))

# views/analytics.py
with open('views/analytics.py', 'w', encoding='utf-8') as f:
    f.write("import streamlit as st\nimport pandas as pd\nimport plotly.express as px\n\n")
    f.write(get_lines(716, 799))
    f.write("\n")
    f.write(get_lines(800, 864))

# views/admin.py
with open('views/admin.py', 'w', encoding='utf-8') as f:
    f.write("import streamlit as st\nimport pandas as pd\nimport plotly.express as px\n\n")
    f.write(get_lines(865, 945))
    f.write("\n")
    f.write(get_lines(946, 1028))

# views/settings.py
with open('views/settings.py', 'w', encoding='utf-8') as f:
    f.write("import streamlit as st\n\n")
    f.write(get_lines(1067, 1121)) # notifications
    f.write("\n")
    f.write(get_lines(1122, 1169)) # settings
    f.write("\n")
    f.write(get_lines(1170, 1176)) # logout

# Rewrite app.py
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(get_lines(1, 14))
    f.write("\n")
    f.write("from utils.styling import local_css\n")
    f.write("from views.home import render_home\n")
    f.write("from views.profile import render_profile\n")
    f.write("from views.learning import render_learning_dashboard, render_skill_assessment, render_personalized_learning_path, render_learning_modules, render_practice_quiz\n")
    f.write("from views.ai_tools import render_ai_tutor, render_writing_evaluation, render_ai_recommendations\n")
    f.write("from views.analytics import render_progress_analytics, render_certificates\n")
    f.write("from views.admin import render_teacher_dashboard, render_admin_dashboard\n")
    f.write("from views.settings import render_notifications, render_settings, render_logout\n\n")
    f.write(get_lines(74, 74)) # Call local_css()
    f.write(get_lines(76, 126))
    f.write("\n")
    f.write(get_lines(1177, 1219))
