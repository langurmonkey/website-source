if(sessionStorage.getItem("dark-mode") == "true"){
    // Toggle dark-mode class if dark-mode sessionStorage is true
    console.log("Add dark mode (session storage)");
    darkModeAdd();
} else if (window.matchMedia && 
    window.matchMedia('(prefers-color-scheme: dark)').matches && 
    sessionStorage.getItem("dark-mode") == null) {
    console.log("Add dark mode (browser prefers-color-scheme)");
    // Check browser setting
    darkModeAdd();
}
function darkModeAdd(){
    document.body.classList.add("dark-mode");
    document.getElementsByTagName('header')[0].classList.add("dark-mode");
    document.getElementById('menu').classList.add("dark-mode");
}
function darkModeToggle(additem) {
    document.body.classList.toggle("dark-mode");
    document.getElementsByTagName('header')[0].classList.toggle("dark-mode");
    document.getElementById('menu').classList.toggle("dark-mode");
    if (additem) {
        hasDark = document.body.classList.contains("dark-mode");
        sessionStorage.setItem("dark-mode", hasDark);
    }
}
