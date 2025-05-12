import streamlit as st
import pyodbc
from db_utils import connect_db
import project_list
from pages import Project_details
from pages import resource_details
import add_project
import edit_project

# --- Basic Authentication (Keep this) ---
if "authentication_status" not in st.session_state:
    st.session_state["authentication_status"] = False
if "username" not in st.session_state:
    st.session_state["username"] = None
if "navigate_to_details" not in st.session_state:
        st.session_state["navigate_to_details"] = False
if "navigate_to_resource_details" not in st.session_state:
    st.session_state["navigate_to_resource_details"] = False

users = {
    "Comfort": "password123",  # Changed "pmo_admin" to "Comfort"
    "department_user": "password456",
}

if not st.session_state["authentication_status"]:
    st.sidebar.subheader("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    login_button = st.sidebar.button("Login")

    if login_button:
        if username in users and users[username] == password:
            st.session_state["authentication_status"] = True
            st.session_state["username"] = username
            st.rerun()
        else:
            st.sidebar.error("Invalid username or password")
else:
    st.sidebar.subheader(f"Welcome {st.session_state['username']}")
    logout_button = st.sidebar.button("Logout")
    if logout_button:
        st.session_state["authentication_status"] = False
        st.session_state["username"] = None
        st.rerun()

    # --- Navigation ---
    page_options = ["Project List", "Add Project", "Edit Project", "Project Details", "resource details"]
    if st.session_state.get('navigate_to_details'):
        index = page_options.index("Project Details")
        st.session_state['current_page'] = "Project Details"
        st.session_state['navigate_to_details'] = False
    elif st.session_state.get('navigate_to_resource_details'):
        index = page_options.index("resource details")
        st.session_state['current_page'] = "resource details"
        st.session_state['navigate_to_resource_details'] = False
    else:
        index = 0
        if 'current_page' in st.session_state and st.session_state['current_page'] in page_options:
            index = page_options.index(st.session_state['current_page'])
        st.session_state['current_page'] = st.sidebar.selectbox("Go to", page_options, index=index)

    # Apply the CSS styling here
    st.markdown(
        """
<style>
body {
    background-color: #663399; /* Purple background */
    color: #FFFFFF; /* White text */
}

.stButton>button {
    background-color: #FFFFFF; /* White button */
    color: #663399; /* Purple text */
    border: 2px solid #663399; /* Purple border */
    border-radius: 5px;
    padding: 10px 20px;
    font-size: 16px;
    cursor: pointer;
}

.stButton>button:hover {
    background-color: #f0f0f0; /* Slightly gray on hover */
}

h1 {
    color: #FFFFFF; /* White header */
    text-align: center;
}

/* Hide top navigation elements */
/* Target the sidebar directly and hide its first child */
div[data-testid="stSidebar"] > div:nth-child(1) {
    display: none !important;
}

</style>
""",
        unsafe_allow_html=True,
    )

    if st.session_state['current_page'] == "Project List":
        project_list.app()
    elif st.session_state['current_page'] == "Add Project" and st.session_state["username"] == "Comfort": #changed pmo_admin
        add_project.app()
    elif st.session_state['current_page'] == "Edit Project" and st.session_state["username"] == "Comfort": #changed pmo_admin
        edit_project.app()
    elif st.session_state['current_page'] == "Project Details":
        Project_details.app()
    elif st.session_state['current_page'] == "resource details":
        resource_details.app()
    else:
        st.warning("You do not have permission to access this page.")
