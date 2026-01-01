
import json
import os

products_json_path = r'c:\Users\HomePC\Desktop\Laffata\products.json'

with open(products_json_path, 'r', encoding='utf-8') as f:
    products = json.load(f)

new_products = [
    {
        "name": "Choco Overdose",
        "url": "/products/choco-overdose.html",
        "price": "45.00",
        "image": "/assets/products/choco-overdose/0.jpg"
    },
    {
        "name": "Berry on Top",
        "url": "/products/berry-on-top.html",
        "price": "45.00",
        "image": "/assets/products/berry-on-top/0.jpg"
    },
    {
        "name": "Vanilla Freak",
        "url": "/products/vanilla-freak.html",
        "price": "45.00",
        "image": "/assets/products/vanilla-freak/0.jpg"
    },
    {
        "name": "Cookie Crave",
        "url": "/products/cookie-crave.html",
        "price": "45.00",
        "image": "/assets/products/cookie-crave/0.jpg"
    },
    {
        "name": "Whipped Pleasure",
        "url": "/products/whipped-pleasure.html",
        "price": "45.00",
        "image": "/assets/products/whipped-pleasure/0.jpg"
    }
]

# Check if already exist to avoid duplicates
existing_urls = set(p['url'] for p in products)
for p in new_products:
    if p['url'] not in existing_urls:
        products.append(p)
        print(f"Added {p['name']}")
    else:
        print(f"Skipped {p['name']} (already exists)")

with open(products_json_path, 'w', encoding='utf-8') as f:
    json.dump(products, f, indent=2)
