// Jahreszahl im Footer
document.getElementById("year").textContent = new Date().getFullYear();

// Download-Tracking
// Auf GitHub Pages wird kein Netlify-Formular-Tracking benötigt.
// Der Download startet nun nativ und ohne künstliche Verzögerung direkt über den Browser.


/* ==========================================================================
   MINIMALISTISCHES PREMIUM REDESIGN INTERAKTIVITÄT
   ========================================================================== */

/* ---------- 1. Dark Mode Steuerung ---------- */
const themeToggleBtn = document.getElementById("theme-toggle");
const darkIcon = document.getElementById("theme-toggle-dark-icon");
const lightIcon = document.getElementById("theme-toggle-light-icon");

if (themeToggleBtn && darkIcon && lightIcon) {
  // Check local storage, defaults to dark theme on first visit
  const storedTheme = localStorage.getItem("theme");
  const initialTheme = storedTheme || "dark";

  // Set initial theme state
  document.documentElement.setAttribute("data-theme", initialTheme);
  updateThemeToggleIcons(initialTheme);

  themeToggleBtn.addEventListener("click", () => {
    const currentTheme = document.documentElement.getAttribute("data-theme");
    const newTheme = currentTheme === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", newTheme);
    localStorage.setItem("theme", newTheme);
    updateThemeToggleIcons(newTheme);
    
    // Sync theme with embedded mockup iframe
    const iframe = document.querySelector("#appMockup iframe");
    if (iframe && iframe.contentWindow) {
      iframe.contentWindow.postMessage({ type: 'setTheme', theme: newTheme }, '*');
    }
  });
}

function updateThemeToggleIcons(theme) {
  if (theme === "dark") {
    darkIcon.style.display = "none";
    lightIcon.style.display = "block";
    document.querySelector('meta[name="theme-color"]').setAttribute("content", "#090a0c");
  } else {
    darkIcon.style.display = "block";
    lightIcon.style.display = "none";
    document.querySelector('meta[name="theme-color"]').setAttribute("content", "#f8f8f6");
  }
}

/* ---------- 5. Collapsible Sections Steuerung (Single Page Layout) ---------- */
document.addEventListener("DOMContentLoaded", () => {
  const sections = {
    features: document.getElementById("features"),
    how: document.getElementById("how")
  };

  const navLinks = {
    features: document.querySelectorAll('a[href="#features"]'),
    how: document.querySelectorAll('a[href="#how"]')
  };

  function toggleSection(sectionKey, forceExpand = null) {
    const sec = sections[sectionKey];
    if (!sec) return;

    const isExpanded = sec.classList.contains("expanded");
    const shouldExpand = forceExpand !== null ? forceExpand : !isExpanded;

    if (shouldExpand) {
      sec.classList.add("expanded");
      if (navLinks[sectionKey]) {
        navLinks[sectionKey].forEach(link => link.classList.add("active-expanded"));
      }
      
      // Scroll smoothly to the newly expanded section
      setTimeout(() => {
        sec.scrollIntoView({ behavior: "smooth", block: "start" });
      }, 100);
    } else {
      sec.classList.remove("expanded");
      if (navLinks[sectionKey]) {
        navLinks[sectionKey].forEach(link => link.classList.remove("active-expanded"));
      }
      // Scroll back up to top smoothly if we are collapsing it
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  }

  // Bind clicks for features
  if (navLinks.features) {
    navLinks.features.forEach(link => {
      link.addEventListener("click", (e) => {
        e.preventDefault();
        toggleSection("features");
      });
    });
  }

  // Bind clicks for how
  if (navLinks.how) {
    navLinks.how.forEach(link => {
      link.addEventListener("click", (e) => {
        e.preventDefault();
        toggleSection("how");
      });
    });
  }
});
