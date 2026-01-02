
import json
import os

products_json_path = r'c:\Users\HomePC\Desktop\Laffata\products.json'

with open(products_json_path, 'r', encoding='utf-8') as f:
    products = json.load(f)

existing_urls = set(p['url'] for p in products)

new_products = [
    {
        "name": "Lattafa Choco Overdose Give me Gourmand collection EDP 75ml Spray",
        "url": "/products/choco-overdose.html",
        "price": "45.00",
        "image": "/assets/products/choco-overdose/0.jpg"
    },
    {
        "name": "Lattafa Berry on Top Give me Gourmand collection EDP 75ml Spray",
        "url": "/products/berry-on-top.html",
        "price": "45.00",
        "image": "/assets/products/berry-on-top/0.jpg"
    },
    {
        "name": "Lattafa Vanilla Freak Give me Gourmand collection EDP 75ml Spray",
        "url": "/products/vanilla-freak.html",
        "price": "45.00",
        "image": "/assets/products/vanilla-freak/0.jpg"
    },
    {
        "name": "Lattafa Cookie Crave Give me Gourmand collection EDP 75ml Spray",
        "url": "/products/cookie-crave.html",
        "price": "45.00",
        "image": "/assets/products/cookie-crave/0.jpg"
    },
    {
        "name": "Lattafa Whipped Pleasure Give me Gourmand collection EDP 75ml Spray",
        "url": "/products/whipped-pleasure.html",
        "price": "45.00",
        "image": "/assets/products/whipped-pleasure/0.jpg"
    }
]

added_count = 0
for p in new_products:
    if p['url'] not in existing_urls:
        products.append(p)
        print(f"Added {p['name']}")
        added_count += 1
    else:
        print(f"Skipped {p['name']} (already exists)")

if added_count > 0:
    with open(products_json_path, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2)
    print("Updated products.json")
else:
    print("products.json up to date")
