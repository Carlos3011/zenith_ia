document.addEventListener('DOMContentLoaded', function() {
    AOS.init({
        duration: 800,
        once: true
    });

    const form = document.getElementById('contactForm');
    const submitBtn = form.querySelector('button[type="submit"]');
    const spinner = submitBtn.querySelector('.loading-spinner');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        try {
            submitBtn.disabled = true;
            spinner.classList.remove('hidden');
            
            const formData = new FormData(form);
            const response = await fetch('/contact/submit', {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': '{{ csrf_token }}'
                },
                body: formData
            });
            
            const data = await response.json();
            
            if(data.success) {
                showNotification('¡Mensaje enviado con éxito!', 'green');
                form.reset();
            } else {
                showNotification('Por favor completa todos los campos correctamente', 'yellow');
            }
        } catch (error) {
            showNotification('Error al enviar el mensaje. Intenta nuevamente.', 'red');
        } finally {
            submitBtn.disabled = false;
            spinner.classList.add('hidden');
        }
    });

    function showNotification(message, color) {
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 px-6 py-3 rounded-lg shadow-lg text-white flex items-center space-x-3 ${color === 'green' ? 'bg-green-500' : color === 'red' ? 'bg-red-500' : 'bg-yellow-500'} animate-slide-in`;
        notification.innerHTML = `
            <i class="fas ${color === 'green' ? 'fa-check-circle' : color === 'red' ? 'fa-times-circle' : 'fa-exclamation-triangle'}"></i>
            <span>${message}</span>
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.classList.add('animate-slide-out');
            setTimeout(() => notification.remove(), 500);
        }, 3000);
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, {
        threshold: 0.1
    });

    document.querySelectorAll('.cards-grid').forEach(grid => {
        observer.observe(grid);
    });

    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
});


// Animación de contadores
document.addEventListener('DOMContentLoaded', function() {
    const counters = document.querySelectorAll('.counter');
    counters.forEach(counter => {
        const target = parseInt(counter.innerText);
        let count = 0;
        const speed = 2000 / target;
        
        function updateCount() {
            if(count < target) {
                count++;
                counter.innerText = count + (counter.innerText.includes('+') ? '+' : '%');
                setTimeout(updateCount, speed);
            }
        }
        
        updateCount();
    });
});
