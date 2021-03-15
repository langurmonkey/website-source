// IMPORTANT: This script is delivered inline in footer.html
if(sessionStorage.getItem("dark-mode") == "true") {
    // Toggle dark-mode class if "dark-mode" property of sessionStorage is true
    darkModeAdd();
} else if (window.matchMedia && 
    window.matchMedia('(prefers-color-scheme: dark)').matches && 
    sessionStorage.getItem("dark-mode") == null) {
    // Otherwise, check browser setting "prefers-color-scheme" is set to "dark"
    darkModeAdd();
}

function darkModeAdd() {
    document.body.classList.add("dark-mode");
    document.getElementsByTagName('header')[0].classList.add("dark-mode");
    document.getElementById('menu').classList.add("dark-mode");
    updateLightsButton(true);
}
function darkModeToggle() {
    var is_dark = document.body.classList.contains("dark-mode");
    // Add classes
    document.body.classList.toggle("dark-mode");
    document.getElementsByTagName('header')[0].classList.toggle("dark-mode");
    document.getElementById('menu').classList.toggle("dark-mode");
    hasDark = document.body.classList.contains("dark-mode");
    sessionStorage.setItem("dark-mode", hasDark);
    updateLightsButton(!is_dark);
}
function updateLightsButton(is_dark) {
    var lights = document.getElementById('lights');
    lights.classList.remove("fa-sun", "fa-moon");
    if(is_dark) {
       lights.classList.add("fa-sun"); 
    } else {
       lights.classList.add("fa-moon"); 
    }
}
