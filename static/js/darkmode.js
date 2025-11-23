// Theme Toggle Functionality
class ThemeToggle {
  constructor() {
    this.themeToggleBtns = Array.from(document.querySelectorAll('.theme-toggle'));
    this.themeIcons = Array.from(document.querySelectorAll('.theme-toggle i'));
    this.theme = localStorage.getItem('theme') || this.getSystemPreference();
    
    // Add loading class to prevent FOUC
    document.documentElement.classList.add('theme-loading');
    
    // Initialize after a small delay to ensure DOM is ready
    setTimeout(() => this.init(), 10);
  }
  
  init() {
    // Set initial theme
    this.setTheme(this.theme);
    
    // Add event listeners for all theme toggle buttons
    this.themeToggleBtns.forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        this.toggleTheme();
      });
      
      // Add keyboard support
      btn.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          this.toggleTheme();
        }
      });
    });
    
    // Remove loading class after a short delay to ensure smooth transition
    setTimeout(() => {
      document.documentElement.classList.remove('theme-loading');
      document.documentElement.classList.add('theme-loaded');
    }, 100);
  }
  
  getSystemPreference() {
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  
  setTheme(theme) {
    // Update data-theme attribute
    document.documentElement.setAttribute('data-theme', theme);
    
    // Update localStorage
    localStorage.setItem('theme', theme);
    
    // Update all icons and ARIA labels
    this.updateIcons(theme);
    
    // Dispatch a custom event for other scripts to listen to
    document.dispatchEvent(new CustomEvent('themeChange', { detail: { theme } }));
  }
  
  toggleTheme() {
    const newTheme = this.theme === 'dark' ? 'light' : 'dark';
    this.theme = newTheme;
    
    // Add animation class
    this.themeToggleBtns.forEach(btn => {
      btn.classList.add('animate');
      // Remove animation class after animation completes
      setTimeout(() => btn.classList.remove('animate'), 500);
    });
    
    this.setTheme(newTheme);
  }
  
  updateIcons(theme) {
    this.themeIcons.forEach(icon => {
      // Add transition class for smooth icon change
      icon.style.transition = 'opacity 0.3s ease';
      icon.style.opacity = '0';
      
      setTimeout(() => {
        if (theme === 'dark') {
          icon.classList.remove('fa-moon');
          icon.classList.add('fa-sun');
        } else {
          icon.classList.remove('fa-sun');
          icon.classList.add('fa-moon');
        }
        
        // Fade in the new icon
        setTimeout(() => {
          icon.style.opacity = '1';
        }, 10);
      }, 150);
    });
    
    this.themeToggleBtns.forEach(btn => {
      if (theme === 'dark') {
        btn.setAttribute('aria-label', 'Switch to light mode');
        btn.setAttribute('title', 'Switch to light mode');
        btn.setAttribute('aria-pressed', 'true');
      } else {
        btn.setAttribute('aria-label', 'Switch to dark mode');
        btn.setAttribute('title', 'Switch to dark mode');
        btn.setAttribute('aria-pressed', 'false');
      }
    });
  }
}

// Initialize theme toggle when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  // Add a class to the html element to prevent FOUC
  document.documentElement.classList.add('theme-loading');
  
  // Initialize theme toggle
  const themeToggle = new ThemeToggle();
  
  // Make theme toggle available globally for debugging
  window.themeToggle = themeToggle;
  
  // Remove loading class after a short delay to ensure smooth transition
  setTimeout(() => {
    document.documentElement.classList.remove('theme-loading');
  }, 100);
});

// Watch for system theme changes
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
  // Only apply system preference if user hasn't explicitly chosen a theme
  if (!localStorage.getItem('theme')) {
    const newTheme = e.matches ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', newTheme);
  }
});
