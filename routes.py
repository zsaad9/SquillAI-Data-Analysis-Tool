from flask import Blueprint, request, jsonify, render_template, send_file
from .utils import get_gpt4_response, query_database, analyze_data, generate_plot
import io

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    print("Serving index.html")
    return render_template('index.html')

@main_bp.route('/query', methods=['POST'])
def get_query():
    user_input = request.json.get('user_input')
    max_attempts = 5
    attempts = 0
    sql_query = get_gpt4_response(user_input)

    while attempts < max_attempts:
        try:
            result = query_database(sql_query)
            formatted_result = {
                "summary": {
                    "attempts": attempts + 1,
                    "query": sql_query,
                    "status": "success"
                },
                "data": {
                    "columns": list(result.columns),
                    "rows": result.to_dict(orient='records')
                }
            }
            return jsonify(formatted_result)
        except Exception as e:
            error_message = str(e)
            attempts += 1
            if attempts < max_attempts:
                sql_query = get_gpt4_response(user_input, error_message)
            else:
                formatted_result = {
                    "summary": {
                        "attempts": attempts,
                        "query": sql_query,
                        "status": "failed",
                        "error_message": error_message
                    },
                    "data": None
                }
                return jsonify(formatted_result)

@main_bp.route('/analyze', methods=['POST'])
def analyze():
    data = request.json.get('data')
    analysis_result = analyze_data(data)
    return jsonify({"analysis": analysis_result})

@main_bp.route('/visualize', methods=['POST'])
def visualize():
    data = request.json.get('data')
    chart_type = data.pop('visualizationType', 'bar')
    selected_columns = data.pop('selectedColumns', [])
    column_types = data.pop('columnTypes', {})

    plot_img = generate_plot(data, chart_type, selected_columns, column_types)
    return send_file(plot_img, mimetype='image/png')
