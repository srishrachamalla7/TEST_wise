import requests
import google.generativeai as genai
import gradio as gr

# Configure Gemini API (Use your actual API key)
genai.configure(api_key='AIzaSyD5yLv8zkGNC7YbxxODLqlMJJKTv8VWdQw')

# Function to get data from OpenFoodFacts API
def get_data(product_name):
    url = "https://world.openfoodfacts.org/cgi/search.pl"
    params = {
        'search_terms': product_name,
        'search_simple': 1,
        'json': 1,
    }
    response = requests.get(url, params=params)
    data = response.json()
    if 'products' not in data or len(data['products']) == 0:
        return []  # Return empty if no products found

    # Filter products with names and return top 5
    data['products'] = [p for p in data['products'] if 'product_name' in p]
    print(data['products'][:5])
    return data['products'][:5]

# Function to generate product analysis using Gemini
def generate_summary(product, tone):
    name = product.get('product_name', 'Not mentioned')
    brand = product.get('brands', 'Not mentioned')
    nutriscore_grade = product.get('nutriscore_grade', 'Not mentioned')
    eco_score = product.get('ecoscore_grade', 'Not mentioned')
    packaging = product.get('packaging', 'Not mentioned')
    ingredients = product.get('ingredients_text', 'Not mentioned')
    nutrients = product.get('nutriments', 'Not mentioned')
    nova = product.get('nova_groups_tags', 'Not mentioned')

    # Generate prompt based on tone
    prompt = f"""
    You are an AI assistant analyzing consumer products. Here are the details:
    - Name: {name}
    - Brand: {brand}
    - EcoScore: {eco_score}
    - NutriScore: {nutriscore_grade}
    - NovaScore: {nova}
    - Ingredients: {ingredients}
    - Nutrients: {nutrients}
    - Packaging: {packaging}

    Please provide a {tone} analysis including:
    1. Positive aspects of the product.
    2. Negative aspects of the product.
    3. Health impact.
    4. Environmental impact.
    """
    
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text

# Function to search products and return a list of product names
def search_products(product_name):
    products = get_data(product_name)
    if not products:
        return "No products found for the given name.", [], []
    
    # Create a list of product names for dropdown
    product_names = [f"{p['product_name']} (Brand: {p.get('brands', 'Unknown')})" for p in products]
    print(product_names)
    return product_names, products  # Return names and products

# Function to generate summary for the selected product
def generate_selected_product_summary(product_name, product_list, tone):
    if not product_name:
        return "No product selected", None

    # Find the selected product
    selected_product = next((p for p in product_list if product_name in p['product_name']), None)
    if not selected_product:
        return "Selected product not found.", None

    # Generate the summary for the selected product
    summary = generate_summary(selected_product, tone)
    return f"Product Name: {selected_product['product_name']} (Brand: {selected_product.get('brands', 'Unknown')})", summary

# Gradio interface
# def build_interface():
#     product_input = gr.Textbox(label="Product Name", placeholder="Enter the product name...")
#     tone_input = gr.Radio(choices=["simple", "deeper"], value="simple", label="Summary Tone")
#     product_dropdown = gr.Dropdown(label="Select a Product", choices=[], interactive=True)

#     # Function to handle the product search and update the dropdown
#     def update_dropdown(product_name):
#         product_names, products = search_products(product_name)
#         if not product_names:
#             return gr.Dropdown.update(choices=[], value=None), products
#         return gr.Dropdown.update(choices=product_names, value=product_names[0]), products

#     # Create a button to trigger the product search
#     search_button = gr.Button("Search")

#     # Create the main interface
#     with gr.Column():
#         search_button.click(
#             fn=update_dropdown,
#             inputs=product_input,
#             outputs=[product_dropdown, gr.State()]
#         )

#         product_dropdown.change(
#             fn=generate_selected_product_summary,
#             inputs=[product_dropdown, gr.State(), tone_input],
#             outputs=["text", "text"]
#         )

#     # Launch the interface
#     gr.Interface(
#         fn=generate_selected_product_summary,
#         inputs=[product_dropdown, gr.State(), tone_input],
#         outputs=["text", "text"]
#     ).launch()
# def build_interface():
#     with gr.Blocks() as demo:
#         product_input = gr.Textbox(label="Product Name", placeholder="Enter the product name...")
#         tone_input = gr.Radio(choices=["simple", "deeper"], value="simple", label="Summary Tone")
#         product_dropdown = gr.Dropdown(label="Select a Product", choices=[], interactive=True)

#         # Function to handle the product search and update the dropdown
#         def update_dropdown(product_name):
#             product_names, products = search_products(product_name)
#             if not product_names:
#                 return gr.Dropdown.update(choices=[], value=None), products
#             return gr.Dropdown.update(choices=product_names, value=product_names[0]), products

#         # Create a button to trigger the product search
#         search_button = gr.Button("Search")

#         # Create the main interface
#         search_button.click(
#             fn=update_dropdown,
#             inputs=product_input,
#             outputs=[product_dropdown, gr.State()]
#         )

#         # Create output components
#         output_product_name = gr.Textbox(label="Product Name", placeholder="Product Name will appear here...")
#         output_summary = gr.Textbox(label="Summary", placeholder="Summary will appear here...")

#         # Product dropdown change event
#         product_dropdown.change(
#             fn=generate_selected_product_summary,
#             inputs=[product_dropdown, gr.State(), tone_input],
#             outputs=[output_product_name, output_summary]
#         )

#     # Launch the interface
#     demo.launch()

def build_interface():
    with gr.Blocks() as demo:
        product_input = gr.Textbox(label="Product Name", placeholder="Enter the product name...")
        tone_input = gr.Radio(choices=["simple", "deeper"], value="simple", label="Summary Tone")
        product_names_state = gr.State(value=[])
        product_dropdown = gr.Dropdown(label="Select a Product", choices=[], interactive=True)

        # Function to handle the product search and update the dropdown
        def update_dropdown(product_name):
            product_names, products = search_products(product_name)
            return gr.Dropdown.update(choices=product_names), product_names, products

        # Function to handle the product dropdown change
        def update_product_summary(product_name, product_names, tone):
            if not product_name:
                return "No product selected.", None
            selected_product = next((p for p in product_names if product_name in p), None)
            if not selected_product:
                return "Selected product not found.", None
            summary = generate_summary(selected_product, tone)
            return f"Product Name: {selected_product}", summary

        # Create a button to trigger the product search
        search_button = gr.Button("Search")
        search_button.click(
            fn=update_dropdown,
            inputs=product_input,
            outputs=[product_dropdown, product_names_state, gr.State()]
        )

        # Create output components
        output_product_name = gr.Textbox(label="Product Name", placeholder="Product Name will appear here...")
        output_summary = gr.Textbox(label="Summary", placeholder="Summary will appear here...")

        # Product dropdown change event
        product_dropdown.change(
            fn=update_product_summary,
            inputs=[product_dropdown, product_names_state, tone_input],
            outputs=[output_product_name, output_summary]
        )

    # Launch the interface
    demo.launch()

if __name__ == "__main__":
    build_interface()