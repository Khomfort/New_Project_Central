import streamlit as st
import pandas as pd
import pyodbc
from db_utils import connect_db

def app():
    st.title("Project Details")

    selected_project_name = st.session_state.get('selected_project')
    st.write(f"Selected Project: {selected_project_name}") # Debugging

    conn = connect_db()
    if conn:
        try:
            if selected_project_name:
                # --- Fetch Project Details ---
                project_query = f"""
                    SELECT * FROM Projects WHERE ProjectName = '{selected_project_name}'
                """
                details_df = pd.read_sql(project_query, conn)

                if not details_df.empty:
                    st.subheader("Project Information")
                    for col in details_df.columns:
                        st.write(f"{col}: {details_df[col].iloc[0]}")

                    # --- Fetch Project Resources ---
                    project_id = details_df['ProjectID'].iloc[0]
                    resources_query = f"""
                        SELECT r.ResourceID, r.ResourceName
                        FROM dbo.Project_Resource AS pr
                        INNER JOIN dbo.Resources AS r ON pr.ResourceID = r.ResourceID
                        WHERE pr.ProjectID = {project_id}
                    """
                    resources_df = pd.read_sql(resources_query, conn)

                    if not resources_df.empty:
                        st.subheader("Project Resources")
                        for index, row in resources_df.iterrows():
                            col1, col2 = st.columns([1, 2])
                            with col1:
                                st.write(row['ResourceName'])
                            with col2:
                                if st.button(f"View Resource", key=f"view_resource_{row['ResourceID']}"):
                                    st.session_state['selected_resource_id'] = row['ResourceID']
                                    st.session_state['navigate_to_resource_details'] = True
                                    st.rerun()
                    else:
                        st.info("No resources assigned to this project.")

                    # --- Fetch Project Artifacts (Keep this section) ---
                    artifacts_query = f"""
                        SELECT ArtifactName, ArtifactLink
                        FROM Artifacts
                        WHERE ProjectID = {project_id}
                    """
                    artifacts_df = pd.read_sql(artifacts_query, conn)
                    if not artifacts_df.empty:
                        st.subheader("Project Artifacts")
                        for index, row in artifacts_df.iterrows():
                            artifact_name = row['ArtifactName']
                            artifact_link = row['ArtifactLink']
                            st.link_button(label=artifact_name, url=artifact_link)
                    else:
                        st.info("No artifacts found for this project.")

                else:
                    st.warning(f"No details found for project: {selected_project_name}")
            else:
                st.info("Please select a project from the Project List.")

        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            st.error(f"Database error: {sqlstate}")
        finally:
            if conn:
                conn.close()
    else:
        st.error("Failed to connect to the database.")