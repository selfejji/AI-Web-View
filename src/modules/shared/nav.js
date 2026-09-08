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

// Exported function for intializing the toggle on the side bar
export function initSidebarToggle() {
  const toggleBtn = document.getElementById('sidebarToggle');
  const sidebar = document.getElementById('sidebar');

  if (!toggleBtn || !sidebar){ return; } 
  else {
    toggleBtn.addEventListener('click', () => {
    sidebar.classList.toggle('collapsed');
    });
  }
}

// Intializes the the navigation menu logic
export function initNav(activeApp = 'home', onNavigate) {

  // Checks if nav container is empty
  const navContainer = document.getElementById('sidebar');
  if (!navContainer) return;

  // Creates an array of the ellements in the side bar
  // The document location interface (windows.location) has standard syntax for the path being ?dir=file
  const navItems = [
    { id: 'home', label: 'Home', path: '?' },
    { id: 'reports', label: 'Reports', path: '?app=reports' },
    { id: 'docs', label: 'Docs', path: '?app=docs' },
    { id: 'calendar', label: 'Calendar', path: '?app=calendar' },
    { id: 'manager', label: 'Manager', path: '?app=manager' }
  ];

  // Inner html definition for nav container
  navContainer.innerHTML = `
    <nav class="sidebar-nav">
      ${navItems
        .map(item =>
          `<a 
            href="${item.path}" 
            data-app="${item.id}"
            class="sidebar-link ${item.id === activeApp ? 'active' : ''}"
          >
            <span class="link-label">${item.label}</span>
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