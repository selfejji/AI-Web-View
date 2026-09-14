/*
-- Owner: Sammy Elfejji
-- Camden County Schools Technology
--
-- #--- CCST Web View ---#
-- An AI centered microservice that empowers users to create 
-- reports, graphs/charts, and basic calculators as an interfaceable web application.
--
-- Date: 09/07/2026
*/


/*---------------------------------
*
* Loading screen logic -- (ARCHIVED)
*
---------------------------------*/


// Build text animation on DOM load
document.addEventListener("DOMContentLoaded", () => {
  const textContainer = document.getElementById('dancing-text-container');
  const textToAnimate = "Camden County Schools Technology";

  if (textContainer && textContainer.children.length === 0) {
    textContainer.classList.add('jiggling');
    textToAnimate.split('').forEach((char) => {
      const span = document.createElement('span');
      span.textContent = char === ' ' ? '\u00A0' : char; 
      span.classList.add('letter');
      textContainer.appendChild(span);
    });
  }
});

// Explicit call triggered only when main.js finishes view setup
window.hideLoadingScreen = function () {
  const loadingScreen = document.getElementById('loading-screen');
  const appContainer = document.getElementById('app-container');

  if (!loadingScreen || !appContainer) return;

  // 1. Reveal layout container BEHIND the opaque overlay
  appContainer.style.display = '';
  appContainer.classList.remove('hidden');

  // 2. Double requestAnimationFrame guarantees browser paints appContainer BEFORE fading loader
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      loadingScreen.classList.add('fade-out');

      setTimeout(() => {
        loadingScreen.remove();
        document.body.style.overflow = '';
      }, 500);
    });
  });
};