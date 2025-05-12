import streamlit as st
import pyodbc
from db_utils import connect_db
import pandas as pd
import datetime

def app():
    st.title("Add New Project")

    project_name = st.text_input("Project Name:")
    project_description = st.text_area("Project Description:")

    project_status_options = ["In_Progress", "Completed", "Cancelled"]
    project_status = st.selectbox("Project Status:", project_status_options)

    project_type_options = ["Internal", "External"]
    project_type = st.selectbox("Project Type:", project_type_options)

    start_date = st.date_input("Start Date:")
    end_date = st.date_input("End Date:")

    risks = st.text_area("Initial Risks (Optional):")
    lessons_learned = st.text_area("Initial Lessons Learned (Optional):")

    conn = connect_db()
    resources_df = None
    if conn:
        try:
            resources_query = "SELECT ResourceID, ResourceName FROM dbo.Resources ORDER BY ResourceName;"
            resources_df = pd.read_sql(resources_query, conn)
            resource_options = resources_df['ResourceName'].tolist()
            selected_resources = st.multiselect("Assign Resources (Optional):", resource_options)
        except pyodbc.Error as ex:
            st.error(f"Database error fetching resources: {ex.args[0]}")
        finally:
            if conn:
                conn.close()
            conn = connect_db() # Re-establish connection for project/artifact insertion

    st.subheader("Artifacts (Optional)")
    artifacts = []
    num_artifacts = st.number_input("Number of Artifacts to Add:", min_value=0, max_value=10, value=0, step=1)

    for i in range(num_artifacts):
        cols = st.columns(2)
        artifact_name = cols[0].text_input(f"Artifact {i+1} Name:", key=f"artifact_name_{i}")
        artifact_link = cols[1].text_input(f"Artifact {i+1} Link (OneDrive URL):", key=f"artifact_link_{i}")
        if artifact_name or artifact_link:
            artifacts.append({"name": artifact_name, "link": artifact_link})

    if st.button("Add Project"):
        if not project_name:
            st.error("Project Name is required.")
            return
        if not project_type:
            st.error("Project Type is required.")
            return

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            project_id = None
            try:
                # Convert dates to Python datetime.date objects, handling potential issues
                start_date_py = None
                if start_date:
                    if isinstance(start_date, datetime.date):
                        start_date_py = start_date
                    else:
                        try:
                            start_date_py = start_date.to_pydatetime().date()
                        except AttributeError:
                            st.error("Invalid start date format.")
                            return

                end_date_py = None
                if end_date:
                    if isinstance(end_date, datetime.date):
                        end_date_py = end_date
                    else:
                        try:
                            end_date_py = end_date.to_pydatetime().date()
                        except AttributeError:
                            st.error("Invalid end date format.")
                            return

                # Insert the new project
                sql_project = """
                    INSERT INTO dbo.Projects (ProjectName, ProjectDescription, ProjectStatus, StartDate, EndDate, ProjectType, Risks, LessonsLearned)
                    OUTPUT inserted.ProjectID
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                """
                values_project = (project_name, project_description, project_status, start_date_py, end_date_py, project_type, risks, lessons_learned)
                cursor.execute(sql_project, values_project)
                row = cursor.fetchone()
                if row:
                    project_id = int(row[0])  # Explicitly convert ProjectID to int
                    conn.commit()
                    st.success(f"Project '{project_name}' added successfully with ID: {project_id}!")
                else:
                    conn.rollback()
                    st.error("Failed to retrieve Project ID after insertion.")
                    return

                # Assign selected resources to the project
                if project_id and selected_resources and resources_df is not None:
                    sql_assign_resource = """
                        INSERT INTO dbo.Project_Resource (ProjectID, ResourceID)
                        VALUES (?, ?);
                    """
                    for resource_name in selected_resources:
                        resource_row = resources_df[resources_df['ResourceName'] == resource_name].iloc[0]
                        resource_id = int(resource_row['ResourceID'])  # Explicitly convert ResourceID to int
                        cursor.execute(sql_assign_resource, (project_id, resource_id))
                    conn.commit()
                    st.success(f"Assigned resources: {', '.join(selected_resources)}")

                # Insert artifacts if provided
                if project_id and artifacts:
                    for artifact in artifacts:
                        if artifact["name"] and artifact["link"]:
                            sql_artifact = """
                                INSERT INTO dbo.Artifacts (ProjectID, ArtifactName, ArtifactLink)
                                VALUES (?, ?, ?);
                            """
                            values_artifact = (int(project_id), artifact["name"], artifact["link"])  # Explicitly convert ProjectID
                            cursor.execute(sql_artifact, values_artifact)
                            conn.commit()
                            st.success(f"Artifact '{artifact['name']}' added.")

            except pyodbc.Error as ex:
                sqlstate = ex.args[0]
                st.error(f"Database error: {sqlstate}")
                if conn:
                    conn.rollback()
            finally:
                if conn:
                    conn.close()
        else:
            st.error("Failed to connect to the database.")

if __name__ == "__main__":
    app()