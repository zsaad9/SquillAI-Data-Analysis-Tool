import os
from google.cloud import bigquery
import pandas as pd
from .openai_api import generate_sql_query, analyze_data_with_openai
import plotly.express as px
import io
import base64

# Initialize BigQuery client
bq_client = bigquery.Client()

def query_database(query):
    query_job = bq_client.query(query)
    result = query_job.result()
    df = result.to_dataframe()
    return df

def get_gpt4_response(question, error_message=None):
    base_prompt = (
        "You are a data analyst who helps in writing SQL queries. There are multiple tables in my database: "
        "order, product, customer, marketing, inventory, and payment. "
        "These are the attributes in each table: \n"
        "1. order: orderid, customerid, orderdate, productid, totalprice, shippingaddress, quantity \n"
        "2. product: productid, productname, category, price, stockquantity \n"
        "3. customer: customerid, firstname, lastname, email, signupdate, city, country \n"
        "4. marketing: campaignid, campaignname, startdate, enddate, budget, totalspent, roi \n"
        "5. inventory: productid, warehouselocation, stocklevel \n"
        "6. payment: paymentid, orderid, paymentmethod, paymentamount, paymentdate \n"
        "Now Write an SQL query to: {question}. **Only write the SQL query for BigQuery, nothing else. Make sure you are using the correct attribute names. From statement should be squill_test.tablename**"
    )
    if error_message:
        base_prompt += f"\nThe previous query failed with the following error: {error_message}. Please write a new SQL query to achieve the same result."
    
    return generate_sql_query(base_prompt.format(question=question))

def analyze_data(data):
    prompt = (
        "You are a data analyst. Please analyze the following data and provide insights:\n\n"
        f"{data}\n\n"
        "Provide a detailed analysis. **Please do not provide dataset summary or dataset overview in your answer**"
    )
    return analyze_data_with_openai(prompt)

def generate_plot(data, chart_type, selected_columns, column_types):
    df = pd.DataFrame(data['rows'], columns=data['columns'])

    # Select only the specified columns
    if selected_columns:
        df = df[selected_columns]

    # Ensure consistent data types
    for col, col_type in column_types.items():
        if col in df.columns:
            if col_type == 'numerical':
                df[col] = pd.to_numeric(df[col], errors='coerce')
            elif col_type == 'categorical':
                df[col] = df[col].astype(str)

    # Determine x and y columns
    x_col = df.columns[0]
    y_cols = df.columns[1:]

    if chart_type in ['bar', 'line']:
        if len(y_cols) > 1:
            df_melted = df.melt(id_vars=[x_col], value_vars=y_cols, var_name='variable', value_name='value')
            fig = px.bar(df_melted, x=x_col, y='value', color='variable') if chart_type == 'bar' else px.line(df_melted, x=x_col, y='value', color='variable')
        else:
            fig = px.bar(df, x=x_col, y=y_cols[0]) if chart_type == 'bar' else px.line(df, x=x_col, y=y_cols[0])
    elif chart_type == 'pie':
        fig = px.pie(df, names=x_col, values=y_cols[0])
    elif chart_type == 'scatter':
        if len(df.columns) < 2:
            raise ValueError("Scatter plot requires at least two numeric columns")
        fig = px.scatter(df, x=x_col, y=y_cols[0])
    else:
        raise ValueError("Unsupported chart type")

    img_bytes = fig.to_image(format="png")
    img = io.BytesIO(img_bytes)
    img.seek(0)
    
    return img
