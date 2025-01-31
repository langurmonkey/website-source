function createLanguageTag(highlightDiv) {
    // Find language
    codes = highlightDiv.getElementsByTagName("code");
    datalang = null;
    for (i =0; i < codes.length; i++){
        if(codes[i].hasAttribute("data-lang")){
            datalang = codes[i].getAttribute("data-lang");
            break;
        }
    }
    if (datalang != null && datalang != "fallback") {
        const langblock = document.createElement("div");
        langblock.className = "data-language-block";
        langblock.innerText = datalang;
        addLanguageTagToDom(langblock, highlightDiv);
    }
}
function addLanguageTagToDom(button, highlightDiv) {
    highlightDiv.insertBefore(button, highlightDiv.firstChild);
    const wrapper = document.createElement("div");
    wrapper.className = "highlight-wrapper";
    highlightDiv.parentNode.insertBefore(wrapper, highlightDiv);
    wrapper.appendChild(highlightDiv);
}
document.querySelectorAll(".highlight")
    .forEach(highlightDiv => createLanguageTag(highlightDiv));
