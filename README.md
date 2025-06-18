# New_Project_Central💼
## Description and Overview
Project Central serves as a streamlined and accessible hub for all ongoing projects within the company, providing a centralized view of their status and key information. Recognizing the challenges of scattered project details across various platforms and communication channels, this project aimed to create a single source of truth for project oversight and collaboration. Built using the robust capabilities of SQL for database management, the analytical power of Python for data processing, and the user-friendly interface of Streamlit for visualization, Project Central offers an intuitive way to track progress, access essential documents, and gain insights into the company's project portfolio.
## Key Features🕵️‍♂️

* **Centralized Project Repository:** Provides a single location to view all active, upcoming, and completed company projects.
* **Project Status Tracking:** Allows users to easily see the current status (e.g., In Progress, On Hold, Completed) of each project.
* **Document Management:** Enables the uploading and accessing of key project documents (e.g., briefs, plans, reports) directly within the platform.
* **Task Management Integration (Potentially):** If you integrated task management, you might have features for creating, assigning, and tracking individual tasks within projects.
* **Progress Visualization:** Offers visual representations of project progress, potentially through charts or dashboards built with Streamlit.
* **Search and Filtering:** Allows users to quickly find specific projects based on keywords, status, department, or other relevant criteria.
* **User Roles and Permissions (Potentially):** If you implemented user roles, you might have features for controlling access to project information based on user roles (e.g., Admin, Project Manager, Team Member).
* **Data Insights and Reporting:** Provides reports or summaries of the overall project portfolio, potentially highlighting key metrics or potential risks.
* **Real-time Updates (Potentially):** If you implemented real-time features, users might see immediate updates on project status or document changes.
* **Team Collaboration Features (Potentially):** Depending on the scope, you might have features for communication or collaboration within project pages.
  ## Technologies Used👩‍💻

* **Programming Language:** Python
* **Libraries:**
    * Pandas (for data manipulation and analysis)
    * SQLAlchemy (for interacting with the database)
    * Streamlit (for creating the web user interface)
* **Database:** Azure SQL Database
* **Other Tools:**
    * Azure Portal (for managing the Azure SQL Database)
    * IDE (VS Code)
## Setup/Installation👩‍🔧
1.  **Clone the repository:**
    ```bash
    git clone [(https://github.com/Khomfort/New_Project_Central.git)]
    ```

2.  **Navigate to the project directory:**
    ```bash
    cd project-central
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Ensure you have a `requirements.txt` file in your repository that lists the necessary Python libraries: `pandas`, `sqlalchemy`, `streamlit`, and potentially `pyodbc` or `mssql-cli` for connecting to Azure SQL.)*

4.  **Configure Azure SQL Database Connection:**
    * You will need an active Azure subscription and an Azure SQL Database instance.
    * **Obtain the connection details:** This includes the server name, database name, username, and password for your Azure SQL Database.
    * **Set up environment variables (recommended):** For security, it's best to store your database credentials as environment variables. You might need to create a `.env` file (and ensure it's not committed to Git) or configure environment variables directly in your operating system or deployment environment.
        ```
        DATABASE_SERVER=your_server.database.windows.net
        DATABASE_NAME=your_database_name
        DATABASE_USER=your_username
        DATABASE_PASSWORD=your_password
        ```
    * **Alternatively (less secure for public repositories):** You might configure the connection string directly in your Python code, but this is generally discouraged for sensitive information.

5.  **Run the Streamlit application:**
    ```bash
    streamlit run main.py
    ```
## Usage👩‍🔬

1.  **Access the Application:**
    * Open your web browser and navigate to the URL where the Project Central application is running.
      
2.  **Login:**
    * If required, you will be prompted to log in with your company credentials. Enter your username and password.
      
3.  **Project Overview:**
    * Upon accessing the application, you will see a central dashboard or project listing page displaying all active projects.
    * You can browse through the projects to get a quick overview of their status and key information.

4.  **Viewing Project Details:**
    * Click on a specific project from the overview page to view its detailed information. This page might include:
        * The project's current status.
        * Key documents related to the project.
        * Any available progress visualizations or reports.

5.  **Searching and Filtering Projects:**
    * Use the search bar (if implemented) to look for projects by project name or resource name.
    * Utilize the filtering options (if available) to narrow down the project list based on criteria like status, department, or date.

6.  **Document Access:**
    * Within a project's detail page, locate the section for documents. You should be able to:
        * View a list of uploaded documents.
        * Click on a document to open or download it.

* Consider adding a few screenshots showing the main screens of your application (e.g., the project overview page, a project detail page, a sample report or visualization). This will make the usage instructions much clearer. You can use Markdown to embed images: `![Screenshot of Project Overview](path/to/overview_screenshot.png)`
## Challenges and Learnings🥂

During the development of Project Central, I encountered several key challenges:

* **Establishing a Robust Connection to Azure SQL Database:** Initially, configuring the connection between the Python application (using SQLAlchemy) and the Azure SQL Database required careful attention to connection strings, driver compatibility (potentially `pyodbc`), and ensuring proper authentication. I overcame this by thoroughly reviewing the documentation for both SQLAlchemy and Azure SQL, and by implementing robust error handling for connection failures. This process significantly improved my understanding of **cloud database connectivity and connection pooling**.

* **Designing an Efficient Database Schema for Diverse Project Data:** Creating a flexible database schema that could accommodate the varying information and document types associated with different company projects proved challenging. I addressed this by employing relational database design principles, carefully defining entities and their relationships, and iteratively refining the schema based on evolving project requirements. This deepened my knowledge of **database normalization and data modeling for complex applications**.

* **Implementing Effective Search and Filtering in Streamlit:** As the number of projects grew, providing users with efficient ways to find specific information became crucial. Implementing the search and filtering functionalities in Streamlit required careful consideration of how to query the backend database based on user input and display the results dynamically. I learned a lot about **integrating frontend user interactions with backend database queries and state management in Streamlit**.

* **Presenting Complex Project Data in a User-Friendly Way with Streamlit:** Displaying detailed project information, including status, documents, and potential visualizations, within the Streamlit interface required careful UI/UX design. I experimented with different Streamlit layouts, widgets (like `st.expander` and `st.tabs`), and data display components (`st.dataframe`) to ensure clarity and ease of navigation. This experience enhanced my skills in **frontend development with Streamlit and designing user interfaces for data-rich applications**.

* **Managing Asynchronous Operations (Potentially):** If the application involved handling file uploads or long-running database queries that could impact the user experience, managing these asynchronously might have presented a challenge. I addressed this by [describe how you handled it if applicable - e.g., using `asyncio` or Streamlit's background tasks], which taught me about **asynchronous programming concepts and improving application responsiveness**.

Through tackling these challenges, I gained valuable experience in:

* **Cloud database management and integration (specifically with Azure SQL).**
* **Relational database design and efficient data querying.**
* **Developing user-friendly and interactive web applications with Streamlit.**
* **Handling data manipulation and presentation in a Python-based web framework.**
* **Problem-solving and debugging in a full-stack development context.**

## Future Enhancements

* **Role-Based Access Control (RBAC):** Implement a system where user roles and permissions are defined, ensuring that only members of the Project Management Office (PMO) have the authority to add or edit project details. This will enhance data integrity and control over project information.
* **Project Approval System:** Introduce an approval workflow where newly added or modified projects must be reviewed and approved by the PMO department head before they are officially added or updated in the central repository. This will ensure adherence to organizational standards and governance.
* **Private Messaging for PMO and Project Managers:** Integrate a private messaging feature that allows the PMO head to directly communicate with individual Project Managers (PMs) through a dedicated inbox. This will facilitate targeted communication and address specific project-related queries or updates.
* **Project Data Export to PDF:** Enable users to export comprehensive project details into a PDF document. This will be useful for generating reports, sharing project summaries offline, and archiving project information.
* **Enhanced Reporting and Analytics:** Expand the reporting capabilities to provide more in-depth insights into the project portfolio, such as resource allocation, risk assessment, and trend analysis. This could involve integrating more advanced data visualization libraries within Streamlit.
* **Integration with Other Productivity Tools:** Explore potential integrations with other commonly used productivity tools within the company (e.g., calendar applications, task management platforms like Jira or Trello, communication platforms like Slack or Microsoft Teams) to streamline workflows and improve collaboration.
* **Automated Notifications and Alerts:** Implement a system for automated notifications and alerts based on project milestones, deadlines, or status changes. This will help keep stakeholders informed and proactive.
* **Version History for Project Details:** Maintain a version history of project details, allowing users to track changes and revert to previous versions if necessary. This will improve accountability and provide an audit trail.
