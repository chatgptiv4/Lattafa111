
import re

files = [
    r'c:\Users\HomePC\Desktop\Laffata\shop-all.html',
    r'c:\Users\HomePC\Desktop\Laffata\best-sellers.html'
]

def check_structure(filepath):
    print(f"Checking {filepath}...")
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Simple check: count divs
    open_divs = content.count('<div')
    close_divs = content.count('</div>')
    
    # This is a crude check because comments/strings might interfere, but decent first pass.
    # A better check is to iterate stack.
    
    stack = []
    lines = content.split('\n')
    
    error_found = False
    
    # Simple scanner for tags
    # regex for tags: </?div[^>]*>
    tag_pattern = re.compile(r'</?div[^>]*>', re.IGNORECASE)
    
    matches = [m for m in tag_pattern.finditer(content)]
    
    depth = 0
    for m in matches:
        tag = m.group(0)
        if tag.lower().startswith('<div'):
            depth += 1
        else:
            depth -= 1
        
        if depth < 0:
            # We closed more than opened!
            # Find line number
            char_pos = m.start()
            line_num = content[:char_pos].count('\n') + 1
            print(f"ERROR: Extra closing div at line {line_num}")
            error_found = True
            break
            
    if depth != 0 and not error_found:
        print(f"ERROR: Unbalanced divs. Final depth: {depth} (Positive means unclosed, Negative means extra closed)")
        error_found = True
    
    if not error_found:
        print("Structure seems OK (balanced divs).")
    else:
        print("Structure BROKEN.")

    print(f"Total <div: {open_divs}")
    print(f"Total </div: {close_divs}")
    print("-" * 20)

for f in files:
    check_structure(f)
