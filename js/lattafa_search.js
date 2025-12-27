document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.querySelector('.search__input');
    const searchResultsContainer = document.querySelector('#PredictiveSearchResults-sections--20292988698847__search-drawer');

    // Fallback if specific ID selector fails, try class based
    const secondaryResultsContainer = document.querySelector('.search__results');

    let products = [];

    // Fetch products on load
    fetch('/products.json')
        .then(response => response.json())
        .then(data => {
            products = data;
        })
        .catch(err => console.error('Error loading search index:', err));

    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase().trim();

            // Clear previous results
            if (searchResultsContainer) searchResultsContainer.innerHTML = '';

            if (query.length < 2) {
                // Determine if we should show recommendations or empty state?
                // For now, just keep empty
                return;
            }

            const filtered = products.filter(p => p.name.toLowerCase().includes(query));

            // Limit results
            const topResults = filtered.slice(0, 5);

            if (topResults.length > 0) {
                renderResults(topResults);
            } else {
                renderNoResults();
            }
        });
    }

    function renderResults(results) {
        const container = searchResultsContainer || secondaryResultsContainer;
        if (!container) return;

        const html = `
            <div class="predictive-search predictive-search--header" tabindex="-1" data-predictive-search="">
                <div class="predictive-search__results-groups-wrapper">
                    <div class="predictive-search__result-group">
                        <span class="predictive-search__item-heading h5 caption-with-letter-spacing-opacity">Products</span>
                        <ul class="predictive-search__results-list list-unstyled" role="listbox" aria-labelledby="predictive-search-products">
                            ${results.map(product => `
                                <li class="predictive-search__list-item" role="option">
                                    <a href="${product.url}" class="predictive-search__item predictive-search__item--link link link--text" tabindex="-1">
                                        ${product.image ? `<img class="predictive-search__image" src="${product.image}" alt="${product.name}" width="50" height="50">` : ''}
                                        <div class="predictive-search__item-content predictive-search__item-content--centered">
                                            <p class="predictive-search__item-heading h5">${product.name}</p>
                                            <div class="predictive-search__item-price">
                                                <span class="price-item price-item--regular">$${product.price}</span>
                                            </div>
                                        </div>
                                    </a>
                                </li>
                            `).join('')}
                        </ul>
                    </div>
                </div>
                <div class="predictive-search__loading-state" aria-hidden="true">
                    <svg aria-hidden="true" focusable="false" class="spinner" viewBox="0 0 66 66" xmlns="http://www.w3.org/2000/svg">
                        <circle class="path" fill="none" stroke-width="6" cx="33" cy="33" r="30"></circle>
                    </svg>
                </div>
            </div>
        `;

        container.innerHTML = html;
        container.classList.remove('hidden');
    }

    function renderNoResults() {
        const container = searchResultsContainer || secondaryResultsContainer;
        if (!container) return;

        container.innerHTML = `
            <div class="predictive-search__item-heading h5" style="padding: 1rem;">
                No products found
            </div>
        `;
    }
});
