ee = {'product': {'barcode': '5449000043382', 'brand': 'Coca-Cola', 'eco_score': 'unknown', 'image_url': 'https://images.openfoodfacts.org/images/products/544/900/004/3382/front_en.3.400.jpg', 'ingredients': '', 'keywords': ['beverage', 'carbonated', 'coca-cola', 'coke', 'drink'], 'name': 'Coke', 'nova': ['unknown'], 'nutrients': 'Not mentioned', 'nutriscore_grade': 'b', 'packaging': '', 'vitamins': [], 'web_url': 'https://world.openfoodfacts.org/product/5449000043382/coke-coca-cola'}, 'tone': 'deeper'}

print(type(ee))
ee = ee.get('product')
print(ee.get('name'))