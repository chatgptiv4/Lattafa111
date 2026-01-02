import sys

def update_index():
    print("Reading index.html...")
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading index.html: {e}")
        return

    print("Reading priority_slides.html...")
    try:
        with open('priority_slides.html', 'r', encoding='utf-8') as f:
            new_slides = f.read()
    except Exception as e:
        print(f"Error reading priority_slides.html: {e}")
        return

    # Target class
    target_class = 'collection-item-slider__products swiper-wrapper'
    print(f"Searching for class: '{target_class}'")
    
    start_idx = content.find(target_class)
    if start_idx == -1:
        print("Could not find target class string.")
        return

    print(f"Found target class at index {start_idx}")

    # Find the opening <div before this class
    # We scan backwards safely
    tag_start = -1
    for i in range(start_idx, 0, -1):
        if content[i] == '<' and content[i+1:i+4] == 'div':
            tag_start = i
            break
            
    if tag_start == -1:
        print("Could not find <div tag start.")
        return
        
    print(f"Found <div start at {tag_start}")
    
    # Find the end of the opening tag >
    tag_end = content.find('>', start_idx) + 1
    print(f"Found > at {tag_end}")
    
    # Scan for matching closing div
    print("Scanning for matching closing div...")
    div_balance = 1
    end_idx = -1
    
    for i in range(tag_end, len(content)):
        # Optimization: verify start of tag
        if content[i] == '<':
            if content[i:i+4] == '<div':
                div_balance += 1
            elif content[i:i+5] == '</div':
                div_balance -= 1
            
            if div_balance == 0:
                end_idx = i
                break
    
    if end_idx == -1:
        print("Could not find matching closing div.")
        return
        
    print(f"Found matching </div> at {end_idx}")
    
    # Construct new content
    new_content = content[:tag_end] + '\n' + new_slides + '\n' + content[end_idx:]
    
    print("Writing index.html...")
    try:
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Successfully updated index.html")
    except Exception as e:
        print(f"Error writing file: {e}")

if __name__ == '__main__':
    update_index()
