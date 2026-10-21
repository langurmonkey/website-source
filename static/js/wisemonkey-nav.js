/* ── Wisemonkey top nav: collapse the links behind a hamburger on narrow screens ──
   Shared by /projects/wisemonkey/ and its docs page. The links are hidden by a
   media query; this only toggles the `open` class, keeps ARIA state in sync, and
   resets the menu when the viewport grows back past the breakpoint.
*/
(() => {
  const toggle = document.querySelector('.nav-toggle');
  const links = document.getElementById('nav-links');
  if (!toggle || !links) return;

  const BREAKPOINT = 860;

  function setOpen(open) {
    links.classList.toggle('open', open);
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
  }

  toggle.addEventListener('click', () => setOpen(!links.classList.contains('open')));

  // Anchor clicks navigate within the page, so the panel must not stay open.
  links.addEventListener('click', (e) => {
    if (e.target.closest('a')) setOpen(false);
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') setOpen(false);
  });

  // Clicking anywhere outside the nav closes it.
  document.addEventListener('click', (e) => {
    if (!e.target.closest('nav')) setOpen(false);
  });

  // Growing past the breakpoint shows the inline links again; drop the stale state.
  let resizeTimer = 0;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
      if (window.innerWidth > BREAKPOINT) setOpen(false);
    }, 150);
  });
})();
