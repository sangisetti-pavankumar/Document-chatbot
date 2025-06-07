document.addEventListener('DOMContentLoaded', function() {
    // Create starfield background
    const starfieldContainer = document.getElementById('starfield');
    if (!starfieldContainer) return;
    
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    
    // Set canvas to full width/height
    canvas.width = starfieldContainer.offsetWidth;
    canvas.height = starfieldContainer.offsetHeight;
    starfieldContainer.appendChild(canvas);
    
    // Star properties
    const stars = [];
    const starCount = 100;
    const starSizeMin = 0.5;
    const starSizeMax = 2;
    const starSpeed = 0.2;
    
    // Create stars
    for (let i = 0; i < starCount; i++) {
        stars.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            size: Math.random() * (starSizeMax - starSizeMin) + starSizeMin,
            speed: Math.random() * starSpeed + 0.1
        });
    }
    
    // Animation function
    function animate() {
        // Clear canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Draw stars
        stars.forEach(star => {
            // Update position
            star.y += star.speed;
            
            // Reset if star goes off screen
            if (star.y > canvas.height) {
                star.y = 0;
                star.x = Math.random() * canvas.width;
            }
            
            // Draw star
            ctx.beginPath();
            ctx.arc(star.x, star.y, star.size, 0, Math.PI * 2);
            ctx.fillStyle = 'rgba(255, 255, 255, 0.7)';
            ctx.fill();
        });
        
        // Continue animation
        requestAnimationFrame(animate);
    }
    
    // Handle window resize
    window.addEventListener('resize', function() {
        canvas.width = starfieldContainer.offsetWidth;
        canvas.height = starfieldContainer.offsetHeight;
    });
    
    // Start animation
    animate();
});