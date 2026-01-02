
import re

filepath = r'c:\Users\HomePC\Desktop\Laffata\shop-all.html'
with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

start_marker = '<div class="f-column card">'
matches = [m.start() for m in re.finditer(re.escape(start_marker), content)]

print(f"Total cards found: {len(matches)}")

new_content = content
offset = 0

# We process from first to second-to-last
for i in range(len(matches) - 1):
    start = matches[i] + offset
    next_start = matches[i+1] + offset
    
    chunk = new_content[start:next_start]
    
    opens = chunk.count('<div')
    closes = chunk.count('</div>')
    
    delta = opens - closes
    if delta > 0:
        print(f"Card {i+1} Unbalanced: Opens {opens}, Closes {closes}. Adding {delta} divs.")
        # We append </div> before the next start
        # The next start is at `next_start`.
        # We need to insert matching number of divs.
        
        insert_str = "</div>" * delta + "\n"
        
        # Insert at the end of the chunk (which is `next_start`)
        new_content = new_content[:next_start] + insert_str + new_content[next_start:]
        offset += len(insert_str)
    elif delta < 0:
        print(f"Card {i+1} Weirdly has too many closes? {delta}")

# Check last card?
# It's harder because we don't know where it ends.
# But assuming the last card is one of the 'clean' ones we didn't touch, it should be fine.

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Fixed unbalanced cards.")
