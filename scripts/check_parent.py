
import re

filepath = r'c:\Users\HomePC\Desktop\Laffata\shop-all.html'
with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

start_marker = '<div class="f-column card">'
m = re.search(re.escape(start_marker), content)

if m:
    # Look backwards from the first card to find the parent container
    # We look for the nearest <div ...> before this.
    
    pre_content = content[:m.start()]
    # Find last <div tag
    last_div_idx = pre_content.rfind('<div')
    if last_div_idx != -1:
        parent_div = pre_content[last_div_idx:]
        # Get just the tag
        parent_tag = parent_div[:parent_div.find('>')+1]
        print(f"Parent tag seems to be: {parent_tag}")
        
        # Check if it has grid classes
        # Should be something like "f-grid" or "row"
        
        # Also let's check if there are any intervening closing divs?
        # Check text between parent and first card
        between = pre_content[last_div_idx + len(parent_tag):]
        if '</div>' in between:
            print("WARNING: There is a closing div between expected parent and first card!")
    else:
        print("Could not find parent div.")
else:
    print("Cards not found.")
