from flask import Flask, jsonify, request, render_template
import requests
import google.generativeai as genai
import os
import markdown2




app = Flask(__name__)

# Configure Gemini API (Use your actual API key)
genai.configure(api_key='AIzaSyD5yLv8zkGNC7YbxxODLqlMJJKTv8VWdQw')

# Function to get data from OpenFoodFacts API
def get_data(product_name):
    url = "https://world.openfoodfacts.org/cgi/search.pl"
    params = {
            'search_terms': product_name,
            'search_simple': 1,
            'json': 1,
            'tagtype_0': 'countries',   # Filter by country
            'tag_contains_0': 'contains',
            'tag_0': 'India',
        }
    response = requests.get(url, params=params)
    data = response.json()
    if 'products' not in data or len(data['products']) == 0:
        return []  # Return empty if no products found
    # print(data['products'][:5])
    # if product dosent have name field then remove the product
    data['products'] = [p for p in data['products'] if 'product_name' in p]
    print(data['products'][:5])
    return data['products'][:5]  # Return top 5 results

# Function to generate product analysis using Gemini
def generate_summary(product, tone):
    # name = product.get('product_name', 'Not mentioned')
    # brand = product.get('brands', 'Not mentioned')
    # nutriscore_grade = product.get('nutriscore_grade', 'Not mentioned')
    # eco_score = product.get('ecoscore_grade', 'Not mentioned')

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
        print('##########################################')
        print(product)
        print('##########################################')
        product = product.get('product')
        name = product.get('name', 'Not mentioned')
        print(name)
        brand = product.get('brands', 'Not mentioned')
        nutriscore_grade = product.get('nutriscore_grade', 'Not mentioned')
        eco_score = product.get('ecoscore_grade', 'Not mentioned')
        packaging = product.get('packaging', 'Not mentioned')
        # ingredients = product.get('ingredients_text', 'Not mentioned')
        ingredients = product.get('ingredients', 'Not mentioned')
        print(ingredients)
        nutrients = product.get('nutrients_data', 'Not mentioned')
        image_url = product.get('image_url', 'Not mentioned')
        web_url = product.get('url', 'Not mentioned')
        barcode = product.get('_id')
        vitamins = product.get('vitamins_tags', 'Not mentioned')
        keywords = product.get('_keywords', 'Not mentioned')
        nova = product.get('nova_groups_tags', 'Not mentioned')


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
            # prompt = f"""
            # You are an AI assistant analyzing consumer products.Here are the details
            # - Name: {name}
            # - Brand: {brand}
            # - EcoScore: {eco_score}
            # - NutriScore: {nutriscore_grade}
            # - NovaScore : {nova}
            # - Ingredients: {ingredients}
            # - NutriScore: {nutrients}
            # - Packaging: {packaging}
            # - Nutrients: {nutrients}
            # - Vitamins: {vitamins}
            # - Keywords: {keywords}
            # if the data is unavailable dont say it as unavailable and never mention it is form open food facts
            # show nutriscore, novascore and ecoscore and display it in the start and give the description of the scores as i said these data is comming from the open food facts api so give accordingly
            # Your task is to provide an in-depth analysis of the product, focusing on:
            # 1. Health impact: Explain how the ingredients, nutrients, and vitamins might affect human health.
            # 2. Environmental impact: Assess the sustainability and environmental friendliness of the product, particularly its packaging.

            # The data comes from the Open Food Facts dataset. Please ensure your response is informative and clear, helping users make conscious decisions about their health and the environment.
            # ex:
            # and if **NovaScore:** **['en:4-ultra-processed-food-and-drink-products']** 
            # make it **NovaScore:** **4-ultra-processed**
            # """
    #         prompt = f"""
    # You are an AI assistant analyzing consumer products. PLease dont give the answer in markdown foramt because it is not necessary. Here are the details:
    # - Name: {name}
    # - Brand: {brand}
    # - EcoScore: {eco_score if eco_score else 'This product’s EcoScore is currently not specified, but its sustainability may vary based on its packaging and ingredients.'}
    # - NutriScore: {nutriscore_grade if nutriscore_grade else 'The NutriScore for this product is not available at the moment, but it is crucial for evaluating health impacts.'}
    # - NovaScore: {nova if nova else 'While the NovaScore isn’t specified, it’s essential to consider how processed a product is when evaluating its healthiness.'}
    # - Ingredients: {ingredients if ingredients else 'This product contains a blend of ingredients typical for carbonated beverages.'}
    # - Nutrients: {nutrients if nutrients else 'Nutritional information is valuable for understanding the health implications of this beverage.'}
    # - Packaging: {packaging if packaging else 'The packaging can significantly influence the product’s environmental footprint.'}
    # - Vitamins: {vitamins if vitamins else 'Vitamins play an essential role in health, and their presence can affect overall wellbeing.'}
    # - Keywords: {keywords if keywords else 'Relevant keywords can highlight important features of the product.'}

    # Please summarize the NutriScore, NovaScore, and EcoScore at the beginning and provide a description of each score as mentioned above. Your task is to provide an in-depth analysis of the product, focusing on:
    # 1. Health impact: Explain how the ingredients, nutrients, and vitamins might affect human health.
    # 2. Environmental impact: Assess the sustainability and environmental friendliness of the product, particularly its packaging.

    # Ensure your response is informative and clear, helping users make conscious decisions about their health and the environment. Do not explicitly mention if any data is unknown or unavailable; instead, provide context or general information when specific data points are missing.
    # """
            prompt = f"""
    You are an AI assistant analyzing consumer products. Please provide the analysis in plain text without any special formatting, headers, or markdown. Here are the details:
    - Name: {name}
    - Brand: {brand}
    - EcoScore: {eco_score if eco_score else 'This product’s EcoScore is currently not specified, but its sustainability may vary based on its packaging and ingredients.'}
    - NutriScore: {nutriscore_grade if nutriscore_grade else 'The NutriScore for this product is not available at the moment, but it is crucial for evaluating health impacts.'}
    - NovaScore: {nova if nova else 'While the NovaScore isn’t specified, it’s essential to consider how processed a product is when evaluating its healthiness.'}
    - Ingredients: {ingredients if ingredients else 'This product contains a blend of ingredients typical for carbonated beverages.'}
    - Nutrients: {nutrients if nutrients else 'Nutritional information is valuable for understanding the health implications of this beverage.'}
    - Packaging: {packaging if packaging else 'The packaging can significantly influence the product’s environmental footprint.'}
    - Vitamins: {vitamins if vitamins else 'Vitamins play an essential role in health, and their presence can affect overall wellbeing.'}
    - Keywords: {keywords if keywords else 'Relevant keywords can highlight important features of the product.'}

    Please summarize the NutriScore, NovaScore, and EcoScore at the beginning and provide a description of each score as mentioned above. Your task is to provide an in-depth analysis of the product, focusing on:
    1. Health impact: Explain how the ingredients, nutrients, and vitamins might affect human health.
    2. Environmental impact: Assess the sustainability and environmental friendliness of the product, particularly its packaging.

    Ensure your response is informative and clear, helping users make conscious decisions about their health and the environment. Do not use markdown, bullet points, or bold text; present the information in plain sentences without any formatting. Do not explicitly mention if any data is unknown or unavailable; instead, provide context or general information when specific data points are missing.
    """



    # Generate content using Gemini LLM
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        response = model.generate_content(prompt)
        return {"summary": response.text}

# API route to get product info
@app.route('/api/products', methods=['GET'])
def get_products():
    product_name = request.args.get('name')
    products = get_data(product_name)
    if not products:
        return jsonify({"error": "No products found"}), 404

    # Extract basic info for the frontend
    product_info = [{
        # "name": product.get('product_name', 'Not mentioned'),
        # "brand": product.get('brands', 'Not mentioned'),
        # "image_url": product.get('image_url', 'Not mentioned'),
        # "web_url": product.get('url', 'Not mentioned'),
        "name" : product.get('product_name', 'Not mentioned'),
        "brand" : product.get('brands', 'Not mentioned'),
        "nutriscore_grade" : product.get('nutriscore_grade', 'Not mentioned'),
        "eco_score" : product.get('ecoscore_grade', 'Not mentioned'),
        "packaging" : product.get('packaging', 'Not mentioned'),
        "ingredients" : product.get('ingredients_text', 'Not mentioned'),
        "nutrients" : product.get('nutrients_data', 'Not mentioned'),
        "image_url" : product.get('image_url', 'Not mentioned'),
        "web_url" : product.get('url', 'Not mentioned'),
        "barcode" : product.get('_id'),
        "vitamins" : product.get('vitamins_tags', 'Not mentioned'),
        "keywords" : product.get('_keywords', 'Not mentioned'),
        "nova" : product.get('nova_groups_tags', 'Not mentioned')

    } for product in products]

    return jsonify(product_info), 200

# API route to get product summary
@app.route('/api/summary', methods=['POST'])
def get_summary():
    data = request.json
    print(data)
    product = data.get('product')
    tone = data.get('tone')
    
    if not product or not tone:
        return jsonify({"error": "Invalid data"}), 400

    summary = generate_summary(data, tone)
    # print(summary)
    # return jsonify(markdown2.markdown(summary)),200

    return jsonify(summary), 200
    # return 200

# Route for the frontend
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
