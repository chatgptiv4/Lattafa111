
import re
import os

filepath = r'c:\Users\HomePC\Desktop\Laffata\shop-all.html'
with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# 1. Find all product cards
# We look for <div class="f-column card"> and traverse to matching </div>
card_start_marker = '<div class="f-column card">'
cards = []
start_indices = [m.start() for m in re.finditer(re.escape(card_start_marker), content)]

print(f"Found {len(start_indices)} existing cards.")

if not start_indices:
    print("No cards found!")
    exit()

# Function to find matching closing div
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
                return i + 1 # Include the >
        else:
            i += 1
    return -1

extracted_cards = []
full_start = start_indices[0]
full_end = 0

for idx in start_indices:
    end_idx = find_closing_div(content, idx)
    if end_idx == -1:
        print(f"Error parse at {idx}")
        continue
    
    card_html = content[idx:end_idx]
    
    # Extract Title to identify
    # <a class="reversed-link" href="/products/...">Title</a>
    title_match = re.search(r'<a class="reversed-link"[^>]*>(.*?)</a>', card_html)
    title = title_match.group(1) if title_match else "Unknown"
    
    extracted_cards.append({
        'html': card_html,
        'title': title,
        'original_index': idx
    })
    full_end = max(full_end, end_idx)

print(f"Extracted {len(extracted_cards)} cards.")

# 2. Define priority groups
group1_names = ["Asad", "Yara", "Qaed Al Fursan", "Badee Al Oud Noble Blush", "Khamrah"]
# Normalize for matching
group1_keywords = {
    "Asad": ["Asad"],
    "Yara": ["Yara"],
    "Qaed Al Fursan": ["Qaed Al Fursan", "Qaed Al Fursan Unlimited", "Qaed Al Fursan Untamed"],
    "Badee Al Oud Noble Blush": ["Badee Al Oud Noble Blush"], # Specific one
    "Khamrah": ["Khamrah", "Khamrah Qahwa", "Khamrah Dukhan"] # Maybe just Khamrah? User said "Lattafa Khamrah Unisex Eau de Parfum Spray". Usually just Khamrah.
}

# The user wants "Lattafa Khamrah Unisex..." specifically. 
# I'll stick to strict matching if possible or fuzzy.
# Matches found in shop-all.html previously: "Khamrah", "Badee Al Oud Noble Blush".

group1_cards = []
rest_cards = []

found_group1 = set()

for card in extracted_cards:
    title = card['title']
    
    is_group1 = False
    for key, variants in group1_keywords.items():
        for v in variants:
            if v.lower() in title.lower():
                # Special check for Asad mostly matching Asad Zanzibar etc.
                # User specifically listed "Lattafa Asad for Men..." ($45).
                # Previous update was just "Asad".
                # If title is just "Asad", it's the one.
                if key == "Asad" and title != "Asad":
                     continue # Skip Asad Zanzibar
                
                # Check for Khamrah variants
                if key == "Khamrah" and title != "Khamrah":
                    continue
                
                # Check Yara variants (Tous, Candy)
                if key == "Yara" and title != "Yara":
                    continue

                card['sort_key'] = key # To sort within group1 if needed
                group1_cards.append(card)
                found_group1.add(key)
                is_group1 = True
                break
        if is_group1: break
    
    if not is_group1:
        rest_cards.append(card)

# Sort group1 according to user list order
group1_order = ["Asad", "Yara", "Qaed Al Fursan", "Badee Al Oud Noble Blush", "Khamrah"]
group1_cards.sort(key=lambda x: group1_order.index(x['sort_key']) if x['sort_key'] in group1_order else 99)

# 3. Create Group 2 (New Products)
# We need to GENERATE these cards as they aren't in the file.
# We'll use the FIRST card from rest_cards as a template.
if not rest_cards:
    print("Error: No cards to use as template.")
    exit()

template_card = rest_cards[0]['html']

new_products_data = [
    {
        "name": "Lattafa Choco Overdose Give me Gourmand collection EDP 75ml Spray", 
        "short_name": "Choco Overdose", 
        "url": "/products/choco-overdose.html", 
        "price_reg": "$59.00 USD", 
        "price_sale": "$45.00 USD",
        "image": "/assets/products/choco-overdose/0.jpg",
        "discount": "-24%"
    },
    {
        "name": "Lattafa Berry on Top Give me Gourmand collection EDP 75ml Spray", 
        "short_name": "Berry on Top", 
        "url": "/products/berry-on-top.html", 
        "price_reg": "$59.00 USD", 
        "price_sale": "$45.00 USD",
        "image": "/assets/products/berry-on-top/0.jpg",
        "discount": "-24%"
    },
    {
        "name": "Lattafa Vanilla Freak Give me Gourmand collection EDP 75ml Spray", 
        "short_name": "Vanilla Freak", 
        "url": "/products/vanilla-freak.html", 
        "price_reg": "$59.00 USD", 
        "price_sale": "$45.00 USD",
        "image": "/assets/products/vanilla-freak/0.jpg",
        "discount": "-24%"
    },
    {
        "name": "Lattafa Cookie Crave Give me Gourmand collection EDP 75ml Spray", 
        "short_name": "Cookie Crave", 
        "url": "/products/cookie-crave.html", 
        "price_reg": "$59.00 USD", 
        "price_sale": "$45.00 USD",
        "image": "/assets/products/cookie-crave/0.jpg",
        "discount": "-24%"
    },
    {
        "name": "Lattafa Whipped Pleasure Give me Gourmand collection EDP 75ml Spray", 
        "short_name": "Whipped Pleasure", 
        "url": "/products/whipped-pleasure.html", 
        "price_reg": "$59.00 USD", 
        "price_sale": "$45.00 USD",
        "image": "/assets/products/whipped-pleasure/0.jpg",
        "discount": "-24%"
    }
]

group2_cards = []

for p in new_products_data:
    new_card = template_card
    
    # Regex Replace Title
    new_card = re.sub(r'<a class="reversed-link" href="[^"]*">.*?</a>', f'<a class="reversed-link" href="{p["url"]}">{p["short_name"]}</a>', new_card)
    # Regex Replace Link in Image
    new_card = re.sub(r'<a href="[^"]*" aria-label="[^"]*"', f'<a href="{p["url"]}" aria-label="{p["short_name"]}"', new_card)
    
    # Regex Replace Images
    # The template has srcset and src. We'll just nuke the inner HTML of media-wrapper or replace img src.
    # Simple replace of the main img src might work if template is consistent.
    # But template has complex shopify liquid/cdn URLs.
    # We replace the whole img tag?
    # Or just replace the src attribute content.
    # <img src="..." alt="...">
    # We'll try to find the src="..." and replace it.
    
    # Doing a brute force replacement of the <img> block might be safer.
    # Look for <div class="media-wrapper ..."><img ...></div>
    
    # Construct new image tag
    new_img = f'<img src="{p["image"]}" alt="{p["short_name"]}" width="1500" height="1500" loading="lazy" class="motion-reduce" style="width:100%; height:auto;">'
    
    # Replace main image
    new_card = re.sub(r'<div class="media-wrapper product-card__image product-card__image--main"[^>]*>.*?</div>', 
                      f'<div class="media-wrapper product-card__image product-card__image--main" style="--aspect-ratio: 1.0">{new_img}</div>', 
                      new_card, flags=re.DOTALL)
    
    # Remove secondary image (hover) to simplify, or use same image
    new_card = re.sub(r'<div class="media-wrapper product-card__image product-card__image--second[^>]*>.*?</div>', 
                      '', 
                      new_card, flags=re.DOTALL)

    # Replace Price
    # We need the new price structure:
    # <div class="product-price-container">...</div>
    new_price_html = f'''
    <div class="product-price-container">
        <span class="discount-badge">{p["discount"]}</span>
        <span class="price-new">{p["price_sale"]}</span>
        <span class="price-old">{p["price_reg"]}</span>
    </div>
    '''
    
    # Find existing f-price div and replace content
    new_card = re.sub(r'<div class="\s*f-price[^>]*>.*?</div>', f'<div class="f-price f-price--left">{new_price_html}</div>', new_card, flags=re.DOTALL)
    
    # Update Quick Add form IDs to be unique?
    # id="quick-add-template...9055..."
    # We should generate a fake random ID or just strip the ID to avoid conflict?
    # Or replace the product ID.
    import random
    fake_id = str(random.randint(1000000000000, 9999999999999))
    new_card = re.sub(r'value="\d+" class="product-variant-id"', f'value="{fake_id}" class="product-variant-id"', new_card)
    
    group2_cards.append(new_card)

# 4. Concatenate
final_cards = [c['html'] for c in group1_cards] + group2_cards + [c['html'] for c in rest_cards]

# 5. Rebuild File
# We found ALL cards. Check if they were contiguous.
# If there's garbage between cards (whitespace is fine), we lose it if we just join.
# But extracted_cards was based on finding sequential divs.
# If the file structure is <grid> <card> ... <card> </grid>, we can replace from start of first card to end of last card.
# BUT, is full_start to full_end contiguous?
# We didn't check for content BETWEEN cards.
# Usually there isn't any except whitespace.
# We will replace content[full_start:full_end] with joined cards.

new_grid_content = "\n".join(final_cards)
new_file_content = content[:full_start] + new_grid_content + content[full_end:]

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_file_content)

print("Updated shop-all.html")
print(f"Group 1 Count: {len(group1_cards)}")
print(f"Group 2 Count: {len(group2_cards)}")
