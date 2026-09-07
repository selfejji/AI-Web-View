// This event listener waits for the webpage to be fully read by the browser
document.addEventListener("DOMContentLoaded", () => {
    const loadingScreen = document.getElementById('loading-screen');
    const appContent = document.getElementById('app-content');
    const textContainer = document.getElementById('dancing-text-container');
    const textToAnimate = "Camden County Schools Technology";

    if (textContainer) {
        textContainer.classList.add('jiggling');

        // Generate letters and apply stagger delay
        textToAnimate.split('').forEach((char, index) => {
            const span = document.createElement('span');
            span.textContent = char === ' ' ? '\u00A0' : char; 
            span.classList.add('letter');
            
            // Stagger the jiggle slightly for each letter so it ripples
            //span.style.animationDelay = `-${index * 0.1}s`;

            textContainer.appendChild(span);
        });
    }
    // setTimeout is the magic here. It acts as an automatic countdown timer.
    // The "2500" at the bottom tells it to wait exactly 2.5 seconds.
    setTimeout(() => {
        
        // 1. Start fading out the loading screen
        loadingScreen.classList.add('fade-out');

        // 2. Wait 0.5 seconds for the fade animation to finish
        setTimeout(() => {
            // 3. Remove the loading screen completely
            loadingScreen.style.display = 'none';
            
            // 4. Reveal the main page
            appContent.classList.remove('hidden');
        }, 500); 

    }, 2000); // <-- Change this number to make the loading screen longer or shorter (1000 = 1 second)
});
