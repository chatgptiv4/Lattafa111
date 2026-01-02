import re

PRIORITY_PRODUCTS = [
    "asad", "yara", "qaed al fursan", "badee al oud noble blush",
    "khamrah", "choco overdose", "berry on top", "vanilla freak",
    "cookie crave", "whipped pleasure"
]

def extract_cards():
    with open('shop-all.html', 'r', encoding='utf-8') as f:
        content = f.read()

    cards = []
    
    # Simple state machine to find cards
    # We look for <div class="f-column card"> ... </div>
    # But strictly speaking we just want to find where each product is.
    
    # Strategy: Find the start of a card containing the product name, then extract the whole card div.
    # Since HTML parsing with regex is fragile, and we know the structure is consistent:
    # 1. Split content by <div class="f-column card">
    # 2. Check each chunk to see if it contains a priority product title
    
    chunks = content.split('<div class="f-column card">')
    
    # The first chunk is header stuff, ignore.
    # subsequent chunks start with the card content.
    
    # We need to be careful about where the div ends. 
    # Provided shop-all.html structure is fairly flat for these cards.
    # Each chunk roughly contains one card, but ends with... wait.
    # Splitting by start tag removes the tag. We need to prepend it back or just wrap results.
    
    # Better Strategy:
    # Use the logic from `find_product_location.py` to find lines, but improved.
    # Actually, the split method is risky if nested divs are complex.
    # Let's try a regex for the card block if possible, or just string manipulation.
    
    # Let's iterate through the file line by line to capture blocks.
    
    found_cards = {}
    
    current_card_lines = []
    in_card = False
    card_brackets = 0
    
    lines = content.splitlines()
    for line in lines:
        if '<div class="f-column card">' in line:
            in_card = True
            current_card_lines = []
            card_brackets = 0 
            # We count this as opening the card.
            # But line might have other divs. 
            # Let's simple-count <div> and </div>
        
        if in_card:
            current_card_lines.append(line)
            card_brackets += line.count('<div')
            card_brackets -= line.count('</div>')
            
            if card_brackets == 0:
                in_card = False
                # Process the card we just found
                card_html = "\n".join(current_card_lines)
                
                # Check if it matches any priority product
                for prod in PRIORITY_PRODUCTS:
                    # Check specific title link or label to avoid false positives
                    # e.g. aria-label="Asad" or >Asad<
                    if f'aria-label="{prod.title()}"' in card_html or \
                       f'"{prod.title()}"' in card_html or \
                       f'>{prod.title()}<' in card_html or \
                       f'/{prod.replace(" ", "-")}.html' in card_html:
                           
                        # Double check specific exclusion for Yara
                        if prod == 'yara' and ('candy' in card_html.lower() or 'elixir' in card_html.lower() or 'moi' in card_html.lower() or 'tous' in card_html.lower()):
                            continue
                            
                        # If we haven't found this one yet, save it
                        if prod not in found_cards:
                            # Modify the wrapper class
                            swiper_html = card_html.replace('<div class="f-column card">', '<div class="f-column swiper-slide">', 1)
                            found_cards[prod] = swiper_html
    
    # Write output
    with open('priority_slides.html', 'w', encoding='utf-8') as f:
        # Enforce order
        for prod in PRIORITY_PRODUCTS:
            if prod in found_cards:
                f.write(found_cards[prod])
                f.write('\n')
            else:
                print(f"Warning: Could not find card for {prod}")

    print("Done. Check priority_slides.html")

if __name__ == '__main__':
    extract_cards()
