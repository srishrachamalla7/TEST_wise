from flask import Flask, request, jsonify
from flask_cors import CORS
from src.main import OpenFoodFacts


OFF = OpenFoodFacts()
app = Flask(__name__)
@app.route('/')
def home():
    return 'AI ConsumeNice product'

@app.route('/name', methods=['POST'])
def send():
    try:
        product_name = request.form.get('product_name')
        extracted_data =OFF.get_data(product_name)

        return jsonify(extracted_data)
    
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/Products', methods=['GET'])
def display(products):
    data = OFF.product_info_extraction(products)
    return jsonify(data)

# @app.route('/summary/<int:product_id>/<tone>', methods=['GET'])
@app.route('/summary', methods=['POST'])
def get_summary(product_data,tone):
    summary = OFF.LLM(product_data, tone)
    return jsonify(summary)

if __name__ == '__main__':
    app.run(debug=True)