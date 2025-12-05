class BookingCalendar {
    constructor() {
        this.currentDate = new Date();
        this.selectedDate = null;
        this.selectedTime = null;
        this.availableSlots = [];
        
        this.init();
    }
    
    init() {
        this.renderCalendar();
        this.bindEvents();
    }
    
    bindEvents() {
        document.getElementById('prevMonth').addEventListener('click', () => {
            this.currentDate.setMonth(this.currentDate.getMonth() - 1);
            this.renderCalendar();
        });
        
        document.getElementById('nextMonth').addEventListener('click', () => {
            this.currentDate.setMonth(this.currentDate.getMonth() + 1);
            this.renderCalendar();
        });
        
        document.getElementById('continueBtn').addEventListener('click', () => {
            if (this.selectedDate && this.selectedTime) {
                const dateStr = this.selectedDate.toISOString().split('T')[0];
                window.location.href = `/contact/${serviceId}/${dateStr}/${this.selectedTime}`;
            }
        });
        
        // Auto-refresh cada 30 segundos si hay una fecha seleccionada
        setInterval(() => {
            if (this.selectedDate) {
                console.log('Auto-actualizando horarios...');
                this.loadAvailableSlots(this.selectedDate, false); // Sin indicador visual
            }
        }, 30000);
    }
    
    renderCalendar() {
        const monthNames = [
            'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
            'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
        ];
        
        const dayNames = ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb'];
        
        document.getElementById('currentMonth').textContent = 
            `${monthNames[this.currentDate.getMonth()]} ${this.currentDate.getFullYear()}`;
        
        const firstDay = new Date(this.currentDate.getFullYear(), this.currentDate.getMonth(), 1);
        const lastDay = new Date(this.currentDate.getFullYear(), this.currentDate.getMonth() + 1, 0);
        
        const calendarGrid = document.getElementById('calendarGrid');
        calendarGrid.innerHTML = '';
        calendarGrid.style.gridTemplateColumns = 'repeat(7, 1fr)';
        calendarGrid.style.gap = '0.5rem';
        
        // Headers
        dayNames.forEach(day => {
            const header = document.createElement('div');
            header.className = 'calendar-header-day';
            header.textContent = day;
            header.style.cssText = `
                padding: 0.5rem;
                text-align: center;
                font-weight: bold;
                color: var(--text-light);
                background: var(--light-bg);
                border-radius: 5px;
            `;
            calendarGrid.appendChild(header);
        });
        
        // Days - solo del mes actual
        const today = new Date();
        const daysInMonth = lastDay.getDate();
        
        // Espacios vacíos al inicio
        for (let i = 0; i < firstDay.getDay(); i++) {
            const emptyDay = document.createElement('div');
            emptyDay.className = 'calendar-day empty';
            emptyDay.style.visibility = 'hidden';
            calendarGrid.appendChild(emptyDay);
        }
        
        // Días del mes actual
        for (let day = 1; day <= daysInMonth; day++) {
            const date = new Date(this.currentDate.getFullYear(), this.currentDate.getMonth(), day);
            
            const dayElement = document.createElement('div');
            dayElement.className = 'calendar-day';
            dayElement.textContent = day;
            
            const isPast = date < today.setHours(0, 0, 0, 0);
            const isSunday = date.getDay() === 0;
            
            if (isPast || isSunday) {
                dayElement.classList.add('disabled');
            } else {
                dayElement.addEventListener('click', () => this.selectDate(date));
            }
            
            calendarGrid.appendChild(dayElement);
        }
    }
    
    async selectDate(date) {
        // Remove previous selection
        document.querySelectorAll('.calendar-day.selected').forEach(day => {
            day.classList.remove('selected');
        });
        
        // Add selection to clicked day
        event.target.classList.add('selected');
        
        this.selectedDate = date;
        this.selectedTime = null;
        
        // Update booking info
        const options = { 
            weekday: 'long', 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
        };
        document.getElementById('selectedDate').textContent = 
            date.toLocaleDateString('es-ES', options);
        
        // Show time slots section
        document.getElementById('timeSlotsSection').style.display = 'block';
        document.getElementById('bookingInfo').style.display = 'block';
        
        // Load available slots with retry
        await this.loadAvailableSlotsWithRetry(date);
        
        // Scroll to time slots
        document.getElementById('timeSlotsSection').scrollIntoView({ 
            behavior: 'smooth' 
        });
    }
    
    async loadAvailableSlotsWithRetry(date, maxRetries = 2) {
        for (let attempt = 1; attempt <= maxRetries; attempt++) {
            console.log(`Intento ${attempt} de ${maxRetries} para cargar horarios`);
            
            const success = await this.loadAvailableSlots(date, true);
            
            if (success) {
                return;
            }
            
            // Si no es el último intento, esperar 2 segundos
            if (attempt < maxRetries) {
                console.log('Reintentando en 2 segundos...');
                await new Promise(resolve => setTimeout(resolve, 2000));
            }
        }
        
        // Si todos los intentos fallaron
        console.log('Todos los intentos fallaron, mostrando mensaje de error');
        this.showErrorMessage();
    }
    
    async loadAvailableSlots(date, showIndicator = true) {
        // Mostrar indicador de carga
        const loadingIndicator = document.getElementById('loadingIndicator');
        if (showIndicator && loadingIndicator) {
            loadingIndicator.style.display = 'inline-block';
        }
        
        try {
            const dateStr = date.toISOString().split('T')[0];
            const timestamp = new Date().getTime();
            const response = await fetch(`/api/available-slots?date=${dateStr}&service_id=${serviceId}&_t=${timestamp}`, {
                method: 'GET',
                headers: {
                    'Cache-Control': 'no-cache',
                    'Pragma': 'no-cache'
                }
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            
            const data = await response.json();
            
            console.log('Horarios actualizados:', data.slots);
            console.log('Timestamp:', data.timestamp);
            
            this.availableSlots = data.slots || [];
            this.renderTimeSlots();
            
            return true; // Éxito
            
        } catch (error) {
            console.error('Error loading slots:', error);
            return false; // Error
        } finally {
            // Ocultar indicador de carga
            if (showIndicator && loadingIndicator) {
                loadingIndicator.style.display = 'none';
            }
        }
    }
    
    showErrorMessage() {
        this.availableSlots = [];
        this.renderTimeSlots();
        
        const timeSlotsSection = document.getElementById('timeSlotsSection');
        if (timeSlotsSection) {
            const errorMsg = document.createElement('div');
            errorMsg.className = 'alert alert-warning mt-2';
            errorMsg.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Error cargando horarios. Recarga la página si persiste el problema.';
            timeSlotsSection.appendChild(errorMsg);
            
            setTimeout(() => errorMsg.remove(), 5000);
        }
    }
    
    renderTimeSlots() {
        const morningSlots = document.getElementById('morningSlots');
        const afternoonSlots = document.getElementById('afternoonSlots');
        const eveningSlots = document.getElementById('eveningSlots');
        
        morningSlots.innerHTML = '';
        afternoonSlots.innerHTML = '';
        eveningSlots.innerHTML = '';
        
        this.availableSlots.forEach(slot => {
            const timeSlot = document.createElement('button');
            timeSlot.className = 'time-slot';
            timeSlot.textContent = slot;
            timeSlot.addEventListener('click', () => this.selectTime(slot, timeSlot));
            
            const hour = parseInt(slot.split(':')[0]);
            
            if (hour < 12) {
                morningSlots.appendChild(timeSlot);
            } else if (hour < 18) {
                afternoonSlots.appendChild(timeSlot);
            } else {
                eveningSlots.appendChild(timeSlot);
            }
        });
        
        // Hide empty periods
        document.querySelector('.time-period:nth-child(1)').style.display = 
            morningSlots.children.length > 0 ? 'block' : 'none';
        document.querySelector('.time-period:nth-child(2)').style.display = 
            afternoonSlots.children.length > 0 ? 'block' : 'none';
        document.querySelector('.time-period:nth-child(3)').style.display = 
            eveningSlots.children.length > 0 ? 'block' : 'none';
    }
    
    selectTime(time, element) {
        // Remove previous selection
        document.querySelectorAll('.time-slot.selected').forEach(slot => {
            slot.classList.remove('selected');
        });
        
        // Add selection
        element.classList.add('selected');
        
        this.selectedTime = time;
        
        // Update booking info
        document.getElementById('selectedTime').textContent = 
            `${time} (${serviceDuration} min)`;
        
        // Enable continue button
        document.getElementById('continueBtn').disabled = false;
    }
}

// Initialize calendar when page loads
document.addEventListener('DOMContentLoaded', () => {
    new BookingCalendar();
});