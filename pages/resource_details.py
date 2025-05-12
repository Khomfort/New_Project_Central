import streamlit as st
import pandas as pd
import pyodbc
from db_utils import connect_db

def app(): # Define the app() function at the top level
    st.title("Resource Details")

    resource_id = st.session_state.get('selected_resource_id')
    st.write(f"Resource ID on Resource Details page: {resource_id}") # For debugging

    conn = connect_db()
    if conn:
        st.write("Database connection successful in resource_details!") # Debugging
        try:
            if resource_id:
                resource_query = f"""
                    SELECT * FROM Resources WHERE ResourceID = {resource_id}
                """
                resource_df = pd.read_sql(resource_query, conn)
                st.write(f"Resource DataFrame:") # Debugging
                st.write(resource_df) # Debugging

                if not resource_df.empty:
                    st.subheader(resource_df['ResourceName'].iloc[0])
                    for col in resource_df.columns:
                        st.write(f"{col}: {resource_df[col].iloc[0]}")

                    # --- Feedback Submission Form ---
                    st.subheader("Provide Feedback")
                    anonymous = st.checkbox("Submit Anonymously")
                    feedback_text = st.text_area("Your Feedback")
                    submit_button = st.button("Submit Feedback")

                    if submit_button:
                        submitted_by = None
                        if not anonymous:
                            submitted_by = st.session_state.get('username', 'Anonymous User')

                        if feedback_text:
                            cursor = conn.cursor()
                            insert_query = """
                                INSERT INTO ResourceFeedback (ResourceID, Anonymous, FeedbackText, SubmittedBy)
                                VALUES (?, ?, ?, ?)
                            """
                            cursor.execute(insert_query, resource_id, anonymous, feedback_text, submitted_by)
                            conn.commit()
                            st.success("Feedback submitted successfully!")
                        else:
                            st.warning("Please enter your feedback.")

                    # --- Display Existing Feedback ---
                    st.subheader("Existing Feedback")
                    feedback_query = f"""
                        SELECT * FROM ResourceFeedback WHERE ResourceID = {resource_id}
                    """
                    feedback_df = pd.read_sql(feedback_query, conn)
                    if not feedback_df.empty:
                        for index, row in feedback_df.iterrows():
                            st.markdown(f"**Feedback:** {row['FeedbackText']}")
                            if not row['Anonymous']:
                                st.markdown(f"*By: {row['SubmittedBy']} on {row['SubmissionDate']}*")
                            else:
                                st.markdown(f"*By: Anonymous on {row['SubmissionDate']}*")
                            st.divider()
                    else:
                        st.info("No feedback available for this resource yet.")

                else:
                    st.warning("Resource not found.")
            else:
                st.info("Please select a resource to view details.")

        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            st.error(f"Database error: {sqlstate}")
        finally:
            if conn:
                conn.close()
    else:
        st.error("Failed to connect to the database.")