import os
from openai import OpenAI

# Initialize OpenAI API with key from environment variable
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

def generate_sql_query(prompt):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=250,
    )
    sql_query = response.choices[0].message.content.strip()

    # Remove markdown code block syntax if present
    if sql_query.startswith("```") and sql_query.endswith("```"):
        sql_query = sql_query[3:-3].strip()

    # Remove leading 'sql' if present
    if sql_query.lower().startswith("sql"):
        sql_query = sql_query[3:].strip()

    return sql_query

def analyze_data_with_openai(prompt):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=500,
    )
    analysis = response.choices[0].message.content.strip()
    return analysis
