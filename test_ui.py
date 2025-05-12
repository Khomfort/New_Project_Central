import streamlit as st
import pyodbc
import pandas as pd

# --- Database Connection ---
def connect_db():
    try:
        server = 'DESKTOP-842C8KP\\SQLEXPRESS'  # <---  **CHANGE THIS**
        database = "WIP_CentralDB"
        driver = '{ODBC Driver 17 for SQL Server}'
        conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        conn = pyodbc.connect(conn_str)
        return conn
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        st.error(f"Error connecting to SQL Server: {sqlstate}")
        return None

st.title("DB Connection Test")

conn = connect_db()

if conn:
    st.success("Successfully connected to the WIP_CentralDB database on SQL Server!")
    conn.close()
else:
    st.error("Failed to connect to the SQL Server database.")

# --- Main Streamlit App ---
st.title("Project Central")

conn = connect_db()

if conn:
    try:
        # Fetch full project data
        query = """
            SELECT
                p.ProjectID,
                p.ProjectName,
                p.StartDate,
                p.EndDate,
                p.ProjectStatus,
                p.ProjectDescription,
                p.LessonsLearned,
                p.Risks,
                p.ProjectType,
                a.ArtifactName,
                a.ArtifactLink,
                r.ResourceName  -- Include ResourceName
            FROM Projects p
            LEFT JOIN Artifacts a ON p.ProjectID = a.ProjectID
            LEFT JOIN Project_Resource pr ON p.ProjectID = pr.ProjectID
            LEFT JOIN Resources r ON pr.ResourceID = r.ResourceID
        """
        projects_df = pd.read_sql(query, conn)

        if not projects_df.empty:
            st.subheader("Select a Project")

            # --- Filter by Project Name ---
            project_name_filter = st.text_input("Filter by Project Name", "")
            filtered_projects_df = projects_df.copy()  # Create a copy to avoid modifying the original
            if project_name_filter:
                filtered_projects_df = filtered_projects_df[filtered_projects_df['ProjectName'].str.contains(project_name_filter, case=False)]

            # --- Filter by Keyword ---
            keyword_filter = st.text_input("Filter by Keyword", "")
            if keyword_filter:
                filter_condition = (
                    filtered_projects_df['ProjectName'].str.contains(keyword_filter, case=False) |
                    filtered_projects_df['ProjectDescription'].str.contains(keyword_filter, case=False) |
                    filtered_projects_df['LessonsLearned'].str.contains(keyword_filter, case=False) |
                    filtered_projects_df['Risks'].str.contains(keyword_filter, case=False)
                )
                filtered_projects_df = filtered_projects_df[filter_condition]

            # --- Filter by Resource Name ---
            resource_options = filtered_projects_df['ResourceName'].unique().tolist()  # Get unique resource names
            resource_name_filter = st.selectbox("Filter by Resource Name", ["All"] + resource_options)  # Add "All" option
            if resource_name_filter != "All" and 'ResourceName' in filtered_projects_df:  # Check if column exists
                filtered_projects_df = filtered_projects_df[filtered_projects_df['ResourceName'] == resource_name_filter]

            project_options = filtered_projects_df['ProjectName'].unique().tolist()
            selected_project = st.selectbox("Choose a project", project_options)

            # Filter data for selected project (from the original DataFrame)
            selected_data = projects_df[projects_df['ProjectName'] == selected_project]

            st.subheader("Project Details")

            # Display Project Details
            if not selected_data.empty:
                st.markdown(f"**Project Name:** {selected_data['ProjectName'].iloc[0]}")
                st.markdown(f"**Start Date:** {selected_data['StartDate'].iloc[0]}")
                st.markdown(f"**End Date:** {selected_data['EndDate'].iloc[0]}")
                st.markdown(f"**Status:** {selected_data['ProjectStatus'].iloc[0]}")
                st.markdown(f"**Type:** {selected_data['ProjectType'].iloc[0]}")
                st.markdown(f"**Description:** {selected_data['ProjectDescription'].iloc[0]}")
                st.markdown(f"**Risks:** {selected_data['Risks'].iloc[0]}")
                st.markdown(f"**Lessons Learned:** {selected_data['LessonsLearned'].iloc[0]}")

                # Display Artifacts
                st.subheader("Project Artifacts")
                if not selected_data.empty and 'ArtifactName' in selected_data.columns and 'ArtifactLink' in selected_data.columns:
                    for index, row in selected_data.iterrows():
                        if row['ArtifactName'] and row['ArtifactLink']:
                            st.markdown(f"- **{row['ArtifactName']}:** [{row['ArtifactLink']}]({row['ArtifactLink']})")
                else:
                    st.info("No artifacts found for this project.")
            else:
                st.info("No details to display for the selected project.")

        else:
            st.warning("No projects found in the database.")

    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        st.error(f"Error executing SQL query: {sqlstate}")

    finally:
        if conn:
            conn.close()
else:
    st.error("Failed to connect to the SQL Server database. Please check your connection details.")