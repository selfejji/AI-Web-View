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

// Imports the functions from nav.js to initalize the nav logic and sidebar toggle
import { initNav, initSidebarToggle } from 'shared/nav.js';

const placeholderContent = document.querySelector('.placeholder-content');
const originalText = placeholderContent.textContent;



// Getter for the current app type based on the page navigation
function getAppType() {

  // Retrives the location search params for the current page
  const params = new URLSearchParams(window.location.search);

  // Gets the app param for that location
  const app = params.get('app');

  const validApps = ['reports', 'docs', 'calendar', 'manager'];

  // Checks if the app param is a current app in the nav, defaults to 'home' if not found or not provided
  return validApps.includes(app) ? app : 'home';
}

// Function to update the page name in the header (takes any type as param)
function updateHeaderTitle(pageName) {

  // Gets the element for the page title and header brand (CCST Web View) by id
  const brandContainer = document.getElementById('headerBrand');
  const pageTitleEl = document.getElementById('pageTitle');

  // Converts the page name to uppercase, defaults to 'home' if not provided
  // This is because the pageName param is calculated off the js file name
  const newTitle = (pageName || 'home').toUpperCase();

  // Checks if the elements exist, if not, return early
  if (!brandContainer || !pageTitleEl) return;

  // Checks if already showing the requested title and if the brand container is already animated
  if (pageTitleEl.textContent === newTitle && brandContainer.classList.contains('animated')) {
    return;
  } else {

    // Shrinks the brand container to prepare for the title change
    brandContainer.classList.remove('animated');

  }

  // Swap text after shrink finishes, then expand back out
  setTimeout(() => {
    pageTitleEl.textContent = newTitle;
    brandContainer.classList.add('animated');
  }, 200); // 200ms matches the CSS contraction speed
}

// Async function for dynamically loading the app view based on whether code is inejected
async function loadAppView(appType) {
  // Updates header title and initializes the nav with the current app type and navigation callback
  updateHeaderTitle(appType);
  initNav(appType, loadAppView);

  // Checks if the app container exists, if not, return early
  const appContainer = document.getElementById('app');
  if (!appContainer) return;

  // If the app type is 'home', show the placeholder content and return early
  if (appType === 'home') {
    placeholderContent.textContent = originalText;

    appContainer.innerHTML = `
      <div class="placeholder-content">
        <p>Waiting for AI content injection...💉</p>
      </div>`;
    return;
  }

  // Dynamically imports the app module based on the app type and calls its init function if it exists
  try {
    const module = await import(`apps/${appType}.js`);
    if (module.init) await module.init();
  } catch (error) {
    console.error(`Failed to load app: "${appType}"`, error);
  }
}


// Main initialization function that sets up the sidebar toggle, loads the initial app view, and handles browser navigation events
async function init() {
  // Initialize sidebar toggle listener (nav.js)
  initSidebarToggle();

  // Wait for initial view & dynamic modules to complete loading
  await loadAppView(getAppType());

  // Add a 'ready' class to the app wrapper to indicate that the app is fully loaded and ready for interaction
  const appWrapper = document.getElementById('app-container');
  if (appWrapper) {
    appWrapper.classList.add('ready');
  }

  // Listen for browser navigation events (back/forward) and reload the app view accordingly
  // Ensures the entire website is NOT reloaded and just the app view is
  window.addEventListener('popstate', () => {
    loadAppView(getAppType());
  });
}

  init();