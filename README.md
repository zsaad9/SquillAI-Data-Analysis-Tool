# Squill AI Chatbot

## Project Description

Squill AI Chatbot is an advanced web-based AI tool designed to assist users in generating and executing SQL queries, analyzing data, and creating visualizations based on the queried data. The application leverages the power of OpenAI's GPT-4 model and Google BigQuery to provide intelligent query generation and comprehensive data analysis.

### Features

- **SQL Query Generation**: Users can input natural language queries, and the chatbot generates the appropriate SQL query to be executed on a BigQuery database.
- **Data Retrieval**: The application retrieves data from Google BigQuery and displays it in a tabular format.
- **Data Analysis**: The chatbot can analyze the retrieved data and provide detailed insights using OpenAI's GPT-4.
- **Data Visualization**: Users can generate visualizations such as bar charts, line charts, pie charts, and scatter plots based on the selected data columns.
- **User Interaction**: A user-friendly interface allows users to interact with the chatbot, request data analysis, and generate visualizations through an intuitive chat interface.
- **Copy to Clipboard**: Users can copy the results table to the clipboard.
- **Export to CSV**: Users can export the query results to a CSV file for further analysis.

### Technologies Used

- **Frontend**: HTML, CSS (TailwindCSS), JavaScript
- **Backend**: Python, Flask
- **Database**: Google BigQuery
- **AI Models**: OpenAI GPT-4
- **Visualization**: Plotly

### How It Works

1. **User Query**: The user inputs a query in natural language into the chat interface.
2. **SQL Generation**: The backend processes the input and uses OpenAI's GPT-4 to generate the corresponding SQL query.
3. **Data Retrieval**: The generated SQL query is executed on Google BigQuery, and the results are fetched.
4. **Display Results**: The results are displayed in a tabular format within the chat interface.
5. **Data Analysis**: Users can request a detailed analysis of the data, which is processed and returned by OpenAI's GPT-4.
6. **Visualization**: Users can choose the type of visualization and the columns to be visualized. The backend generates the visualization using Plotly and displays it to the user.

