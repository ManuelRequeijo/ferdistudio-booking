class ContactForm {
    constructor() {
        this.form = document.getElementById('contactForm');
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.formatDate();
    }
    
    bindEvents() {
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
        
        // Phone number formatting
        const phoneInput = document.getElementById('telefono');
        phoneInput.addEventListener('input', (e) => this.formatPhone(e));
        
        // Real-time validation
        const requiredFields = this.form.querySelectorAll('[required]');
        requiredFields.forEach(field => {
            field.addEventListener('blur', () => this.validateField(field));
            field.addEventListener('input', () => this.clearFieldError(field));
        });
    }
    
    formatDate() {
        const dateElement = document.getElementById('bookingDate');
        if (typeof bookingData !== 'undefined') {
            const date = new Date(bookingData.date);
            const options = { 
                weekday: 'long', 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric' 
            };
            dateElement.textContent = date.toLocaleDateString('es-ES', options);
        }
    }
    
    formatPhone(e) {
        let value = e.target.value.replace(/\D/g, '');
        
        // Format as: 11 2345 6789
        if (value.length >= 2) {
            value = value.substring(0, 2) + ' ' + value.substring(2);
        }
        if (value.length >= 7) {
            value = value.substring(0, 7) + ' ' + value.substring(7, 11);
        }
        
        e.target.value = value;
    }
    
    validateField(field) {
        const value = field.value.trim();
        let isValid = true;
        let errorMessage = '';
        
        // Required validation
        if (field.hasAttribute('required') && !value) {
            isValid = false;
            errorMessage = 'Este campo es obligatorio';
        }
        
        // Email validation
        if (field.type === 'email' && value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                isValid = false;
                errorMessage = 'Ingresa un email válido';
            }
        }
        
        // Phone validation
        if (field.id === 'telefono' && value) {
            const phoneRegex = /^\d{2}\s\d{4}\s\d{4}$/;
            if (!phoneRegex.test(value)) {
                isValid = false;
                errorMessage = 'Formato: 11 2345 6789';
            }
        }
        
        this.showFieldError(field, isValid, errorMessage);
        return isValid;
    }
    
    showFieldError(field, isValid, message) {
        // Remove existing error
        const existingError = field.parentNode.querySelector('.field-error');
        if (existingError) {
            existingError.remove();
        }
        
        if (!isValid) {
            field.classList.add('is-invalid');
            
            const errorDiv = document.createElement('div');
            errorDiv.className = 'field-error text-danger small mt-1';
            errorDiv.textContent = message;
            field.parentNode.appendChild(errorDiv);
        } else {
            field.classList.remove('is-invalid');
            field.classList.add('is-valid');
        }
    }
    
    clearFieldError(field) {
        field.classList.remove('is-invalid');
        const errorDiv = field.parentNode.querySelector('.field-error');
        if (errorDiv) {
            errorDiv.remove();
        }
    }
    
    validateForm() {
        const requiredFields = this.form.querySelectorAll('[required]');
        let isFormValid = true;
        
        requiredFields.forEach(field => {
            if (!this.validateField(field)) {
                isFormValid = false;
            }
        });
        
        return isFormValid;
    }
    
    async handleSubmit(e) {
        e.preventDefault();
        
        if (!this.validateForm()) {
            this.showAlert('Por favor corrige los errores en el formulario', 'danger');
            return;
        }
        
        const submitBtn = this.form.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        
        try {
            // Show loading state
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Procesando...';
            
            // Prepare form data
            const formData = new FormData(this.form);
            const customerData = {
                nombre: formData.get('nombre'),
                apellido: formData.get('apellido'),
                email: formData.get('email'),
                telefono: document.getElementById('countryCode').value + formData.get('telefono').replace(/\s/g, ''),
                observaciones: formData.get('observaciones') || ''
            };
            
            // Obtener datos de la URL
            const pathParts = window.location.pathname.split('/');
            const serviceId = pathParts[2];
            const date = pathParts[3];
            const time = pathParts[4];
            
            const bookingRequest = {
                service_id: serviceId,
                date: date,
                time: time,
                customer: customerData
            };
            
            console.log('Enviando reserva:', bookingRequest);
            
            // Submit booking
            const response = await fetch('/api/create-booking', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(bookingRequest)
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Redirect to confirmation
                window.location.href = `/confirmation/${result.booking_id}`;
            } else {
                throw new Error(result.error || 'Error al crear la reserva');
            }
            
        } catch (error) {
            console.error('Error:', error);
            this.showAlert('Error al procesar la reserva. Inténtalo nuevamente.', 'danger');
        } finally {
            // Restore button
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
        }
    }
    
    showAlert(message, type = 'info') {
        // Remove existing alerts
        const existingAlert = document.querySelector('.booking-alert');
        if (existingAlert) {
            existingAlert.remove();
        }
        
        const alert = document.createElement('div');
        alert.className = `alert alert-${type} booking-alert fade-in`;
        alert.innerHTML = `
            <i class="fas fa-${type === 'danger' ? 'exclamation-triangle' : 'info-circle'}"></i>
            ${message}
            <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
        `;
        
        this.form.insertBefore(alert, this.form.firstChild);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (alert.parentNode) {
                alert.remove();
            }
        }, 5000);
    }
}

// Initialize form when page loads
document.addEventListener('DOMContentLoaded', () => {
    new ContactForm();
});