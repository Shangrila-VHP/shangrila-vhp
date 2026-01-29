// Basic website interactions
document.addEventListener('DOMContentLoaded', () => {
    console.log('Shangrila-VHP Website Loaded');

    // Smooth scroll for navigation links handled by CSS
    
    // Intersection Observer for scroll animations
    const observerOptions = {
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);

    // Target sections or cards for scroll reveal if needed
    // Currently using CSS animations for hero
});
