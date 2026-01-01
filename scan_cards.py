
import re

files = [r'c:\Users\HomePC\Desktop\Laffata\best-sellers.html']

for filepath in files:
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    lines = content.split('\n')
    stack = []
    
    # We want to identifying WHERE the imbalance starts.
    # It's hard because a missing </div> usually manifests at the end.
    # But if we track indentation or logical blocks?
    
    # Let's count divs in the Grid Section specifically.
    # Identified by `id="shopify-section-template...collection_list..."` or similar container.
    # In best-sellers.html, the loop starts around line 6047 `grid-list class="block"` ?
    
    print(f"Scanning {filepath}...")
    
    # Find the collection list container
    match_start = content.find('collection-list class="block')
    if match_start == -1:
        print("Could not find collection-list container.")
        continue

    # We will scan from there.
    # We expect a sequence of <div class="f-column card"> ... </div>
    
    # Let's verify each card individually.
    card_start_marker = '<div class="f-column card">'
    card_indices = [m.start() for m in re.finditer(re.escape(card_start_marker), content)]
    
    print(f"Found {len(card_indices)} cards.")
    
    bad_cards = []
    
    for i, start_idx in enumerate(card_indices):
        # We try to find the balancing closing div for THIS card
        # We scan forward.
        depth = 0
        found_end = False
        current_pos = start_idx
        
        # Limit scan to next card start or reasonable length to prevent runaway
        next_card_start = card_indices[i+1] if i+1 < len(card_indices) else len(content)
        
        # Actually, finding closing div logic:
        temp_depth = 0
        scan_cursor = start_idx
        
        while scan_cursor < len(content):
            # Find next tag
            next_open = content.find('<div', scan_cursor)
            next_close = content.find('</div>', scan_cursor)
            
            if next_close == -1:
                break # EOF
                
            if next_open != -1 and next_open < next_close:
                temp_depth += 1
                scan_cursor = next_open + 4
            else:
                temp_depth -= 1
                scan_cursor = next_close + 6
                if temp_depth == 0:
                    found_end = True
                    end_pos = scan_cursor
                    break
        
        if not found_end:
            print(f"Card {i} at index {start_idx} appears UNCLOSED.")
            bad_cards.append(i)
        elif end_pos > next_card_start:
             # This means the card overlaps with the next card! 
             # (i.e. we missed a closing div inside the card, so we consumed the next card's start as content)
             print(f"Card {i} at index {start_idx} OVERLAPS into Card {i+1} (End: {end_pos} > Next: {next_card_start})")
             bad_cards.append(i)
        else:
            pass
            # print(f"Card {i} OK.")

    if not bad_cards:
        print("All cards seem individually balanced (relative to each other).")
        # Then the issue might be the CONTAINER closing tags.
        # Check what follows the last card.
        last_card_start = card_indices[-1]
        
        # Check depth from start to last card end
        # ... logic ...
    else:
        print(f"Found {len(bad_cards)} potentially broken cards.")

