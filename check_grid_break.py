
import re

filepath = r'c:\Users\HomePC\Desktop\Laffata\shop-all.html'
with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

start_marker = '<div class="f-column card">'
matches = [m.start() for m in re.finditer(re.escape(start_marker), content)]

for i in range(min(5, len(matches))):
    start = matches[i]
    if i < len(matches) - 1:
        end = matches[i+1]
    else:
        end = min(start + 5000, len(content))
    
    chunk = content[start:end]
    opens = chunk.count('<div')
    closes = chunk.count('</div>')
    
    print(f"Card {i+1}: Opens {opens}, Closes {closes}, Delta {opens-closes}")
    
    # Also check if maybe there is a closing div immediately after the card but BEFORE the next Match?
    # Our chunk captures everything up to next match.
    # If the Delta is 0, it means it's self-contained.
    # But if the cards are stacking, maybe they shouldn't be wrapped in "f-column"?
    # Or "f-column" is 100% width?
    
    # Let's check the CSS classes of these cards?
    # They are all <div class="f-column card">
