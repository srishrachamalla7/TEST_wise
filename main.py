# from flask import Flask, jsonify, request, render_template
# import requests
# import google.generativeai as genai
# import os

# genai.configure(api_key='AIzaSyD5yLv8zkGNC7YbxxODLqlMJJKTv8VWdQw')


# app = Flask(__name__)

# # Configure Gemini API (Use your actual API key)
# genai.configure(api_key='AIzaSyD5yLv8zkGNC7YbxxODLqlMJJKTv8VWdQw')

# # Function to get data from OpenFoodFacts API
# def get_data(product_name):
#     url = "https://world.openfoodfacts.org/cgi/search.pl"
#     params = {
#         'search_terms': product_name,
#         'search_simple': 1,
#         'json': 1
#     }
#     response = requests.get(url, params=params)
#     data = response.json()
#     if 'products' not in data or len(data['products']) == 0:
#         return []  # Return empty if no products found
#     return data['products'][:5]  # Return top 5 results

# # Function to generate product analysis using Gemini
# def generate_summary(product, tone):
#     name = product.get('product_name', 'Not mentioned')
#     brand = product.get('brands', 'Not mentioned')
#     nutriscore_grade = product.get('nutriscore_grade', 'Not mentioned')
#     eco_score = product.get('ecoscore_grade', 'Not mentioned')

#     # Generate prompt based on tone
#     if tone == 'simple':
#         prompt = f"""
#         The product name is {name}, brand is {brand}, and its eco-score is {eco_score}, nutriscore grade is {nutriscore_grade}.
#         Provide a simple analysis including:
#         1. Positive aspects.
#         2. Negative aspects.
#         3. Health impact.
#         4. Environmental impact.
#         """
#     else:
#         prompt = f"""
#         The product name is {name}, brand is {brand}, and its eco-score is {eco_score}, nutriscore grade is {nutriscore_grade}.
#         Provide a deeper analysis including:
#         1. Positive aspects.
#         2. Negative aspects.
#         3. Health impact (positive and negative).
#         4. Environmental impact (packaging and ingredients).
#         5. Include relevant health articles if available.
#         """

#     # Generate content using Gemini LLM
#     model = genai.GenerativeModel(model_name="gemini-1.5-flash")
#     response = model.generate_content(prompt)
#     return {"summary": response.text}

# # API route to get product info
# @app.route('/api/products', methods=['GET'])
# def get_products():
#     product_name = request.args.get('name')
#     products = get_data(product_name)
#     if not products:
#         return jsonify({"error": "No products found"}), 404

#     # Extract basic info for the frontend
#     product_info = [{
#         "name": p.get('product_name', 'Not mentioned'),
#         "brand": p.get('brands', 'Not mentioned'),
#         "image_url": p.get('image_url', 'Not mentioned'),
#         "web_url": p.get('url', 'Not mentioned')
#     } for p in products]

#     return jsonify(product_info), 200

# # API route to get product summary
# @app.route('/api/summary', methods=['POST'])
# def get_summary():
#     data = request.json
#     product = data.get('product')
#     tone = data.get('tone')
    
#     if not product or not tone:
#         return jsonify({"error": "Invalid data"}), 400

#     summary = generate_summary(product, tone)
#     return jsonify(summary), 200

# # Route for the frontend
# @app.route('/')
# def index():
#     return render_template('index.html')

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests
import markdown2
import google.generativeai as genai

app = Flask(__name__)

# Function to get data from OpenFoodFacts API
def get_data(product_name):
    url = "https://world.openfoodfacts.org/cgi/search.pl"
    params = {
        'search_terms': product_name,
        'search_simple': 1,
        'json': 1
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data['products'][:5]  # Return top 5 results


# LLM function based on your provided use case
# def LLM(product, tone):
    # name = product.get('product_name', 'Not mentioned')
    # brand = product.get('brands', 'Not mentioned')
    # nutriscore_grade = product.get('nutriscore_grade', 'Not mentioned')
    # eco_score = product.get('ecoscore_grade', 'Not mentioned')
    # packaging = product.get('packaging', 'Not mentioned')
    # ingredients = product.get('ingredients_text', 'Not mentioned')
    # nutrients = product.get('nutrients_data', 'Not mentioned')
    # image_url = product.get('image_url', 'Not mentioned')
    # web_url = product.get('url', 'Not mentioned')

    # # Generate prompt based on tone
    # if tone == 'simple':
    #     prompt = f"""
    #     The product name is {name}, brand is {brand}, and its eco-score is {eco_score}, nutriscore grade is {nutriscore_grade}.
    #     Provide a simple analysis including:
    #     1. Positive aspects.
    #     2. Negative aspects.
    #     3. Health impact.
    #     4. Environmental impact.
    #     """
    # else:
    #     prompt = f"""
    #     The product name is {name}, brand is {brand}, and its eco-score is {eco_score}, nutriscore grade is {nutriscore_grade}.
    #     Provide a deeper analysis including:
    #     1. Positive aspects.
    #     2. Negative aspects.
    #     3. Health impact (positive and negative).
    #     4. Environmental impact (packaging and ingredients).
    #     5. Include relevant health articles if available.
    #     """

    # # Using a sample response instead of actual API call to Generative AI
    # response = {
    #     'text': f'# Product Summary\n\n**Product Name**: {name}\n\nEco Score: {eco_score}\n\nSummary: {tone}'
    # }
    # return response['text']
def LLM(product, tone):
        name = product.get('product_name', 'Not mentioned')
        brand = product.get('brands', 'Not mentioned')
        nutriscore_grade = product.get('nutriscore_grade', 'Not mentioned')
        eco_score = product.get('ecoscore_grade', 'Not mentioned')
        packaging = product.get('packaging', 'Not mentioned')
        ingredients = product.get('ingredients_text', 'Not mentioned')
        nutrients = product.get('nutrients_data', 'Not mentioned')
        image_url = product.get('image_url', 'Not mentioned')
        web_url = product.get('url', 'Not mentioned')

        # Generate prompt based on tone
        if tone == 'simple':
            prompt = f"""
            The product name is {name}, brand is {brand}, and its eco-score is {eco_score}, nutriscore grade is {nutriscore_grade}.
            Provide a simple analysis including:
            1. Positive aspects.
            2. Negative aspects.
            3. Health impact.
            4. Environmental impact.
            """
        else:
            prompt = f"""
            The product name is {name}, brand is {brand}, and its eco-score is {eco_score}, nutriscore grade is {nutriscore_grade}.
            Provide a deeper analysis including:
            1. Positive aspects.
            2. Negative aspects.
            3. Health impact (positive and negative).
            4. Environmental impact (packaging and ingredients).
            5. Include relevant health articles if available.
            """

        genai.configure(api_key='AIzaSyD5yLv8zkGNC7YbxxODLqlMJJKTv8VWdQw')
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text



@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/products', methods=['GET'])
def get_products():
    product_name = request.args.get('name')
    products = get_data(product_name)
    return jsonify([{
        "name": p.get('product_name', 'Not mentioned'),
        "brand": p.get('brands', 'Not mentioned'),
        "image_url": p.get('image_url', ''),
        "web_url": p.get('url', '')
    } for p in products])


@app.route('/summary/<int:product_id>/<tone>', methods=['GET'])
def show_summary(product_id, tone):
    product_name = request.args.get('name')
    products = get_data(product_name)

    # Get the selected product
    selected_product = products[product_id]

    # Generate the summary based on tone
    summary_text = LLM(selected_product, tone)

    # Convert summary to markdown
    summary_html = markdown2.markdown(summary_text)

    return render_template('summary.html', summary=summary_html, product=selected_product)


if __name__ == '__main__':
    app.run(debug=True)