
import os
import re

template_path = r'c:\Users\HomePC\Desktop\Laffata\products\asad.html'
with open(template_path, 'r', encoding='utf-8') as f:
    template = f.read()

products = [
    {
        "name": "Choco Overdose",
        "slug": "choco-overdose",
        "price_new": "$45.00",
        "price_old": "$59.00",
        "discount": "-24%",
        "description": "Lattafa Choco Overdose is a decadent fragrance from the 'Give Me Gourmand Collection'. A wearable dessert fantasy capturing the aroma of molten chocolate and freshly baked cupcakes.",
        "top_notes": "Dark Chocolate Fudge",
        "middle_notes": "Cocoa Powder, Cupcake Accord",
        "base_notes": "Vanilla, Caramel, Benzoin"
    },
    {
        "name": "Berry on Top",
        "slug": "berry-on-top",
        "price_new": "$45.00",
        "price_old": "$59.00",
        "discount": "-24%",
        "description": "Lattafa's Berry on Top is a floral fruity gourmand scent, designed to be playful yet elegant, celebrating the irresistible sweetness of strawberries.",
        "top_notes": "Strawberry, Chantilly Cream",
        "middle_notes": "Cooked Sugar, Strawberry Jam, White Flowers",
        "base_notes": "Musk, Vanilla"
    },
    {
        "name": "Vanilla Freak",
        "slug": "vanilla-freak",
        "price_new": "$45.00",
        "price_old": "$59.00",
        "discount": "-24%",
        "description": "Lattafa Vanilla Freak is a captivating and unapologetically decadent gourmand fragrance that aims to take vanilla to its most indulgent extremes.",
        "top_notes": "Cupcake Accord",
        "middle_notes": "Almond, Sugar Frosting, Cinnamon",
        "base_notes": "Vanilla, Musk, Buttercream"
    },
    {
        "name": "Cookie Crave",
        "slug": "cookie-crave",
        "price_new": "$45.00",
        "price_old": "$59.00",
        "discount": "-24%",
        "description": "Lattafa Cookie Crave is a warm, irresistible gourmand fragrance that evokes the feeling of stepping into a warm bakery.",
        "top_notes": "Butter, Cocoa",
        "middle_notes": "Cookie, Milk, Sugar",
        "base_notes": "Vanilla, Whipped Cream, Sandalwood"
    },
    {
        "name": "Whipped Pleasure",
        "slug": "whipped-pleasure",
        "price_new": "$45.00",
        "price_old": "$59.00",
        "discount": "-24%",
        "description": "Lattafa Whipped Pleasure is a decadent gourmand fragrance with a sensual twist, designed for those who appreciate refined sweetness and dessert-like perfumes.",
        "top_notes": "Caramel Popcorn, Caramel, Salted Caramel",
        "middle_notes": "Creamy Milk, Jasmine",
        "base_notes": "Tonka Bean, Musk, Benzoin, Ambrofix"
    }
]

for p in products:
    content = template
    # Replace simple strings
    content = content.replace('Asad', p['name'])
    content = content.replace('asad', p['slug'])
    
    # Replace Price
    # Finding the price container block to replace exactly is tricky with simple replace if whitespace differs, 
    # but we know the structure from the read.
    # We'll use regex to be safe or just replace the specific values if they are unique enough?
    # Actually, the template has specific values: $28.00, $45.00, -38%.
    content = content.replace('$28.00', p['price_new'])
    content = content.replace('$45.00', p['price_old'])
    content = content.replace('-38%', p['discount'])
    
    # Replace Description
    # The description in asad.html is inside a <div class="descnew"><p> ... </p></div>
    # and <div class="notesfinal">...</div>
    # We'll use regex to clear the old description and inject new one.
    
    # Remove existing description content
    content = re.sub(r'<div class="descnew">\s*<p>.*?</p>\s*</div>', f'<div class="descnew"><p>{p["description"]}</p></div>', content, flags=re.DOTALL)
    
    # Remove existing notes
    # There are multiple notesfinal divs.
    # We'll construct the new notes HTML
    new_notes_html = f'''
                        <div class="notesfinal">
                            <p><strong>Top Notes</strong><br>{p["top_notes"]}</p>
                        </div>
                        <div class="notesfinal">
                            <p><strong>Middle Notes</strong><br>{p["middle_notes"]}</p>
                        </div>
                        <div class="notesfinal">
                            <p><strong>Base Notes</strong><br>{p["base_notes"]}</p>
                        </div>'''
    
    # Replace the block of notes. 
    # In template: 
    # <div class="notesfinal">...Top Notes...</div>
    # ...
    # <div class="notesfinal">...Base Notes...</div>
    
    # We can match from the first notesfinal to the last closing div of notesfinal
    content = re.sub(r'<div class="notesfinal">.*?Base Notes.*?</div>\s*</div>', f'{new_notes_html}</div>', content, flags=re.DOTALL)
    
    # Check for image count. The template has 0.jpg and 1.jpg hardcoded.
    # We should check how many images exist for the new product.
    img_dir = os.path.join(r'c:\Users\HomePC\Desktop\Laffata\assets\products', p['slug'])
    if os.path.exists(img_dir):
        images = [f for f in os.listdir(img_dir) if f.endswith('.jpg')]
        # Construct thumbnails HTML
        thumbs_html = '<div class="thumbnails">'
        for i in range(len(images)):
            active = ' active' if i == 0 else ''
            img_path = f'/assets/products/{p["slug"]}/{i}.jpg'
            thumbs_html += f'<div class="thumbnail{active}" onclick=\'changeImage("{img_path}", this)\'><img src="{img_path}" alt="{p["name"]}"></div>'
        thumbs_html += '</div>'
        
        # Replace thumbnails div
        content = re.sub(r'<div class="thumbnails">.*?</div>', thumbs_html, content, flags=re.DOTALL)
        
    # Write new file
    out_path = os.path.join(r'c:\Users\HomePC\Desktop\Laffata\products', f'{p["slug"]}.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created {out_path}")

