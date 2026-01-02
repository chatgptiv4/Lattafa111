
import re

filepath = r'c:\Users\HomePC\Desktop\Laffata\shop-all.html'
with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

start_marker = '<div class="f-column card">'
matches = [m.start() for m in re.finditer(re.escape(start_marker), content)]

print(f"Total cards found: {len(matches)}")

def count_divs(text):
    opens = text.count('<div')
    closes = text.count('</div>')
    return opens, closes

for i in range(min(5, len(matches))):
    start = matches[i]
    if i < len(matches) - 1:
        end = matches[i+1]
    else:
        end = min(start + 5000, len(content)) # just check next chunk
    
    chunk = content[start:end]
    opens, closes = count_divs(chunk)
    
    print(f"Card {i+1}: Opens={opens}, Closes={closes}, Delta={opens-closes}")
    if opens != closes:
        print(f"!!! Card {i+1} is unbalanced (Delta {opens-closes})")
        # Print the end of the chunk to see what's missing
        print(f"Last 100 chars of Card {i+1}:")
        print(chunk[-100:].replace('\n', '\\n'))
