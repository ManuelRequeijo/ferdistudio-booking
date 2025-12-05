document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('contactForm');
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        console.log('Formulario enviado');
        
        // Obtener datos del formulario
        const formData = new FormData(form);
        const nombre = formData.get('nombre');
        const apellido = formData.get('apellido');
        const email = formData.get('email');
        const telefono = formData.get('telefono');
        
        // Obtener datos de la URL
        const path = window.location.pathname.split('/');
        const serviceId = path[2];
        const date = path[3];
        const time = path[4];
        
        console.log('Datos:', { serviceId, date, time, nombre, email });
        
        // Preparar datos para enviar
        const bookingData = {
            service_id: serviceId,
            date: date,
            time: time,
            customer: {
                nombre: nombre,
                apellido: apellido,
                email: email,
                telefono: '+54' + telefono.replace(/\s/g, ''),
                observaciones: formData.get('observaciones') || ''
            }
        };
        
        console.log('Enviando:', bookingData);
        
        try {
            const response = await fetch('/api/create-booking', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(bookingData)
            });
            
            const result = await response.json();
            console.log('Respuesta:', result);
            
            if (result.success) {
                window.location.href = `/confirmation/${result.booking_id}`;
            } else {
                alert('Error: ' + result.error);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error al procesar la reserva');
        }
    });
});