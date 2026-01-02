
import re

filepath = r'c:\Users\HomePC\Desktop\Laffata\shop-all.html'
with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

start_marker = '<div class="f-column card">'
m = re.search(re.escape(start_marker), content)

if m:
    start_idx = m.start()
    # Count lines before
    line_no = content[:start_idx].count('\n') + 1
    print(f"First 'f-column card' found at line {line_no}")
    
    # Let's extract this card and print the last few lines of it
    # We will assume it ends at the next card start or some heuristic
    
    # Check next card
    m2 = re.search(re.escape(start_marker), content[start_idx+1:])
    if m2:
        end_idx = start_idx + 1 + m2.start()
        chunk = content[start_idx:end_idx]
        print(f"Card 1 length: {len(chunk)}")
        print("--- End of Card 1 ---")
        print(chunk[-200:])
        
        # Check balance
        opens = chunk.count('<div')
        closes = chunk.count('</div>')
        print(f"Opens: {opens}, Closes: {closes}")
    else:
        print("Only 1 card found?")

else:
    print("No 'f-column card' found.")
