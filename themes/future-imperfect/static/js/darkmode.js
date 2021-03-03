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
}
function darkModeToggle() {
    document.body.classList.toggle("dark-mode");
    document.getElementsByTagName('header')[0].classList.toggle("dark-mode");
    document.getElementById('menu').classList.toggle("dark-mode");
    hasDark = document.body.classList.contains("dark-mode");
    sessionStorage.setItem("dark-mode", hasDark);
}
