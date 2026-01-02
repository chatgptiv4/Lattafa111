
import re

filepath = r'c:\Users\HomePC\Desktop\Laffata\shop-all.html'
with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# We know the grid starts around line 9000.
# Let's start searching from valid grid start.
start_marker = '<div class="f-column card">'
m_grid = re.search(re.escape(start_marker), content)
if not m_grid:
    print("Grid not found.")
    exit()

grid_content = content[m_grid.start():]

# Find Yara
m_yara = re.search(r'href="[^"]*yara\.html"', grid_content)
if not m_yara:
    print("Yara not found in grid.")
    exit()

# Find Qaed
m_qaed = re.search(r'href="[^"]*qaed-al-fursan-unlimited\.html"', grid_content)
if not m_qaed:
    print("Qaed not found in grid.")
    # Maybe try text search?
    m_qaed = re.search(r'Qaed Al Fursan', grid_content)
    if not m_qaed:
        print("Qaed text not found in grid.")
        exit()

yara_idx = m_yara.start()
qaed_idx = m_qaed.start()

print(f"Yara link at {yara_idx}, Qaed link at {qaed_idx}")

# Extract chunk between them
# Yara is inside a card. We want the END of Yara's card and START of Qaed's card.
# The `yara_idx` is inside the href.
# We need to find the closing `</div>` of the Yara card.
# And verify what's between it and the `<div class="f-column card">` of Qaed.

# Logic: From yara_idx, find next `<div class="f-column card">`.
# The text BEFORE that new card is the "between" text.

card_matches = [m.start() for m in re.finditer(re.escape(start_marker), grid_content)]

# Find which card Yara belongs to
yara_card_idx = -1
for i, start in enumerate(card_matches):
    if start > yara_idx:
        break
    if start <= yara_idx:
        yara_card_idx = i

if yara_card_idx == -1:    print("weird"); exit()

print(f"Yara seems to be Card {yara_card_idx + 1}")

# Get content of Yara Card + boundary
start_yara = card_matches[yara_card_idx]
if yara_card_idx + 1 < len(card_matches):
    start_next = card_matches[yara_card_idx+1]
else:
    start_next = len(grid_content)

chunk = grid_content[start_yara:start_next]
print(f"Chunk length: {len(chunk)}")
print("--- End of Yara Card Chunk ---")
print(chunk[-200:].replace('\n', '\\n'))

opens = chunk.count('<div')
closes = chunk.count('</div>')
print(f"Opens {opens}, Closes {closes}")
