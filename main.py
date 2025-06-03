import os
from app import generate_response
from database import database
from flask import Flask, send_file, request, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return send_file('src/index_test.html')

@app.route('/process', methods=['POST'])
def process_text():
    text = request.get_json()
    cypher_query = generate_response(text)

    raw_result = database(cypher_query)

    # Normalize the result
    processed_result = [i['Name'] for i in raw_result]

    return jsonify(processed_result)

def normalize_response(result):
    """
    Normalize Neo4j response to a JSON-compatible format
    """
    # If it's already a list of dictionaries, return directly
    if isinstance(result, list):
        if all(isinstance(r, dict) for r in result):
            return result
        elif all(hasattr(r, 'data') for r in result):  # Neo4j Record objects
            return [r.data() for r in result]
        else:
            return [str(r) for r in result]

    # If it's a CSV-style string
    if isinstance(result, str):
        if "," in result:
            return [item.strip() for item in result.split(",")]
        else:
            return [result.strip()]

    # Fallback
    return [str(result)]

def main():
    app.run(port=int(os.environ.get('PORT', 80)), debug=True)

if __name__ == "__main__":
    main()
