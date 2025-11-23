// Initialize when DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize form elements
    const form = document.getElementById('checkoutForm');
    const paymentMethodRadios = document.querySelectorAll('input[name="payment_method"]');
    const qrCodeSection = document.getElementById('qrCodeSection');
    const placeOrderButton = document.getElementById('place-order-button');
    const termsCheckbox = document.getElementById('termsCheckbox');
    const termsAccepted = document.getElementById('terms_accepted');
    
    // Handle payment method change
    function handlePaymentMethodChange() {
        const selectedMethod = document.querySelector('input[name="payment_method"]:checked');
        if (selectedMethod && qrCodeSection) {
            qrCodeSection.style.display = selectedMethod.value === 'qr' ? 'block' : 'none';
        }
    }

    // Initialize payment method listeners
    if (paymentMethodRadios && paymentMethodRadios.length) {
        paymentMethodRadios.forEach(method => {
            method.addEventListener('change', handlePaymentMethodChange);
        });
        // Initial check
        handlePaymentMethodChange();
    }

    // Update terms accepted hidden field
    if (termsCheckbox && termsAccepted) {
        termsCheckbox.addEventListener('change', function() {
            termsAccepted.value = this.checked ? 'true' : 'false';
            this.setCustomValidity('');
        });
    }

    // Form submission handler
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // Reset previous errors
            const errorElements = form.querySelectorAll('.is-invalid');
            errorElements.forEach(el => el.classList.remove('is-invalid'));
            
            // Update hidden address fields
            const fullName = document.getElementById('full_name');
            const email = document.getElementById('email');
            const phone = document.getElementById('phone');
            const address = document.getElementById('address');
            const cityInput = document.getElementById('city');
            const stateInput = document.getElementById('state');
            const zipInput = document.getElementById('zip_code');
            const paymentMethod = document.querySelector('input[name="payment_method"]:checked');
            
            // Validate required fields
            const requiredFields = [
                { element: fullName, name: 'Full Name' },
                { element: email, name: 'Email' },
                { element: phone, name: 'Phone' },
                { element: address, name: 'Address' },
                { element: cityInput, name: 'City' },
                { element: stateInput, name: 'State' },
                { element: zipInput, name: 'ZIP Code' },
                { element: paymentMethod, name: 'Payment Method' }
            ];
            
            let isValid = true;
            requiredFields.forEach(field => {
                if (!field.element || !field.element.value.trim()) {
                    showNotification(`Please fill in ${field.name}`, 'danger');
                    if (field.element) {
                        field.element.classList.add('is-invalid');
                        field.element.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }
                    isValid = false;
                }
            });
            
            if (!isValid) {
                return;
            }
            
            // Update hidden fields
            const shippingCity = document.getElementById('shipping_city');
            const shippingState = document.getElementById('shipping_state');
            const shippingZip = document.getElementById('shipping_zip');
            
            if (cityInput && shippingCity) shippingCity.value = cityInput.value;
            if (stateInput && shippingState) shippingState.value = stateInput.value;
            if (zipInput && shippingZip) shippingZip.value = zipInput.value;
            
            // Validate terms acceptance
            if (!termsCheckbox.checked) {
                showNotification('Please accept the terms and conditions', 'danger');
                termsCheckbox.scrollIntoView({ behavior: 'smooth', block: 'center' });
                return;
            }
            
            // Validate form
            if (!form.checkValidity()) {
                e.stopPropagation();
                form.classList.add('was-validated');
                return;
            }

            // Check terms acceptance
            if (termsCheckbox && !termsCheckbox.checked) {
                termsCheckbox.setCustomValidity('You must accept the terms and conditions');
                termsCheckbox.reportValidity();
                return;
            }
            
            // Show loading state
            if (placeOrderButton) {
                placeOrderButton.disabled = true;
                const submitText = placeOrderButton.querySelector('.submit-text');
                const spinner = placeOrderButton.querySelector('.spinner-border');
                if (submitText) submitText.textContent = 'Processing...';
                if (spinner) spinner.classList.remove('d-none');
            }

            try {
                const formData = new FormData(form);
                
                // Add payment method to form data
                const selectedMethod = document.querySelector('input[name="payment_method"]:checked');
                if (selectedMethod) {
                    formData.append('payment_method', selectedMethod.value);
                }

                const response = await fetch(form.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });

                const result = await response.json();
                
                if (result.redirect) {
                    window.location.href = result.redirect;
                } else if (result.success) {
                    if (result.message) {
                        showNotification(result.message, 'success');
                    }
                    if (result.redirect_url) {
                        setTimeout(() => {
                            window.location.href = result.redirect_url;
                        }, 1500);
                    }
                } else {
                    // Show error message
                    const errorContainer = document.getElementById('form-errors');
                    if (errorContainer) {
                        errorContainer.textContent = result.error || 'An error occurred. Please try again.';
                        errorContainer.classList.remove('d-none');
                        window.scrollTo({ top: 0, behavior: 'smooth' });
                    }
                }
            } catch (error) {
                console.error('Error:', error);
                const errorContainer = document.getElementById('form-errors');
                if (errorContainer) {
                    errorContainer.textContent = 'An error occurred. Please try again.';
                    errorContainer.classList.remove('d-none');
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                }
            } finally {
                // Reset button state
                if (placeOrderButton) {
                    placeOrderButton.disabled = false;
                    const submitText = placeOrderButton.querySelector('.submit-text');
                    const spinner = placeOrderButton.querySelector('.spinner-border');
                    if (submitText) submitText.textContent = 'Place Order';
                    if (spinner) spinner.classList.add('d-none');
                }
            }
        });
    }

    // Show notification function
    function showNotification(message, type = 'success') {
        // Remove any existing notifications
        const existingNotifications = document.querySelectorAll('.alert-notification');
        existingNotifications.forEach(el => el.remove());
        
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} position-fixed top-0 end-0 m-3 alert-notification`;
        notification.style.zIndex = '9999';
        notification.style.minWidth = '300px';
        notification.style.maxWidth = '90%';
        notification.style.wordBreak = 'break-word';
        notification.innerHTML = `
            <div class="d-flex align-items-center">
                <i class="bi ${type === 'success' ? 'bi-check-circle-fill' : 'bi-exclamation-triangle-fill'} me-2"></i>
                <span>${message}</span>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Add animation
        notification.style.opacity = '0';
        notification.style.transition = 'opacity 0.3s';
        setTimeout(() => notification.style.opacity = '1', 10);
        
        // Auto-remove after delay
        setTimeout(() => {
            notification.style.opacity = '0';
            setTimeout(() => notification.remove(), 300);
        }, 5000);
    }
    
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});
