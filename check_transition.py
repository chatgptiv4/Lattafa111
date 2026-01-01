
import re

filepath = r'c:\Users\HomePC\Desktop\Laffata\shop-all.html'
with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Find Yara card
# We look for "Yara" inside a card structure
# Or simpler: Find "Yara" text, then find the NEXT card start.
# Assumption: Asad is first, Yara is second.

# Let's find "Yara"
yara_matches = [m.start() for m in re.finditer("Yara", content)]
# There might be many matches (collection, nav, etc).
# We want the one in the main grid.
# The main grid starts late in the file?
# Or did I inject them at the beginning of the file?
# My reorder script did: `new_file_content = content[:full_start] + new_grid_content + content[full_end:]`
# `full_start` was the FIRST card.
# So if the first card was at line 5000, that's where I injected.
# If the first card was at line 3700 (Featured Collection), I injected THERE.
# Wait!!
# If I injected into the Featured Collection (Swiper), then I BROKE the Swiper because Swiper expects `swiper-slide` class, but I injected `f-column card`.

Reflecting on `check_first_card.py` output (Step 482):
"First 'f-column card' found at line 9050 approx" (no it printed content that looked like grid card).
But `grep` found 25 cards.
In `reorder_shop_all.py`:
`start_indices = [m.start() for m in re.finditer(re.escape(card_start_marker), content)]`
If `card_start_marker` is `<div class="f-column card">`.

If the Featured Collection items were `swiper-slide promotion-item`... then `reorder_shop_all.py` would NOT have touched them.
UNLESS... those items *also* have nested `f-column card`?
View 471, line 3760: `<div class="product-card product-card-style-standard">`. NO `f-column card`.

So, the Main Grid (starting ~line 9000?) is where the `f-column card` resides.
So I injected my 10 priority cards at line ~9000.
So Asad, Yara, Qaed... are at line 9000+.

So, I need to check the transition between Yara (Card 2) and Qaed (Card 3) in the block starting at ~9000.

I will search for "Yara" followed by "Qaed Al Fursan" in that region.
