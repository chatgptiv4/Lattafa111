
import re
import os

target_files = [
    r'c:\Users\HomePC\Desktop\Laffata\shop-all.html',
    r'c:\Users\HomePC\Desktop\Laffata\best-sellers.html'
]

products_to_update = [
    "/products/choco-overdose.html",
    "/products/berry-on-top.html",
    "/products/vanilla-freak.html",
    "/products/cookie-crave.html",
    "/products/whipped-pleasure.html",
    "/products/asad.html",
    "/products/yara.html",
    "/products/qaed-al-fursan-unlimited.html",
    "/products/badee-al-oud-noble-blush.html",
    "/products/khamrah.html"
]

target_price_html = '''    <div class="product-price-container">
        <span class="discount-badge">-38%</span>
        <span class="price-new">$28.00</span>
        <span class="price-old">$45.00</span>
    </div>'''

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

for filepath in target_files:
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        continue
        
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # We loop through content, finding cards, identifying if they belong to our products, and replacing price.
    # Note: Regex replacing inside a large file can be tricky if we don't know exact context.
    # But we iterate cards.
    
    card_start_marker = '<div class="f-column card">'
    start_indices = [m.start() for m in re.finditer(re.escape(card_start_marker), content)]
    
    new_content_parts = []
    last_idx = 0
    
    for idx in start_indices:
        # Append content before this card
        new_content_parts.append(content[last_idx:idx])
        
        end_idx = find_closing_div(content, idx)
        if end_idx == -1:
            # Error fallback: append rest and stop
            new_content_parts.append(content[idx:])
            last_idx = len(content)
            break
            
        card_html = content[idx:end_idx]
        
        # Check if card is for one of our products
        matched_product = False
        for url in products_to_update:
            if url in card_html:
                matched_product = True
                break
        
        if matched_product:
            # Replace price block
            # Look for existing price container (either old f-price or new product-price-container)
            
            # Pattern 1: New container
            m_new = re.search(r'<div class="product-price-container">.*?</div>', card_html, re.DOTALL)
            if m_new:
                # Replace inner content of parent f-price div? No, just replace this container?
                # Wait, structure is <div class="f-price ..."><div class="product-price-container">...</div></div>
                # If I replace product-price-container, parent f-price remains.
                
                # Regex replace the whole product-price-container block
                card_html = re.sub(r'<div class="product-price-container">.*?</div>', 
                                   target_price_html.strip(), 
                                   card_html, flags=re.DOTALL)
            else:
                # Pattern 2: Old f-price block
                m_old = re.search(r'<div class="\s*f-price[^>]*>.*?</div>', card_html, re.DOTALL)
                if m_old:
                    # We need to preserve the outer f-price div?
                    # Or replace it?
                    # Best to replace valid inner content. 
                    # But f-price matches the whole block.
                    # We can replace the whole f-price block with:
                    # <div class="f-price f-price--left"> [target_price_html] </div>
                    
                    new_block = f'<div class="f-price f-price--left">\n{target_price_html}\n</div>'
                    card_html = re.sub(r'<div class="\s*f-price[^>]*>.*?</div>', new_block, card_html, flags=re.DOTALL)
        
        new_content_parts.append(card_html)
        last_idx = end_idx

    new_content_parts.append(content[last_idx:])
    
    new_full_content = "".join(new_content_parts)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_full_content)
        
    print(f"Updated {filepath}")

print("Done enforcing prices.")
