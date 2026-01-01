document.addEventListener('DOMContentLoaded', () => {
    console.log("Lattafa Adapter Loaded");

    // Remove User Account Elements (Aggressive)
    function removeUserElements() {
        // 1. Specific Selectors
        const selectors = [
            'a[href*="/account"]',
            'a[href*="/login"]',
            'a[href*="shopify.com/authentication"]',
            '.icon-user',
            '.fa-user',
            '.header__icon--account',
            '.localization-form__currency'
        ];

        selectors.forEach(selector => {
            const elements = document.querySelectorAll(selector);
            elements.forEach(el => el.remove());
        });

        // 2. SVG-based detection (if classes are missing)
        // Look for SVGs that might be the user icon by checking common path data or parent links
        const svgs = document.querySelectorAll('svg');
        svgs.forEach(svg => {
            // Check if it's inside a link
            const link = svg.closest('a');
            if (link) {
                const href = link.getAttribute('href') || '';
                // If link goes to account or login, OR if it's a specific Shopify auth link
                if (href.includes('account') || href.includes('login') || href.includes('authentication')) {
                    link.remove(); // Remove the whole link
                }
            }
        });

        // 3. Fallback: Search by "visual" or "aria" labels if possible (optional but good)
        // This targets the specific icon the user sees if it has "Log in" or similar text
        const links = document.querySelectorAll('a');
        links.forEach(a => {
            if (a.innerText.includes('Log in') || a.innerText.includes('Sign in') || a.getAttribute('aria-label')?.includes('Log in')) {
                a.remove();
            }
        });
    }

    // Run multiple times to catch delayed rendering
    removeUserElements();
    window.addEventListener('load', removeUserElements);
    setInterval(removeUserElements, 1000); // Poll every second just in case


    // Update "Shop All" Link
    function updateShopAllLink() {
        const links = document.querySelectorAll('a');
        links.forEach(a => {
            const text = a.innerText.trim().toUpperCase();
            if (text === 'SHOP ALL' || text === 'SHOP') {
                // Check if it's likely the main nav link (not a footer link perhaps? Or maybe all of them?)
                // User said "Under this Shop All", implying a specific one or the main one.
                // Safest to update all primary navigation ones, or just all of them if they are generic.
                // Let's check if it creates issues. Usually "Shop All" goes to collection.
                // We'll update it to gift-sets.html.
                a.href = 'gift-sets.html';
            }
        });
    }
    updateShopAllLink();
    window.addEventListener('load', updateShopAllLink);




    // Handle data-link attributes for summary and other elements
    document.addEventListener('click', (e) => {
        const target = e.target.closest('[data-link]');
        if (target) {
            const url = target.getAttribute('data-link');
            if (url) {
                window.location.href = url;
            }
        }
    });

    // 1. Initialize Cart State
    let cart = JSON.parse(localStorage.getItem('cart')) || [];

    // 2. Create Cart UI via JS (Sidebar)
    const cartSidebar = document.createElement('div');
    cartSidebar.className = 'cart-sidebar';
    cartSidebar.innerHTML = `
        <div class="cart-header">
            <h3>Shopping Bag</h3>
            <span class="close-cart">&times;</span>
        </div>
        <div class="cart-items">
            <!-- Items go here -->
        </div>
        <div class="cart-footer">
            <div class="total-price">
                <span>Total:</span>
                <span id="cart-total">$0.00</span>
            </div>
            <button class="btn-checkout">Checkout</button>
        </div>
    `;
    document.body.appendChild(cartSidebar);

    // 3. Create Floating Cart Icon
    const floatIcon = document.createElement('div');
    floatIcon.className = 'floating-cart-icon';
    floatIcon.innerHTML = `<i class="fa-solid fa-bag-shopping"></i><span class="floating-count">0</span>`;
    document.body.appendChild(floatIcon);

    // Event Listeners for Cart
    const closeBtn = cartSidebar.querySelector('.close-cart');

    function toggleCart() {
        cartSidebar.classList.toggle('open');
    }

    floatIcon.addEventListener('click', toggleCart);
    closeBtn.addEventListener('click', toggleCart);

    // Mobile Sticky Bar Cart Icon
    const mobileCartBtn = document.querySelector('.mobile-adapter-cart-btn');
    if (mobileCartBtn) {
        mobileCartBtn.addEventListener('click', (e) => {
            e.preventDefault();
            toggleCart();
        });
    }

    // Checkout Logic (Now handled by global hijacker)

    // Handle Success/Cancel messages from URL
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('success')) {
        alert("Payment Successful! Thank you for your order.");
        localStorage.removeItem('cart');
        cart = [];
        updateCart();
    } else if (urlParams.get('canceled')) {
        alert("Payment Canceled.");
    }

    // --- GLOBAL CHECKOUT HIJACKER ---
    // This intercepts clicks on any original "Checkout" buttons or forms
    async function handleStripeCheckout(e) {
        if (cart.length === 0) {
            alert("Your cart is empty!");
            if (e) e.preventDefault();
            return;
        }

        if (e) {
            e.preventDefault();
            e.stopPropagation();
        }

        const target = (e && e.target) ? e.target : checkoutBtn;
        const originalText = target ? (target.innerText || target.value || "Checkout") : "Checkout";

        if (target && (target.tagName === 'BUTTON' || target.tagName === 'INPUT')) {
            target.innerText = "Processing...";
            target.disabled = true;
        }

        try {
            // Determine API URL based on environment
            const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
            // If local, assume running separate backend on 4242. If production, use relative API path.
            // But wait, if they use 'vercel dev' locally, relative path also works. 
            // We'll prioritize relative path if we suspect we are on valid domain, but keep localhost:4242 fallback for specific local setup.

            let apiUrl = '/api/create-checkout-session';
            if (isLocal && window.location.port !== '3000') {
                // Assumption: If on localhost and NOT standard Vercel port, maybe just static HTML opening or LiveServer
                // Try the specific backend port if the relative one fails? 
                // Actually, let's try relative first, if it fails then we can't really fallback easily in one request without complexity.
                // Let's stick to a robust simple check:
                // If we are on the Vercel deployment (or similar), use relative.
                // If we are strictly on localhost, we might be using node server.js.
            }

            // Simplified approach: Use full URL if localhost to hit port 4242, else relative
            if (isLocal) {
                // Try to detect if we are served by the node server itself? No easy way.
                // Let's use the relative path as default for Vercel, and if it fails, the user gets the error.
                // BUT, user specifically had issue with localhost:4242 hardcoded.
                // We will change it to relative path for Vercel support.
                apiUrl = '/api/create-checkout-session';

                // However, for the user's local "node server.js" workflow, that server runs on 4242.
                // If the frontend is also served by that server (port 4242), then relative path works!
                // If frontend is Live Server (port 5500), relative path '/api/...' hits port 5500 which is 404.

                if (window.location.port !== '4242' && window.location.port !== '') {
                    // Likely Live Server or similar
                    apiUrl = 'http://localhost:4242/create-checkout-session';
                }
            }

            // Override for production to ALWAYS use relative, just in case
            if (!isLocal) {
                apiUrl = '/api/create-checkout-session';
            }

            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ items: cart }),
            });

            const session = await response.json();
            if (session.url) {
                window.location.href = session.url;
            } else {
                alert("Checkout error: " + (session.error || "Unknown error"));
                if (target && (target.tagName === 'BUTTON' || target.tagName === 'INPUT')) {
                    target.innerText = originalText;
                    target.disabled = false;
                }
            }
        } catch (error) {
            console.error("Checkout Request Failed:", error);
            alert("Checkout failed. Make sure the backend server (node server.js) is running on port 4242.");
            if (target && (target.tagName === 'BUTTON' || target.tagName === 'INPUT')) {
                target.innerText = originalText;
                target.disabled = false;
            }
        }
    }

    // Listen for any click on a "checkout" named button
    document.addEventListener('click', (e) => {
        if (e.target.closest('button[name="checkout"], input[name="checkout"], .btn-checkout')) {
            handleStripeCheckout(e);
        }
    }, true);

    // Listen for any form submission that goes to /cart or /checkout
    document.addEventListener('submit', (e) => {
        const action = e.target.getAttribute('action');
        if (action) {
            // Hijack Checkout
            if ((action.includes('/cart') || action.includes('/checkout'))) {
                // Only hijack if it's a checkout-related submission (Shopify uses /cart for checkout too)
                if (e.submitter && e.submitter.name === 'checkout' || e.target.querySelector('[name="checkout"]')) {
                    handleStripeCheckout(e);
                    return;
                }
            }

            // Hijack Add To Cart (Native Forms) to use Local Cart
            if (action.includes('/cart/add')) {
                e.preventDefault();
                e.stopPropagation();

                // Get Product Info from Form Context
                const form = e.target;
                const card = form.closest('.product-card') || document.querySelector('.product-info');

                if (!card) return;

                // Extract Details
                const titleEl = card.querySelector('.product-card__title a') ||
                    card.querySelector('.product-card__title') ||
                    card.querySelector('.h3 a') ||
                    card.querySelector('h1') || // Product page title
                    card.querySelector('h3');

                const priceEl = card.querySelector('.price-new') ||
                    card.querySelector('.f-price-item--sale') ||
                    card.querySelector('.f-price-item--regular') ||
                    card.querySelector('.price-item--regular') ||
                    card.querySelector('.price__regular .price-item');

                const imgEl = card.querySelector('img.motion-reduce') ||
                    card.querySelector('img');

                if (titleEl) {
                    const title = titleEl.innerText.trim();

                    // Double check sold out status just in case
                    if (isSoldOut && isSoldOut(title)) {
                        alert("This item is currently Sold Out.");
                        return;
                    }

                    const priceStr = priceEl ? priceEl.innerText : "$0.00";
                    const price = parseFloat(priceStr.replace(/[^0-9.]/g, '')) || 0;

                    let imgSrc = imgEl ? imgEl.src : '';
                    if (imgSrc.startsWith('//')) imgSrc = 'https:' + imgSrc;

                    addToCart({
                        id: title.replace(/\s+/g, '-').toLowerCase(),
                        name: title,
                        price: price,
                        image: imgSrc,
                        quantity: 1
                    });
                    toggleCart();
                }
            }
        }
    }, true);
    // --------------------------------

    // 4. Inject "Add to Cart" Buttons into Product Cards
    const PRIORITY_PRODUCTS = [
        "asad", "yara", "qaed al fursan", "badee al oud noble blush",
        "khamrah", "choco overdose", "berry on top", "vanilla freak",
        "cookie crave", "whipped pleasure"
    ];

    const EXCLUDED_VARIANTS = [
        "tous", "moi", "candy", "zanzibar", "unlimited", "untamed", "qahwa", "dukhan", "sublime", "amethyst", "honor & glory"
    ];

    function isSoldOut(name) {
        if (!name) return true;
        const lowerName = name.toLowerCase();

        // 1. Check for Excluded Variants (Blacklist)
        if (EXCLUDED_VARIANTS.some(variant => lowerName.includes(variant))) {
            return true; // Sold Out
        }

        // 2. Check for Priority Products (Whitelist)
        // Return TRUE (Sold Out) if the name does NOT contain any of the priority keywords
        return !PRIORITY_PRODUCTS.some(keyword => lowerName.includes(keyword));
    }

    function injectAddToCartButtons() {
        const products = document.querySelectorAll('.product-card:not(.buttons-injected)');
        products.forEach(card => {
            card.classList.add('buttons-injected');

            // Extract Data - Improved Selectors
            const titleEl = card.querySelector('.product-card__title a') ||
                card.querySelector('.product-card__title') ||
                card.querySelector('.h3 a') ||
                card.querySelector('h3');

            const priceEl = card.querySelector('.price-new') ||
                card.querySelector('.f-price-item--sale') ||
                card.querySelector('.f-price-item--regular') ||
                card.querySelector('.f-price-item') ||
                card.querySelector('.price-item--regular');

            const imgEl = card.querySelector('img.motion-reduce') ||
                card.querySelector('img');

            if (titleEl) {
                const btn = document.createElement('button');
                btn.className = 'btn-lattafa-add';
                const prodName = titleEl.innerText.trim();

                if (isSoldOut(prodName)) {
                    btn.innerText = 'Sold Out';
                    btn.disabled = true;
                    btn.style.backgroundColor = '#ccc';
                    btn.style.cursor = 'not-allowed';
                    btn.style.opacity = '0.7';
                } else {
                    btn.innerText = 'Add to Cart';
                }

                // Layout: Insert after price info or at the end of info div
                const infoDiv = card.querySelector('.product-card__info') ||
                    card.querySelector('.product-info') ||
                    card;

                infoDiv.appendChild(btn);

                // Click Handler
                btn.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();

                    const title = titleEl.innerText.trim();
                    const priceStr = priceEl ? priceEl.innerText : "$0.00";
                    const price = parseFloat(priceStr.replace(/[^0-9.]/g, '')) || 0;

                    // Handle image URL
                    let imgSrc = imgEl ? imgEl.src : '';
                    if (imgSrc.startsWith('//')) imgSrc = 'https:' + imgSrc;

                    addToCart({
                        id: title.replace(/\s+/g, '-').toLowerCase(),
                        name: title,
                        price: price,
                        image: imgSrc,
                        quantity: 1
                    });
                    toggleCart(); // Show cart
                });
            }
        });

        // NEW: Handle Single Product Page Button
        const productPageBtn = document.querySelector('.product-info .add-to-cart-btn');
        if (productPageBtn && !productPageBtn.dataset.listenerAttached) {
            productPageBtn.dataset.listenerAttached = "true";
            productPageBtn.addEventListener('click', (e) => {
                e.preventDefault();

                // scrape details from page
                const titleEl = document.querySelector('h1.product__title');
                const priceEl = document.querySelector('.product-price-container .price-new') || document.querySelector('.product-price .price-regular');
                const imgEl = document.querySelector('#mainImage');

                if (titleEl && priceEl) {
                    const title = titleEl.innerText.trim();
                    const priceStr = priceEl.innerText.trim();
                    const price = parseFloat(priceStr.replace(/[^0-9.]/g, '')) || 0;
                    const imgSrc = imgEl ? imgEl.src : '';

                    addToCart({
                        id: window.location.pathname.split('/').pop().replace('.html', ''),
                        name: title,
                        price: price,
                        image: imgSrc,
                        quantity: 1
                    });
                    toggleCart();
                }
            });
        }
    }

    // 5. Force Enable Native Buttons for Priority Products (Aggressive Override)
    function forceEnablePriorityButtons() {
        const products = document.querySelectorAll('.product-card');
        products.forEach(card => {
            const titleEl = card.querySelector('.product-card__title a') ||
                card.querySelector('.product-card__title') ||
                card.querySelector('.h3 a') ||
                card.querySelector('h3');

            if (!titleEl) return;
            const title = titleEl.innerText.trim();

            // Check if Priority
            const isPriority = PRIORITY_PRODUCTS.some(keyword => title.toLowerCase().includes(keyword));

            // Check exclusion for safety (e.g. Yara Candy vs Yara)
            const isExcluded = EXCLUDED_VARIANTS.some(variant => title.toLowerCase().includes(variant));

            if (isPriority && !isExcluded) {
                // A. Find Native Button
                const nativeBtn = card.querySelector('button[name="add"]');
                const nativeTextSpan = card.querySelector('.product-card__atc-text');

                if (nativeBtn) {
                    // Force Enable
                    if (nativeBtn.disabled || nativeBtn.getAttribute('disabled') === '' || nativeBtn.classList.contains('disabled')) {
                        nativeBtn.disabled = false;
                        nativeBtn.removeAttribute('disabled');
                        nativeBtn.classList.remove('disabled');
                    }

                    // Force Text
                    if (nativeTextSpan) {
                        if (nativeTextSpan.innerText.trim().toUpperCase() === 'SOLD OUT') {
                            nativeTextSpan.innerText = 'Add to Cart';
                        }
                    } else if (nativeBtn.innerText.includes('Sold Out')) {
                        nativeBtn.innerText = 'Add to Cart';
                    }
                }

                // B. Find Injected Button (The one under the image)
                const injectedBtn = card.querySelector('.btn-lattafa-add');
                if (injectedBtn) {
                    if (injectedBtn.disabled || injectedBtn.innerText === 'Sold Out') {
                        injectedBtn.disabled = false;
                        injectedBtn.innerText = 'Add to Cart';
                        // Reset styles to match active state (black bg)
                        injectedBtn.style.backgroundColor = '';
                        injectedBtn.style.cursor = '';
                        injectedBtn.style.opacity = '';
                    }
                }
            }
        });
    }

    // Run force enable periodically
    setInterval(forceEnablePriorityButtons, 1000);
    window.addEventListener('load', forceEnablePriorityButtons);

    // Initial injection
    injectAddToCartButtons();

    // Use MutationObserver for dynamically loaded products
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            if (mutation.addedNodes.length) {
                injectAddToCartButtons();
            }
        });
    });

    observer.observe(document.body, {
        childList: true,
        subtree: true
    });

    // Cart Logic
    function addToCart(product) {
        const existing = cart.find(item => item.id === product.id);
        if (existing) {
            existing.quantity++;
        } else {
            cart.push(product);
        }
        updateCart();
    }

    function removeFromCart(id) {
        cart = cart.filter(item => item.id !== id);
        updateCart();
    }

    function updateCart() {
        localStorage.setItem('cart', JSON.stringify(cart));
        renderCart();
        if (typeof renderCartPage === 'function') renderCartPage();
    }

    function renderCart() {
        const itemsContainer = cartSidebar.querySelector('.cart-items');
        const countBadge = floatIcon ? floatIcon.querySelector('.floating-count') : null;
        const totalEl = document.getElementById('cart-total');

        if (!itemsContainer) return;

        itemsContainer.innerHTML = '';
        let total = 0;
        let count = 0;

        cart.forEach(item => {
            total += item.price * item.quantity;
            count += item.quantity;

            const div = document.createElement('div');
            div.className = 'cart-item';
            div.innerHTML = `
                <img src="${item.image}" alt="${item.name}">
                <div class="item-details">
                    <h4>${item.name}</h4>
                    <span class="item-price">$${item.price.toFixed(2)} x ${item.quantity}</span>
                </div>
                <span class="remove-item" style="cursor:pointer; color:red; margin-left:auto;">&times;</span>
            `;

            div.querySelector('.remove-item').addEventListener('click', () => removeFromCart(item.id));
            itemsContainer.appendChild(div);
        });

        if (countBadge) countBadge.innerText = count;
        if (totalEl) totalEl.innerText = '$' + total.toFixed(2);
    }

    // --- NEW: Full Cart Page Logic ---
    function updateQuantity(id, delta) {
        const item = cart.find(i => i.id === id);
        if (item) {
            item.quantity += delta;
            if (item.quantity <= 0) {
                removeFromCart(id);
            } else {
                updateCart();
            }
        }
    }

    function renderCartPage() {
        const container = document.getElementById('main-cart-items');
        const emptyMsg = document.getElementById('cart-empty-message');
        const wrapper = document.getElementById('cart-items-wrapper');
        const subtotalEl = document.getElementById('cart-page-subtotal');
        // Mobile checkout button
        const checkoutBtn = document.getElementById('cart-page-checkout-btn');

        if (!container) return; // Not on cart page

        if (cart.length === 0) {
            if (emptyMsg) emptyMsg.classList.remove('hidden');
            if (wrapper) wrapper.classList.add('hidden');
            return;
        }

        if (emptyMsg) emptyMsg.classList.add('hidden');
        if (wrapper) wrapper.classList.remove('hidden');

        container.innerHTML = '';
        let total = 0;

        cart.forEach(item => {
            const itemTotal = item.price * item.quantity;
            total += itemTotal;

            const row = document.createElement('div');
            row.className = 'cart-page-item flex flex-col md:flex-row items-center border-b py-4 gap-4';
            row.innerHTML = `
                <div class="w-full md:w-1/2 flex items-center gap-4">
                    <img src="${item.image}" alt="${item.name}" class="w-20 h-20 object-cover rounded aspect-square">
                    <div>
                        <h4 class="font-bold text-sm md:text-base">${item.name}</h4>
                        <p class="text-sm text-gray-500">$${item.price.toFixed(2)}</p>
                    </div>
                </div>
                <div class="w-full md:w-1/4 flex justify-between md:justify-center items-center">
                    <span class="md:hidden text-sm font-semibold">Qty:</span>
                    <div class="flex items-center border rounded">
                        <button class="px-3 py-1 hover:bg-gray-100 btn-decrease" data-id="${item.id}">-</button>
                        <span class="px-3 text-sm">${item.quantity}</span>
                        <button class="px-3 py-1 hover:bg-gray-100 btn-increase" data-id="${item.id}">+</button>
                    </div>
                </div>
                <div class="w-full md:w-1/4 flex justify-between md:justify-end items-center">
                    <span class="md:hidden text-sm font-semibold">Total:</span>
                    <span class="font-bold">$${itemTotal.toFixed(2)}</span>
                </div>
                <button class="ml-4 text-red-500 hover:text-red-700 btn-remove hidden md:block" title="Remove Item" data-id="${item.id}">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                </button>
            `;

            // Add listeners
            row.querySelector('.btn-decrease').addEventListener('click', () => updateQuantity(item.id, -1));
            row.querySelector('.btn-increase').addEventListener('click', () => updateQuantity(item.id, 1));
            const rmBtn = row.querySelector('.btn-remove');
            if (rmBtn) rmBtn.addEventListener('click', () => removeFromCart(item.id));

            container.appendChild(row);
        });

        if (subtotalEl) subtotalEl.innerText = '$' + total.toFixed(2);

        // Ensure checkout button works
        if (checkoutBtn) {
            checkoutBtn.addEventListener('click', (e) => {
                // Trigger the global hijacker if it doesn't pick it up automatically
                // But since we added a click listener on document for 'button[name="checkout"]', 
                // we should maybe give this button that name or call handleStripeCheckout directly.
                e.preventDefault();
                window.handleStripeCheckout(e);
            });
        }
    }

    // Expose to window
    window.renderCartPage = renderCartPage;
    // Expose handleStripeCheckout for the explicit button listener above
    window.handleStripeCheckout = handleStripeCheckout;

    // Initial Render
    renderCart();
});

