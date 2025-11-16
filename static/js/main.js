// ==================== GLOBAL VARIABLES ====================
let notificationDropdown = null;
let notificationIcon = null;
let cartBadge = null;

// ==================== INITIALIZATION ====================
document.addEventListener('DOMContentLoaded', function() {
    initNavigation();
    initFlashMessages();
    initNotifications();
    initCartBadge();
    initForms();
});

// ==================== NAVIGATION ====================
function initNavigation() {
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');
    
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!navToggle.contains(e.target) && !navMenu.contains(e.target)) {
                navMenu.classList.remove('active');
            }
        });
    }
}

// ==================== FLASH MESSAGES ====================
function initFlashMessages() {
    const flashMessages = document.querySelectorAll('.flash');
    
    flashMessages.forEach(flash => {
        const closeBtn = flash.querySelector('.flash-close');
        
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                flash.style.animation = 'slideOut 0.3s ease-out';
                setTimeout(() => flash.remove(), 300);
            });
        }
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            flash.style.animation = 'slideOut 0.3s ease-out';
            setTimeout(() => flash.remove(), 300);
        }, 5000);
    });
}

// ==================== NOTIFICATIONS ====================
function initNotifications() {
    notificationIcon = document.getElementById('notificationIcon');
    notificationDropdown = document.getElementById('notificationDropdown');
    
    if (notificationIcon && notificationDropdown) {
        notificationIcon.addEventListener('click', (e) => {
            e.stopPropagation();
            notificationDropdown.classList.toggle('active');
            if (notificationDropdown.classList.contains('active')) {
                loadNotifications();
            }
        });
        
        // Close dropdown when clicking outside
        document.addEventListener('click', (e) => {
            if (!notificationDropdown.contains(e.target) && !notificationIcon.contains(e.target)) {
                notificationDropdown.classList.remove('active');
            }
        });
        
        // Load notifications periodically
        loadNotifications();
        setInterval(loadNotifications, 30000); // Every 30 seconds
    }
}

async function loadNotifications() {
    try {
        const response = await fetch('/api/notifications');
        const data = await response.json();
        
        const badge = document.getElementById('notificationBadge');
        const list = document.getElementById('notificationList');
        
        if (badge) {
            badge.textContent = data.count;
            badge.style.display = data.count > 0 ? 'flex' : 'none';
        }
        
        if (list) {
            if (data.notifications.length === 0) {
                list.innerHTML = '<p class="no-notifications">No new notifications</p>';
            } else {
                list.innerHTML = data.notifications.map(n => `
                    <div class="notification-item" onclick="markNotificationRead(${n.id})">
                        <p>${n.message}</p>
                        <small style="color: var(--gray);">${n.created_at}</small>
                    </div>
                `).join('');
            }
        }
    } catch (error) {
        console.error('Error loading notifications:', error);
    }
}

async function markNotificationRead(notificationId) {
    try {
        await fetch(`/api/notification/read/${notificationId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        loadNotifications();
    } catch (error) {
        console.error('Error marking notification as read:', error);
    }
}

// ==================== CART ====================
function initCartBadge() {
    cartBadge = document.getElementById('cartBadge');
    if (cartBadge) {
        updateCartBadge();
    }
}

async function updateCartBadge() {
    try {
        const response = await fetch('/api/cart/count');
        const data = await response.json();
        
        if (cartBadge) {
            cartBadge.textContent = data.count;
            cartBadge.style.display = data.count > 0 ? 'flex' : 'none';
        }
    } catch (error) {
        console.error('Error updating cart badge:', error);
    }
}

async function addToCart(productId) {
    try {
        const response = await fetch(`/cart/add/${productId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast('Added to cart!', 'success');
            updateCartBadge();
        } else {
            showToast(data.message || 'Failed to add to cart', 'danger');
        }
    } catch (error) {
        console.error('Error adding to cart:', error);
        showToast('An error occurred', 'danger');
    }
}

async function updateCartQuantity(itemId, quantity) {
    try {
        const response = await fetch(`/cart/update/${itemId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify({ quantity })
        });
        
        const data = await response.json();
        
        if (data.success) {
            location.reload();
        } else {
            showToast(data.message || 'Failed to update cart', 'danger');
        }
    } catch (error) {
        console.error('Error updating cart:', error);
        showToast('An error occurred', 'danger');
    }
}

async function removeFromCart(itemId) {
    if (!confirm('Remove this item from cart?')) return;
    
    try {
        const response = await fetch(`/cart/remove/${itemId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast('Item removed', 'success');
            location.reload();
        } else {
            showToast(data.message || 'Failed to remove item', 'danger');
        }
    } catch (error) {
        console.error('Error removing from cart:', error);
        showToast('An error occurred', 'danger');
    }
}

// ==================== SHOP OWNER FUNCTIONS ====================
async function deleteProduct(productId) {
    if (!confirm('Are you sure you want to delete this product?')) return;
    
    try {
        const response = await fetch(`/shop/product/delete/${productId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast('Product deleted', 'success');
            location.reload();
        } else {
            showToast(data.message || 'Failed to delete product', 'danger');
        }
    } catch (error) {
        console.error('Error deleting product:', error);
        showToast('An error occurred', 'danger');
    }
}

async function updateOrderStatus(orderId, status) {
    try {
        const response = await fetch(`/shop/order/update-status/${orderId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ status })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast('Order status updated', 'success');
            location.reload();
        } else {
            showToast(data.message || 'Failed to update order', 'danger');
        }
    } catch (error) {
        console.error('Error updating order:', error);
        showToast('An error occurred', 'danger');
    }
}

// ==================== ADMIN FUNCTIONS ====================
async function toggleUser(userId) {
    try {
        const response = await fetch(`/admin/user/toggle/${userId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast('User status updated', 'success');
            location.reload();
        } else {
            showToast(data.message || 'Failed to update user', 'danger');
        }
    } catch (error) {
        console.error('Error toggling user:', error);
        showToast('An error occurred', 'danger');
    }
}

async function toggleShop(shopId) {
    try {
        const response = await fetch(`/admin/shop/toggle/${shopId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast('Shop status updated', 'success');
            location.reload();
        } else {
            showToast(data.message || 'Failed to update shop', 'danger');
        }
    } catch (error) {
        console.error('Error toggling shop:', error);
        showToast('An error occurred', 'danger');
    }
}

async function toggleProduct(productId) {
    try {
        const response = await fetch(`/admin/product/toggle/${productId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast('Product status updated', 'success');
            location.reload();
        } else {
            showToast(data.message || 'Failed to update product', 'danger');
        }
    } catch (error) {
        console.error('Error toggling product:', error);
        showToast('An error occurred', 'danger');
    }
}

// ==================== FORMS ====================
function initForms() {
    // Image preview
    const imageInputs = document.querySelectorAll('input[type="file"]');
    imageInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const preview = document.getElementById('imagePreview');
                    if (preview) {
                        preview.src = e.target.result;
                        preview.style.display = 'block';
                    }
                };
                reader.readAsDataURL(file);
            }
        });
    });
    
    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('error');
                } else {
                    field.classList.remove('error');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showToast('Please fill in all required fields', 'danger');
            }
        });
    });
}

// ==================== UTILITIES ====================
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `flash flash-${type}`;
    toast.innerHTML = `
        ${message}
        <button class="flash-close">&times;</button>
    `;
    
    let container = document.querySelector('.flash-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'flash-container';
        document.body.appendChild(container);
    }
    
    container.appendChild(toast);
    
    const closeBtn = toast.querySelector('.flash-close');
    closeBtn.addEventListener('click', () => {
        toast.remove();
    });
    
    setTimeout(() => {
        toast.remove();
    }, 5000);
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR'
    }).format(amount);
}

function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// ==================== SEARCH & FILTER ====================
function filterProducts() {
    const searchInput = document.getElementById('searchInput');
    const categorySelect = document.getElementById('categorySelect');
    
    if (searchInput || categorySelect) {
        const search = searchInput ? searchInput.value : '';
        const category = categorySelect ? categorySelect.value : '';
        
        const params = new URLSearchParams();
        if (search) params.append('search', search);
        if (category) params.append('category', category);
        
        window.location.href = `/products?${params.toString()}`;
    }
}

// ==================== MODAL ====================
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
    }
}

// Close modal when clicking outside
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal')) {
        e.target.classList.remove('active');
    }
});

// ==================== EXPORT FUNCTIONS ====================
window.addToCart = addToCart;
window.updateCartQuantity = updateCartQuantity;
window.removeFromCart = removeFromCart;
window.deleteProduct = deleteProduct;
window.updateOrderStatus = updateOrderStatus;
window.toggleUser = toggleUser;
window.toggleShop = toggleShop;
window.toggleProduct = toggleProduct;
window.filterProducts = filterProducts;
window.openModal = openModal;
window.closeModal = closeModal;
window.markNotificationRead = markNotificationRead;
