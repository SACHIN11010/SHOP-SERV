// Cart functionality
async function addToCart(productId, quantity = 1) {
    try {
        const response = await fetch(`/api/cart/add/product/${productId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify({ quantity })
        });

        const data = await response.json();
        
        if (data.success) {
            updateCartCount(data.cart_count || 0);
            showToast('Product added to cart', 'success');
            return true;
        } else {
            showToast(data.message || 'Failed to add to cart', 'error');
            return false;
        }
    } catch (error) {
        console.error('Error adding to cart:', error);
        showToast('An error occurred. Please try again.', 'error');
        return false;
    }
}

async function updateCartItem(itemId, itemType, newQuantity) {
    try {
        const endpoint = `/api/cart/update/${itemType}/${itemId}`;
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify({ quantity: newQuantity })
        });
        
        const data = await response.json();
        
        if (data.success) {
            updateItemTotal(itemId, itemType, newQuantity);
            updateCartTotals(data.cart || {});
            showToast('Cart updated successfully', 'success');
            return true;
        } else {
            showToast(data.message || 'Failed to update cart', 'error');
            return false;
        }
    } catch (error) {
        console.error('Error updating cart:', error);
        showToast('An error occurred. Please try again.', 'error');
        return false;
    }
}

// Remove item from cart
async function removeFromCart(itemId, itemType) {
    if (!confirm('Are you sure you want to remove this item from your cart?')) {
        return false;
    }

    try {
        const endpoint = `/api/cart/remove/${itemType}/${itemId}`;
        const response = await fetch(endpoint, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            const itemElement = document.getElementById(`${itemType}-item-${itemId}`);
            if (itemElement) {
                itemElement.remove();
                updateCartTotals(data.cart || {});
                updateCartCount(data.cart_count || 0);
                showToast('Item removed from cart', 'success');
                
                // If cart is empty, reload the page
                if (data.cart_count === 0) {
                    window.location.reload();
                }
            }
            return true;
        } else {
            showToast(data.message || 'Failed to remove item', 'error');
            return false;
        }
    } catch (error) {
        console.error('Error removing item:', error);
        showToast('An error occurred. Please try again.', 'error');
        return false;
    }
}

// Update cart count in navbar
function updateCartCount(count) {
    const cartCountElements = document.querySelectorAll('.cart-count');
    cartCountElements.forEach(el => {
        el.textContent = count;
        el.classList.toggle('hidden', count === 0);
    });
}

// Update the total for a specific item
function updateItemTotal(itemId, itemType, quantity) {
    const itemTotal = document.querySelector(`[data-item-id="${itemId}"].item-total`);
    if (itemTotal) {
        const price = parseFloat(itemTotal.dataset.price);
        itemTotal.textContent = `₹${(price * quantity).toFixed(2)}`;
    }
}

// Update cart totals in the UI
function updateCartTotals(cartData) {
    // Update subtotal
    if (cartData.subtotal !== undefined) {
        const subtotalElement = document.getElementById('cart-subtotal');
        if (subtotalElement) {
            subtotalElement.textContent = `₹${cartData.subtotal.toFixed(2)}`;
        }
    }
    
    // Update total
    if (cartData.total !== undefined) {
        const totalElement = document.getElementById('cart-total');
        if (totalElement) {
            totalElement.textContent = `₹${cartData.total.toFixed(2)}`;
        }
    }
    
    // Update item count in cart icon
    if (cartData.item_count !== undefined) {
        const cartCountElement = document.getElementById('cart-count');
        if (cartCountElement) {
            cartCountElement.textContent = cartData.item_count;
            cartCountElement.classList.toggle('hidden', cartData.item_count === 0);
        }
    }
}

// Show toast notification
function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toast-container');
    if (!toastContainer) return;
    
    const toast = document.createElement('div');
    const toastId = 'toast-' + Date.now();
    toast.id = toastId;
    
    toast.className = `p-4 mb-2 rounded-md shadow-lg ${
        type === 'success' ? 'bg-green-100 text-green-800' : 
        type === 'error' ? 'bg-red-100 text-red-800' :
        'bg-blue-100 text-blue-800'
    }`;
    
    toast.role = 'alert';
    
    // Add message and close button
    toast.innerHTML = `
        <div class="flex items-center justify-between">
            <div class="flex items-center">
                ${type === 'success' ? '✅' : type === 'error' ? '❌' : 'ℹ️'}
                <span class="ml-2">${message}</span>
            </div>
            <button type="button" class="ml-4 text-gray-500 hover:text-gray-700" onclick="document.getElementById('${toastId}').remove()">
                <span class="sr-only">Close</span>
                <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
            </button>
        </div>
    `;
    
    // Add to container
    toastContainer.appendChild(toast);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        const toastElement = document.getElementById(toastId);
        if (toastElement) {
            toastElement.remove();
        }
    }, 5000);
}

// Function to get CSRF token
function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]')?.content || '';
}

// Function to make AJAX requests
async function makeRequest(url, method = 'GET', data = {}) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        credentials: 'same-origin'
    };

    if (method !== 'GET' && method !== 'HEAD') {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(url, options);
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.message || 'Request failed');
        }
        return await response.json();
    } catch (error) {
        console.error('Request failed:', error);
        showToast('An error occurred. Please try again.', 'error');
        throw error;
    }
}

// Initialize cart functionality when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Event delegation for quantity updates
    document.addEventListener('click', async function(e) {
        // Handle quantity increase/decrease
        const updateBtn = e.target.closest('.update-quantity');
        if (updateBtn) {
            e.preventDefault();
            const itemId = updateBtn.dataset.itemId;
            const itemType = updateBtn.dataset.itemType;
            const action = updateBtn.dataset.action;
            const input = document.querySelector(`#${itemType === 'product' ? 'quantity' : 'service-quantity'}-${itemId}`);
            
            if (!input) return;
            
            let newQuantity = parseInt(input.value) || 1;
            
            if (action === 'increase') {
                newQuantity++;
            } else if (action === 'decrease' && newQuantity > 1) {
                newQuantity--;
            }
            
            input.value = newQuantity;
            await updateCartItem(itemId, itemType, newQuantity);
        }
        
        // Handle remove item
        const removeBtn = e.target.closest('.remove-item');
        if (removeBtn) {
            e.preventDefault();
            const itemId = removeBtn.dataset.itemId;
            const itemType = removeBtn.dataset.itemType;
            
            if (confirm('Are you sure you want to remove this item from your cart?')) {
                await removeCartItem(itemId, itemType);
            }
        }
    });
    
    // Handle direct input changes
    document.addEventListener('change', async function(e) {
        const quantityInput = e.target.closest('input[type="number"][data-item-id]');
        if (quantityInput) {
            const itemId = quantityInput.dataset.itemId;
            const itemType = quantityInput.dataset.itemType;
            let newQuantity = parseInt(quantityInput.value) || 1;
            
            if (newQuantity < 1) {
                newQuantity = 1;
                quantityInput.value = 1;
            }
            
            await updateCartItem(itemId, itemType, newQuantity);
        }
    });
});
