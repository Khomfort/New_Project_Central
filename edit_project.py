import streamlit as st
import pyodbc
from db_utils import connect_db
import pandas as pd
import datetime

def app():
    st.title("Edit / Delete Project")

    conn = connect_db()
    if conn:
        try:
            # --- Fetch all available resources ---
            all_resources_query = "SELECT ResourceID, ResourceName FROM dbo.Resources ORDER BY ResourceName;"
            all_resources_df = pd.read_sql(all_resources_query, conn)
            all_resource_options = all_resources_df['ResourceName'].tolist()
            resource_id_to_name = all_resources_df.set_index('ResourceID')['ResourceName'].to_dict()
            name_to_resource_id = {v: k for k, v in resource_id_to_name.items()}

            # --- Fetch all project names ---
            query = "SELECT ProjectName FROM dbo.Projects ORDER BY ProjectName;"
            projects_df = pd.read_sql(query, conn)
            project_names = projects_df['ProjectName'].tolist()
            selected_project_name = st.selectbox("Select Project to Edit/Delete:", [""] + project_names)

            if selected_project_name:
                # --- Fetch project details ---
                project_details_query = f"""
                    SELECT ProjectID, ProjectName, ProjectDescription, ProjectStatus, StartDate, EndDate, Risks, LessonsLearned, ProjectType
                    FROM dbo.Projects
                    WHERE ProjectName = '{selected_project_name}';
                """
                project_data_df = pd.read_sql(project_details_query, conn)

                if not project_data_df.empty:
                    project_data = project_data_df.iloc[0]
                    project_id = project_data['ProjectID']
                    project_name = st.text_input("Project Name:", project_data['ProjectName'])
                    project_description = st.text_area("Project Description:", project_data['ProjectDescription'])

                    project_status_options = ["In_Progress", "Completed", "Cancelled"]
                    default_status_index = 0
                    if project_data['ProjectStatus'] == "In_Progress":
                        default_status_index = project_status_options.index("In_Progress")
                    elif project_data['ProjectStatus'] == "Completed":
                        default_status_index = project_status_options.index("Completed")
                    elif project_data['ProjectStatus'] == "Cancelled":
                        default_status_index = project_status_options.index("Cancelled")
                    project_status = st.selectbox("Project Status:", project_status_options, index=default_status_index)

                    project_type_options = ["Internal", "External"]
                    default_type_index = 0
                    if project_data['ProjectType'] in project_type_options:
                        default_type_index = project_type_options.index(project_data['ProjectType'])
                    project_type = st.selectbox("Project Type:", project_type_options, index=default_type_index)

                    start_date = st.date_input("Start Date:", project_data['StartDate'])
                    end_date = st.date_input("End Date:", project_data['EndDate'])
                    risks = st.text_area("Risks:", project_data['Risks'])
                    lessons_learned = st.text_area("Lessons Learned:", project_data['LessonsLearned'])

                    # --- Fetch currently assigned resources for the project ---
                    assigned_resources_query = f"""
                        SELECT pr.ResourceID
                        FROM dbo.Project_Resource pr
                        WHERE pr.ProjectID = {project_id};
                    """
                    assigned_resources_df = pd.read_sql(assigned_resources_query, conn)
                    assigned_resource_names = [resource_id_to_name.get(res_id) for res_id in assigned_resources_df['ResourceID'].tolist() if resource_id_to_name.get(res_id)]

                    selected_resources_edit = st.multiselect("Edit Assigned Resources:", all_resource_options, default=assigned_resource_names)

                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("About to check Update Project button!")  # Debugging
                        if st.button("Update Project"):
                            st.write("Update Project button was definitely clicked!")  # Debugging
                            # --- Logic to update project details (existing) ---
                            update_query = f"""
                                UPDATE dbo.Projects
                                SET ProjectName = ?,
                                    ProjectDescription = ?,
                                    ProjectStatus = ?,
                                    StartDate = ?,
                                    EndDate = ?,
                                    Risks = ?,
                                    LessonsLearned = ?,
                                    ProjectType = ?
                                WHERE ProjectID = ?;
                            """
                            # Explicitly convert project_id to a Python integer
                            project_id_py = int(project_id)
                            update_values = (project_name, project_description, project_status, start_date, end_date, risks, lessons_learned, project_type, project_id_py)

                            st.write("Update Query:", update_query)  # Debugging
                            st.write("Update Values:", update_values)  # Debugging

                            try:
                                with connect_db() as conn:  # Use 'with' for connection management
                                    with conn.cursor() as cursor:  # Use 'with' for cursor management
                                        cursor.execute(update_query, update_values)
                                        conn.commit()
                                        st.success(f"Project '{project_name}' updated successfully (resource update not yet implemented)!")
                            except pyodbc.Error as ex:
                                sqlstate = ex.args[0]
                                st.error(f"Database error during update: {sqlstate}")
                                if conn:
                                    conn.rollback()

                            st.rerun() # Refresh the page to see updated data

                    with col2:
                        with st.expander("Confirm Delete"):
                            st.warning(f"Are you sure you want to permanently delete project '{project_name}'?", icon="⚠️")
                            col_confirm, col_cancel = st.columns(2)
                            with col_confirm:
                                if st.button("Yes, Delete", key=f"delete_confirm_{project_id}"):
                                    delete_query = f"""
                                        DELETE FROM dbo.Projects WHERE ProjectID = ?;
                                    """
                                    cursor = conn.cursor()
                                    project_id_py = int(project_id)
                                    cursor.execute(delete_query, (project_id_py,))
                                    conn.commit()
                                    st.success(f"Project '{project_name}' deleted successfully!")
                                    st.session_state['selected_project'] = None # Clear selection
                                    st.session_state['navigate_to_details'] = False
                                    st.rerun() # Refresh to update the project list
                            with col_cancel:
                                if st.button("Cancel", key=f"delete_cancel_{project_id}"):
                                    st.info("Delete operation cancelled.")

                else:
                    st.warning("Could not retrieve project details.")

        except pyodbc.Error as ex:
            st.error(f"Database error: {ex.args[0]}")
        finally:
            if conn:
                conn.close()
    else:
        st.error("Failed to connect to the database.")

if __name__ == "__main__":
    app()