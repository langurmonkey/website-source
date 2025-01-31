if(window.sessionStorage.getItem("dark-mode") == "true") {
  // Toggle dark-mode class if "dark-mode" property of localStorage is true
  darkModeAdd();
} else if (window.matchMedia && 
  window.matchMedia('(prefers-color-scheme: dark)').matches && 
  window.sessionStorage.getItem("dark-mode") == null) {
  // Otherwise, check browser setting "prefers-color-scheme" is set to "dark"
  darkModeAdd();
}

// Adds the dark mode to the site, at startup.
function darkModeAdd() {
  document.body.classList.add("dark-mode");
  window.onload = function () {
    updateThemeToggleButton(true);
  }
}

// Toggles dark and light modes.
function darkModeToggle() {
  // Add classes
  document.body.classList.toggle("dark-mode");
  is_dark = document.body.classList.contains("dark-mode");
  window.sessionStorage.setItem("dark-mode", is_dark);
  updateThemeToggleButton(is_dark);
}

// Updates the theme toggle button icon.
function updateThemeToggleButton(is_dark) {
  var toggle = document.getElementById("toggle-theme");
  toggle.classList.remove("fa-sun-o", "fa-moon");
  if(is_dark) {
    toggle.classList.add("fa-sun-o"); 
  } else {
    toggle.classList.add("fa-moon"); 
  }
}
