from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import requests
import markdown2
import google.generativeai as genai

app = Flask(__name__)
app.secret_key = '8a1b3e7d5f9a2c5e6b1a4f7d9c8e3b4f'  # Required for using session

# Function to get data from OpenFoodFacts API
def get_data(product_name):
    url = "https://world.openfoodfacts.org/cgi/search.pl"
    params = {
        'search_terms': product_name,
        'search_simple': 1,
        'json': 1
    }

    try:
        response = requests.get(url, params=params)

        # Check if the response was successful (status code 200)
        if response.status_code != 200:
            return jsonify({"error": f"Failed to fetch data from OpenFoodFacts API. Status code: {response.status_code}"})

        # Check if the content is in JSON format
        try:
            data = response.json()
        except ValueError:
            return jsonify({"error": "Invalid JSON response from OpenFoodFacts API"})

        # Return the top 5 products
        return data.get('products', [])[:5]

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"An error occurred: {str(e)}"})


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

    # Store the products in session
    session['products'] = products

    return jsonify([{
        "name": p.get('product_name', 'Not mentioned'),
        "brand": p.get('brands', 'Not mentioned'),
        "image_url": p.get('image_url', ''),
        "web_url": p.get('url', '')
    } for p in products])


@app.route('/summary/<int:product_id>/<tone>', methods=['GET'])
def show_summary(product_id, tone):
    # Retrieve products from session
    products = session.get('products')

    # Check if products exist in session
    if products is None or product_id >= len(products):
        return jsonify({"error": "Product not found or invalid product ID."})

    # Get the selected product
    selected_product = products[product_id]

    # Generate the summary based on tone
    summary_text = LLM(selected_product, tone)

    # Convert summary to markdown
    summary_html = markdown2.markdown(summary_text)

    return render_template('summary.html', summary=summary_html, product=selected_product)


if __name__ == '__main__':
    app.run(debug=True)
