document.addEventListener('DOMContentLoaded', function() {
    // Create particles
    const particlesContainer = document.getElementById('particles-js');
    if (!particlesContainer) return;
    
    const particleCount = 30;
    
    for (let i = 0; i < particleCount; i++) {
        createParticle(particlesContainer);
    }
    
    function createParticle(container) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        
        // Random size between 1-4px
        const size = Math.random() * 3 + 1;
        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        
        // Random position
        const posX = Math.random() * 100;
        const posY = Math.random() * 100;
        particle.style.left = `${posX}%`;
        particle.style.top = `${posY}%`;
        
        // Random opacity
        particle.style.opacity = Math.random() * 0.3 + 0.1;
        
        // Animation
        const duration = Math.random() * 30 + 15;
        const delay = Math.random() * 5;
        
        particle.style.animation = `floatingParticle ${duration}s ${delay}s infinite linear`;
        
        // Add keyframe animation dynamically
        if (!document.querySelector('#particle-keyframes')) {
            const style = document.createElement('style');
            style.id = 'particle-keyframes';
            style.innerHTML = `
                @keyframes floatingParticle {
                    0% {
                        transform: translate(0, 0);
                    }
                    25% {
                        transform: translate(${Math.random() * 80 - 40}px, ${Math.random() * 80 - 40}px);
                    }
                    50% {
                        transform: translate(${Math.random() * 80 - 40}px, ${Math.random() * 80 - 40}px);
                    }
                    75% {
                        transform: translate(${Math.random() * 80 - 40}px, ${Math.random() * 80 - 40}px);
                    }
                    100% {
                        transform: translate(0, 0);
                    }
                }
            `;
            document.head.appendChild(style);
        }
        
        container.appendChild(particle);
    }
    
    // Add subtle parallax effect to hero section
    const heroSection = document.querySelector('.hero-section');
    if (heroSection) {
        document.addEventListener('mousemove', function(e) {
            const mouseX = e.clientX / window.innerWidth;
            const mouseY = e.clientY / window.innerHeight;
            
            const blobs = document.querySelectorAll('.hero-blob');
            blobs.forEach((blob, index) => {
                const depth = index + 1;
                const moveX = (mouseX - 0.5) * 15 * depth;
                const moveY = (mouseY - 0.5) * 15 * depth;
                blob.style.transform = `translate(${moveX}px, ${moveY}px)`;
            });
            
            const heroImage = document.querySelector('.hero-image');
            if (heroImage) {
                const moveX = (mouseX - 0.5) * -15;
                const moveY = (mouseY - 0.5) * -15;
                heroImage.style.transform = `translateY(0) rotate(-2deg) translate(${moveX}px, ${moveY}px)`;
            }
        });
    }
    
    // Add reveal animations
    const revealElements = document.querySelectorAll('[data-aos]');
    revealElements.forEach(element => {
        const observer = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    element.classList.add('aos-animate');
                    observer.unobserve(element);
                }
            });
        }, { threshold: 0.1 });
        
        observer.observe(element);
    });
    
    // Add realistic shadow effect to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mousemove', function(e) {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const angleX = (y - centerY) / 15;
            const angleY = (centerX - x) / 15;
            
            card.style.transform = `perspective(1000px) rotateX(${angleX}deg) rotateY(${angleY}deg) translateZ(10px)`;
            card.style.boxShadow = `
                ${angleY * 0.5}px ${angleX * 0.5}px 15px rgba(0,0,0,0.1),
                ${angleY * 0.2}px ${angleX * 0.2}px 5px rgba(0,0,0,0.05)
            `;
        });
        
        card.addEventListener('mouseleave', function() {
            card.style.transform = '';
            card.style.boxShadow = '';
        });
    });
});