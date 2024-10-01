from flask import Flask, request, jsonify,render_template
from flask_cors import CORS
from src.main import OpenFoodFacts


OFF = OpenFoodFacts()
app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')

# @app.route('/name', methods=['POST'])
# def send():
#     try:
#         product_name = request.form.get('product_name')
#         extracted_data =OFF.get_data(product_name)

#         return jsonify(extracted_data)
    
#     except Exception as e:
#         return f"An error occurred: {e}"

# @app.route('/Products', methods=['GET'])
# def display(products):
#     data = OFF.product_info_extraction(products)
#     return jsonify(data)

@app.route('/name', methods=['POST'])
def send():
    try:
        product_name = request.form.get('product_name')
        # Extract data for the given product name
        extracted_data = OFF.get_data(product_name)
        
        # Extract relevant product information for the table
        products = OFF.product_info_extraction(extracted_data)

        # Render the HTML template with the product data
        return render_template('products.html', products=products)

    except Exception as e:
        return f"An error occurred: {e}"
# @app.route('/summary/<int:product_id>/<tone>', methods=['GET'])
@app.route('/summary', methods=['POST'])
def get_summary(product_data,tone):
    summary = OFF.LLM(product_data, tone)
    return jsonify(summary)

if __name__ == '__main__':
    app.run(debug=True)