+++
title = "Search"
description = "Fast, low-bandwidth client-side search."
showpagemeta = false
+++

<link href="/pagefind/pagefind-ui.css" rel="stylesheet">

<div id="search" class="search-container"></div>

<script src="/pagefind/pagefind-ui.js"></script>

<script>
  window.addEventListener('DOMContentLoaded', (event) => {
    new PagefindUI({
      element: "#search",
      resetStyles: false,
      showSubResults: true, // Shows matches within headings
      showImages: false,    // Set to true if you want post images in results
      translations: {
        placeholder: "Enter your search query here"
      }
    });
  });
</script>

<style>
.search-container {
    width: 100%;
    margin-top: 2rem;
  }

  /* Light Mode Defaults (General) */
  :root {
    --pagefind-ui-font: open sans, sans-serif;
    --pagefind-ui-primary: var(--fg-color);      /* Links and buttons */
    --pagefind-ui-text: #393939;         /* Main text */
    --pagefind-ui-background: var(--bg-color);   /* Result cards background */
    --pagefind-ui-border: #eeeeee;       /* Lines and borders */
    --pagefind-ui-tag: #f4f4f4;          /* Filter tags */
  }

  /* Dark Mode Overrides */
  body.dark-mode {
    --pagefind-ui-font: open sans, sans-serif;
    --pagefind-ui-primary: #8ab4f8;      /* Softer blue for dark backgrounds */
    --pagefind-ui-text: #e8eaed;         /* Light grey text */
    --pagefind-ui-background: #1a1b1e;   /* Match your dark mode bg */
    --pagefind-ui-border: #3c4043;       /* Darker borders */
    --pagefind-ui-tag: #2d2e31;
  }

  /* Accessibility & Layout Fixes */
  /* Ensures the search input text is visible in dark mode */
  body.dark-mode .pagefind-ui__search-input {
    background-color: var(--pagefind-ui-background);
    color: var(--pagefind-ui-text);
  }

  /* Makes the 'Clear' button and 'No results' text adapt */
  body.dark-mode .pagefind-ui__drawer,
  body.dark-mode .pagefind-ui__result-link,
  body.dark-mode .pagefind-ui__result-excerpt {
    color: var(--pagefind-ui-text);
  }
  /* Force visibility on the Search Input */
  .pagefind-ui__search-input {
    background-color: var(--pagefind-ui-background) !important;
    color: var(--pagefind-ui-text) !important;
    border: 2px solid var(--pagefind-ui-border) !important;
    opacity: 1 !important; /* Ensure it's not faded out */
  }

  /* Style the placeholder text ("Enter your search query here") */
  .pagefind-ui__search-input::placeholder {
    color: var(--pagefind-ui-text) !important;
    opacity: 0.6; /* Makes it look like a placeholder but still readable */
  }

  /* Specific fix for Light Mode visibility */
  body:not(.dark-mode) {
    --pagefind-ui-text: #1a1a1a;
    --pagefind-ui-background: #ffffff;
    --pagefind-ui-border: #cccccc; /* Darker border for light mode */
  }

  /* Clear button (the 'X' that appears when typing) */
  .pagefind-ui__search-clear {
    color: var(--pagefind-ui-text) !important;
    background-color: var(--pagefind-ui-background) !important;
  }

  
  /* Reduce padding on the individual result container */
  .pagefind-ui__result {
    padding-top: 10px !important;
    padding-bottom: 10px !important;
    border-bottom: none;
  }

  /* Tighten the gap between the title and the excerpt text */
  .pagefind-ui__result-inner {
    margin-top: 0 !important;
  }

  /* Reduce the font size of the excerpt if it feels too bulky */
  .pagefind-ui__result-excerpt {
    font-size: 0.9rem;
    margin-top: 4px !important;
  }

  /* Remove the default bottom border from the very last result */
  .pagefind-ui__result:last-child {
    border-bottom: none;
  }
  /* Remove double underlining from search result titles */
  .pagefind-ui__result-link {
      text-decoration: none !important;
      display: inline-block; /* Helps with spacing consistency */
  }

  /* If you want the underline back only on hover */
  .pagefind-ui__result-link:hover {
      text-decoration: underline !important;
  }

  /* Ensure the result title isn't inheriting weird colors */
  .pagefind-ui__result-title {
      display: inline;
  }
</style>
