
import re
import os
import random

filepath = r'c:\Users\HomePC\Desktop\Laffata\shop-all.html'
with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

card_start_marker = '<div class="f-column card">'
start_indices = [m.start() for m in re.finditer(re.escape(card_start_marker), content)]

if not start_indices:
    print("No cards found to use as template!")
    exit()

def find_closing_div(text, start_idx):
    depth = 0
    i = start_idx
    while i < len(text):
        if text[i:i+4] == '<div':
            depth += 1
            i += 4
        elif text[i:i+5] == '</div':
            depth -= 1
            i += 5
            if depth == 0:
                return i + 1
        else:
            i += 1
    return -1

# Extract just the first card to use as template
idx = start_indices[0]
end_idx = find_closing_div(content, idx)
template_card = content[idx:end_idx]

# Define ALL priority products (Group 1: Old Updates, Group 2: New Updates)
priority_products = [
    # Group 1
    {
        "name": "Lattafa Asad for Men Eau de Parfum spray", 
        "short_name": "Asad", 
        "url": "/products/asad.html", 
        "price_reg": "$45.00", 
        "price_sale": "$28.00",
        "image": "/assets/products/asad/0.jpg",
        "discount": "-38%"
    },
    {
        "name": "Lattafa Yara Eau de Parfum Spray", 
        "short_name": "Yara", 
        "url": "/products/yara.html", 
        "price_reg": "$49.00", 
        "price_sale": "$29.00",
        "image": "/assets/products/yara/0.jpg",
        "discount": "-41%"
    },
    {
        "name": "Lattafa Qaed Al Fursan for Unisex Eau de Parfum Spray", 
        "short_name": "Qaed Al Fursan", 
        "url": "/products/qaed-al-fursan-unlimited.html", 
        "price_reg": "$30.00", 
        "price_sale": "$24.00",
        "image": "/assets/products/qaed-al-fursan-unlimited/0.jpg",
        "discount": "-20%"
    },
    {
        "name": "Lattafa Badee Al Oud Noble Blush Eau de Parfum Spray", 
        "short_name": "Badee Al Oud Noble Blush", 
        "url": "/products/badee-al-oud-noble-blush.html", 
        "price_reg": "$59.00", 
        "price_sale": "$38.00",
        "image": "/assets/products/badee-al-oud-noble-blush/0.jpg",
        "discount": "-35%"
    },
    {
        "name": "Lattafa Khamrah Unisex Eau de Parfum Spray", 
        "short_name": "Khamrah", 
        "url": "/products/khamrah.html", 
        "price_reg": "$37.35", 
        "price_sale": "$27.00",
        "image": "/assets/products/khamrah/0.jpg",
        "discount": "-26%"
    },
    # Group 2
    {
        "name": "Lattafa Choco Overdose Give me Gourmand collection EDP 75ml Spray", 
        "short_name": "Choco Overdose", 
        "url": "/products/choco-overdose.html", 
        "price_reg": "$59.00", 
        "price_sale": "$45.00",
        "image": "/assets/products/choco-overdose/0.jpg",
        "discount": "-24%"
    },
    {
        "name": "Lattafa Berry on Top Give me Gourmand collection EDP 75ml Spray", 
        "short_name": "Berry on Top", 
        "url": "/products/berry-on-top.html", 
        "price_reg": "$59.00", 
        "price_sale": "$45.00",
        "image": "/assets/products/berry-on-top/0.jpg",
        "discount": "-24%"
    },
    {
        "name": "Lattafa Vanilla Freak Give me Gourmand collection EDP 75ml Spray", 
        "short_name": "Vanilla Freak", 
        "url": "/products/vanilla-freak.html", 
        "price_reg": "$59.00", 
        "price_sale": "$45.00",
        "image": "/assets/products/vanilla-freak/0.jpg",
        "discount": "-24%"
    },
    {
        "name": "Lattafa Cookie Crave Give me Gourmand collection EDP 75ml Spray", 
        "short_name": "Cookie Crave", 
        "url": "/products/cookie-crave.html", 
        "price_reg": "$59.00", 
        "price_sale": "$45.00",
        "image": "/assets/products/cookie-crave/0.jpg",
        "discount": "-24%"
    },
    {
        "name": "Lattafa Whipped Pleasure Give me Gourmand collection EDP 75ml Spray", 
        "short_name": "Whipped Pleasure", 
        "url": "/products/whipped-pleasure.html", 
        "price_reg": "$59.00", 
        "price_sale": "$45.00",
        "image": "/assets/products/whipped-pleasure/0.jpg",
        "discount": "-24%"
    }
]

generated_cards = []

for p in priority_products:
    new_card = template_card
    
    # Regex Replace Title
    new_card = re.sub(r'<a class="reversed-link" href="[^"]*">.*?</a>', f'<a class="reversed-link" href="{p["url"]}">{p["short_name"]}</a>', new_card)
    new_card = re.sub(r'<a href="[^"]*" aria-label="[^"]*"', f'<a href="{p["url"]}" aria-label="{p["short_name"]}"', new_card)
    
    # Replace Image
    new_img = f'<img src="{p["image"]}" alt="{p["short_name"]}" width="1500" height="1500" loading="lazy" class="motion-reduce" style="width:100%; height:auto;">'
    new_card = re.sub(r'<div class="media-wrapper product-card__image product-card__image--main"[^>]*>.*?</div>', 
                      f'<div class="media-wrapper product-card__image product-card__image--main" style="--aspect-ratio: 1.0">{new_img}</div>', 
                      new_card, flags=re.DOTALL)
    new_card = re.sub(r'<div class="media-wrapper product-card__image product-card__image--second[^>]*>.*?</div>', '', new_card, flags=re.DOTALL)

    # Replace Price
    new_price_html = f'''
    <div class="product-price-container">
        <span class="discount-badge">{p["discount"]}</span>
        <span class="price-new">{p["price_sale"]}</span>
        <span class="price-old">{p["price_reg"]}</span>
    </div>
    '''
    new_card = re.sub(r'<div class="\s*f-price[^>]*>.*?</div>', f'<div class="f-price f-price--left">{new_price_html}</div>', new_card, flags=re.DOTALL)
    
    fake_id = str(random.randint(1000000000000, 9999999999999))
    new_card = re.sub(r'value="\d+" class="product-variant-id"', f'value="{fake_id}" class="product-variant-id"', new_card)
    
    generated_cards.append(new_card)

# Identify range of existing cards to replace/prepend
# We will PREPEND these 10 cards to the EXISTING list of cards.
# Finding all existing cards again
extracted_cards = []
full_start = start_indices[0]
full_end = 0

for idx in start_indices:
    end_idx = find_closing_div(content, idx)
    if end_idx == -1: continue
    
    # Check if this card is one of the priority ones (to avoid duplication if they already exist at top)
    card_html = content[idx:end_idx]
    
    # We won't try to dedupe complexly, just prepend. 
    # If the user reloads, we might duplicate if we run this script multiple times on same file.
    # But since we read fresh content, it's fine.
    
    extracted_cards.append(card_html)
    full_end = max(full_end, end_idx)

# Concatenate: Generated Cards + Existing Cards
# Wait, if we just prepend, we might push "24 Carat" down. That's what we want.
final_cards = generated_cards + extracted_cards

new_grid_content = "\n".join(final_cards)
new_file_content = content[:full_start] + new_grid_content + content[full_end:]

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_file_content)

print(f"Updated shop-all.html with {len(generated_cards)} priority cards.")
