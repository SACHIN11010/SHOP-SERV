// Debug logging
console.log('Dark mode script loaded');

// Dark mode functionality
function initDarkMode() {
  const themeToggle = document.getElementById('theme-toggle');
  const html = document.documentElement;
  const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');
  
  // Debug: Log initial state
  console.log('Theme toggle element:', themeToggle);
  console.log('Current theme from localStorage:', localStorage.getItem('theme'));
  console.log('Prefers dark mode:', prefersDarkScheme.matches);
  
  // Function to set the theme
  function setTheme(theme) {
    console.log('Setting theme to:', theme);
    
    // Add transition class for smooth theme switching
    html.classList.add('theme-transition');
    
    // Set the theme attribute and update the UI
    document.documentElement.setAttribute('data-theme', theme);
    
    // Update the toggle button icon
    if (themeToggle) {
      if (theme === 'dark') {
        themeToggle.innerHTML = '<i class="bi bi-sun" title="Switch to light mode"></i>';
        themeToggle.setAttribute('aria-label', 'Switch to light mode');
      } else {
        themeToggle.innerHTML = '<i class="bi bi-moon" title="Switch to dark mode"></i>';
        themeToggle.setAttribute('aria-label', 'Switch to dark mode');
      }
      
      // Add a small animation to the icon
      themeToggle.classList.add('animate');
      setTimeout(() => themeToggle.classList.remove('animate'), 300);
    }
    
    // Save the theme preference
    localStorage.setItem('theme', theme);
    
    // Remove the transition class after the animation completes
    setTimeout(() => {
      html.classList.remove('theme-transition');
    }, 300);
  }
  
  // Listen for system theme changes (only if no explicit preference is set)
  prefersDarkScheme.addEventListener('change', (e) => {
    if (!localStorage.getItem('theme')) {
      setTheme(e.matches ? 'dark' : 'light');
    }
  });
  
  // Set the initial theme based on user preference or system preference
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme === 'dark' || (!savedTheme && prefersDarkScheme.matches)) {
    setTheme('dark');
  } else {
    setTheme('light');
  }
  
  // Toggle theme when the button is clicked
  if (themeToggle) {
    console.log('Adding click event listener to theme toggle');
    themeToggle.addEventListener('click', function() {
      const currentTheme = document.documentElement.getAttribute('data-theme');
      console.log('Theme toggle clicked. Current theme:', currentTheme);
      setTheme(currentTheme === 'dark' ? 'light' : 'dark');
    });
    
    // Add a class to the body when JavaScript is enabled (for no-js fallbacks)
    document.body.classList.add('js-enabled');
  } else {
    console.error('Theme toggle button not found!');
  }
}

// Initialize when the DOM is fully loaded
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initDarkMode);
} else {
  initDarkMode();
}

// Add a small script to prevent flash of unstyled content (FOUC)
// This should be as early in the <head> as possible
(function() {
  // Check for saved theme preference before the page loads
  const savedTheme = localStorage.getItem('theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  
  // Apply the theme immediately to prevent FOUC
  if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
    document.documentElement.setAttribute('data-theme', 'dark');
  } else {
    document.documentElement.setAttribute('data-theme', 'light');
  }
  
  // Add a class to indicate the theme is loaded
  document.documentElement.classList.add('theme-loaded');
})();
