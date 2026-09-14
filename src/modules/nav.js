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

import { getAgents } from '../../main.js';

// Getter for the current app type based on the page navigation
export function getAppType(validApps) {

  // Retrives the location search params for the current page
  const params = new URLSearchParams(window.location.search);

  // Gets the app param for that location
  const app = params.get('app');

  // Checks if the app param is a current app in the nav, defaults to 'home' if not found or not provided
  return validApps.includes(app) ? app : 'home';
}

// Function to update the page name in the header (takes any type as param)
export async function updateHeader(agentName) {

  // Gets the element for the page title and header brand (CCST Web View) by id
  const appContainer = document.getElementById('appHeader');
  const agentTitle = document.getElementById('agentTitle');
  const titleCenter = document.getElementById('titleCenter');
  const sidebar_link = document.getElementById('sidebar-link');


  try {
    // Checks if the elements exist, if not, return early
    if (!agentTitle) throw error;
    
  } catch (error) {
    console.error("Failed to load agent title element: ", error);
  }

  // Checks if already showing the requested title and if the brand container is already animated
  if (agentTitle.textContent === newTitle && appContainer.classList.contains('animated')) {
    return;
  } else {

    // Shrinks the brand container to prepare for the title change
    appContainerContainer.classList.remove('animated');

  }

  // Swap text after shrink finishes, then expand back out
  setTimeout(() => {
    agentTitle.textContent = newTitle;
    appContainer.classList.add('animated');
  }, 200); 

  try {
    // Checks if the elements exist, if not, return early
    if (!titleCenter) throw error;
    
  } catch (error) {
    console.error("Failed to load title element: ", error);
  }

}

// Async function for dynamically loading the app view based on whether code is inejected
export async function loadAppView(appType) {
  
  updateHeaderTitle(appType);


  const appContainer = document.getElementById('app');
  if (!appContainer) return;

  try {
    const module = await import("modules/app-state.js");
    //await module.${appType}init();

  } catch (error) {
    console.error(`Failed to load app: "${appType}"`, error);
  }

  const navContainer = document.getElementById('sidebar');

  try {
    // Checks if nav container is empty
    if (!navContainer) throw error;
  } catch (error) {
    console.error("Failed to load sidebar: ", error);
  }


   // Collects element metadata upon click
  sidebar-link.addEventListener('click', (e) => {

    // CRUCIAL: supresses the browsers native navigation behavior 
    // Allows for the DOM to handle navigation events
    e.preventDefault();

    // Gets the elements meta data dor the app id and link passed from history.pushState()
    const href = link.getAttribute('href');
    const appId = link.getAttribute('data-app');
      
    // Performs the navigation on DOM side
    if (window.location.search !== href && !(href === '?' && window.location.search === '')) {
      history.pushState(null, '', href);
      if (typeof onNavigate === 'function') {
        onNavigate(appId);
      }
    }
  });
}

// Exported function for intializing the toggle on the side bar
export async function initSidebarToggle() {
  const toggleBtn = document.getElementById('sidebarToggle');
  const sidebar = document.getElementById('sidebar');

  if (!toggleBtn || !sidebar){ return; } 
  else {
    toggleBtn.addEventListener('click', () => {
    sidebar.classList.toggle('collapsed');
    });
  }
}

export async function initNav(activeApp = 'home', onNavigate) {
  /* UNCOMMENT WHEN READY AND DELETE iniSiteToggle function
  const toggleBtn = document.getElementById('sidebarToggle');
  const sidebar = document.getElementById('sidebar');

    if (!toggleBtn || !sidebar){ return; } 
    else {
      toggleBtn.addEventListener('click', () => {
      sidebar.classList.toggle('collapsed');
      });
    }
  */

  // Checks if nav container is empty
  const navContainer = document.getElementById('sidebar');
  if (!navContainer) return;

  const agents = await getAgents();

  const navItems = agents.map(agent => ({
    model: agent.model,
    id: agent["chat-id"] 
  }));

  // Inner html definition for nav container
  navContainer.innerHTML = `
    <nav class="sidebar-nav">
      ${navItems
        .map(item =>
          `<a 
            href=""?app=" + ${item.id} + "/" + ${item.model}" 
            data-app="${item.id}"
            class="sidebar-link ${item.id === activeApp ? 'active' : ''}"
          >
            <span class="link-label">${item.model}</span>
          </a>`
        ).join('')}
    </nav>`;

  // Intercept click events to prevent full page reloads
  navContainer.querySelectorAll('.sidebar-link').forEach(link => {

    // Collects element metadata upon click
    link.addEventListener('click', (e) => {

      // CRUCIAL: supresses the browsers native navigation behavior 
      // Allows for the DOM to handle navigation events
      e.preventDefault();

      // Gets the elements meta data dor the app id and link passed from history.pushState()
      const href = link.getAttribute('href');
      const appId = link.getAttribute('data-app');
      
      // Performs the navigation on DOM side
      if (window.location.search !== href && !(href === '?' && window.location.search === '')) {
        history.pushState(null, '', href);
        if (typeof onNavigate === 'function') {
          onNavigate(appId);
        }
      }
    });
  });
}