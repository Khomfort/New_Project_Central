import streamlit as st
import pandas as pd
import pyodbc
from db_utils import connect_db
import base64

def app():
    st.title("Project List")

    st.markdown("""
        <style>
        .view-details-button {
            background-color: #4CAF50; /* Green background */
            border: none;
            color: white;
            padding: 8px 12px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 14px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 5px;
        }
        </style>
    """, unsafe_allow_html=True)

    search_term = st.text_input("Search Projects by Name", "")

    conn = connect_db()
    if conn:
        try:
            query = """
                SELECT
                    p.ProjectID,
                    p.ProjectName,
                    p.ProjectStatus
                FROM
                    dbo.Projects p
            """
            projects_df = pd.read_sql(query, conn)

            filtered_projects_df = projects_df.copy()
            if search_term:
                filtered_projects_df = filtered_projects_df[
                    (filtered_projects_df['ProjectName'].str.contains(search_term, case=False))
                ].reset_index(drop=True)

            for index, row in filtered_projects_df.iterrows():
                col1, col2, col3, col4 = st.columns([1, 4, 2, 2]) # Adjust columns
                with col1:
                    st.write(row['ProjectID'])
                with col2:
                    st.write(row['ProjectName'])
                with col3:
                    st.write(row['ProjectStatus'])
                with col4:
                    if st.button(f"View Project Details", key=f"view_project_details_{index}"):
                        st.session_state['selected_project'] = row['ProjectName']
                        st.session_state['navigate_to_details'] = True
                        st.rerun()

        except pyodbc.Error as ex:
            st.error(f"Database error: {ex.args[0]}")
        finally:
            conn.close()
    else:
        st.error("Failed to connect to the database.")

if __name__ == "__main__":
    app()