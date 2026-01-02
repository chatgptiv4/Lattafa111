
import re

filepath = r'c:\Users\HomePC\Desktop\Laffata\shop-all.html'
with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Find where the grid starts
start_marker = '<div class="f-column card">'
matches = [m.start() for m in re.finditer(re.escape(start_marker), content)]

print(f"Total cards found: {len(matches)}")

def count_divs(text):
    opens = text.count('<div')
    closes = text.count('</div>')
    return opens, closes

# We expect each card block to be balanced BEFORE the next card starts.
# Let's check the text BETWEEN matches.
for i in range(len(matches)):
    start = matches[i]
    if i < len(matches) - 1:
        end = matches[i+1]
    else:
        # Last card ... heuristic end?
        # Use find_closing_div logic to find where it SHOULD end
        end = len(content)
    
    chunk = content[start:end]
    opens, closes = count_divs(chunk)
    
    # Heuristic: The chunk includes the start of the card.
    # If it goes up to the next card, it should ideally be balanced if there is no wrapper between cards.
    # BUT, if we just sliced content[start:end], we included everything up to the next card.
    # The Grid list itself is a wrapper. Cards are siblings.
    # So chunk SHOULD contain exactly matched divs if cards are direct siblings with no other HTML in between.
    
    print(f"Card {i+1} (starts at {start}): Opens={opens}, Closes={closes}, Delta={opens-closes}")
    
    if opens != closes:
        print(f"--> MALFORMED CARD {i+1}?")
        # Let's print the last few chars of this chunk
        print(f"    Ends with: {chunk[-50:].replace('\n', ' ')}")

