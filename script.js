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


/* ---------- 2. App Mockup: Tab Steuerung ---------- */
const sidebarBtns = document.querySelectorAll(".app-mockup .nav-item");
const tabContents = document.querySelectorAll(".app-mockup .mockup-tab-content");

if (sidebarBtns.length > 0 && tabContents.length > 0) {
  sidebarBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      sidebarBtns.forEach((b) => b.classList.remove("active"));
      tabContents.forEach((c) => c.style.display = "none");
      
      btn.classList.add("active");
      const targetTab = btn.getAttribute("data-tab");
      const targetEl = document.getElementById(`tab-${targetTab}`);
      if (targetEl) {
        targetEl.style.display = "flex";
      }
    });
  });
}


/* ---------- 3. App Mockup: Checkboxen-Validator & Timer ---------- */
const btnStartFocus = document.getElementById("btn-start-focus");
const focusCheckboxes = document.querySelectorAll(".timer-setup .check-item input[type='checkbox']");

if (btnStartFocus && focusCheckboxes.length > 0) {
  const checkCheckboxes = () => {
    const allChecked = Array.from(focusCheckboxes).every((cb) => cb.checked);
    btnStartFocus.disabled = !allChecked;
  };

  focusCheckboxes.forEach((cb) => {
    cb.addEventListener("change", checkCheckboxes);
  });
  // Init
  checkCheckboxes();
}

// Timer Variables
const timerSetup = document.getElementById("mockup-timer-setup");
const timerActive = document.getElementById("mockup-timer-active");
const activeSubject = document.getElementById("mockup-active-subject");
const subjectInput = document.getElementById("mockup-subject");
const timeDisplay = document.getElementById("mockup-time-display");
const btnAbortFocus = document.getElementById("btn-abort-focus");
const btnCompleteFocus = document.getElementById("btn-complete-focus");
const svgProgress = document.getElementById("timer-svg-progress");
const toast = document.getElementById("mockup-toast");

// XP & Leveling Variables
const currentXpEl = document.getElementById("mockup-xp-current");
const levelEl = document.getElementById("mockup-level");
const xpBar = document.getElementById("mockup-xp-bar");
const streakEl = document.getElementById("mockup-streak");
const statsStreakEl = document.getElementById("mockup-stats-streak");

let timerInterval = null;
let totalTime = 25 * 60; // 25 minutes
let timeLeft = totalTime;
let currentLevel = 3;
let currentXp = 240;
let maxXp = 300;
let currentStreak = 5;

if (btnStartFocus && timerSetup && timerActive) {
  btnStartFocus.addEventListener("click", () => {
    const subject = (subjectInput && subjectInput.value.trim()) || "Konzentriertes Arbeiten";
    if (activeSubject) activeSubject.textContent = subject;
    
    timerSetup.style.display = "none";
    timerActive.style.display = "flex";
    
    timeLeft = totalTime;
    updateTimerDisplay();
    
    if (svgProgress) {
      svgProgress.style.strokeDashoffset = "440";
    }
    
    // In our live mockup, let's make the countdown run snappily (accelerated for dynamic presentation)
    timerInterval = setInterval(() => {
      timeLeft--;
      updateTimerDisplay();
      
      if (svgProgress) {
        const progressPercent = timeLeft / totalTime;
        svgProgress.style.strokeDashoffset = (440 * (1 - progressPercent)).toString();
      }
      
      if (timeLeft <= 0) {
        completeSession();
      }
    }, 400); // 400ms = 1 simulated second
  });
}

function updateTimerDisplay() {
  if (!timeDisplay) return;
  const minutes = Math.floor(timeLeft / 60);
  const seconds = timeLeft % 60;
  timeDisplay.textContent = `${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;
}

if (btnAbortFocus) {
  btnAbortFocus.addEventListener("click", () => {
    resetTimer();
    
    // Deduct a little XP
    currentXp = Math.max(0, currentXp - 25);
    updateXpSidebar();
    
    if (timerActive) timerActive.style.display = "none";
    if (timerSetup) timerSetup.style.display = "flex";
  });
}

if (btnCompleteFocus) {
  btnCompleteFocus.addEventListener("click", () => {
    completeSession();
  });
}

function completeSession() {
  resetTimer();
  
  currentXp += 60;
  currentStreak += 1;
  
  let levelUp = false;
  if (currentXp >= maxXp) {
    currentXp = currentXp - maxXp;
    currentLevel += 1;
    maxXp = currentLevel * 100; // increase level limit dynamically
    levelUp = true;
  }
  
  if (toast) {
    toast.classList.add("show");
    const tStrong = toast.querySelector("strong");
    const tSpan = toast.querySelector("span");
    
    if (levelUp) {
      if (tStrong) tStrong.textContent = "LEVEL UP! 🎉";
      if (tSpan) tSpan.textContent = `Du hast Level ${currentLevel} erreicht!`;
    } else {
      if (tStrong) tStrong.textContent = "Sitzung beendet! ✨";
      if (tSpan) tSpan.textContent = "+60 XP & Lernzeit gesammelt";
    }
    
    setTimeout(() => {
      toast.classList.remove("show");
    }, 3800);
  }
  
  updateXpSidebar();
  
  if (timerActive) timerActive.style.display = "none";
  if (timerSetup) timerSetup.style.display = "flex";
}

function resetTimer() {
  clearInterval(timerInterval);
  timerInterval = null;
}

function updateXpSidebar() {
  if (currentXpEl) currentXpEl.textContent = currentXp.toString();
  if (levelEl) levelEl.textContent = currentLevel.toString();
  if (streakEl) streakEl.textContent = currentStreak.toString();
  if (statsStreakEl) statsStreakEl.textContent = currentStreak.toString();
  
  if (xpBar) {
    const xpPercent = Math.min(100, (currentXp / maxXp) * 100);
    xpBar.style.width = `${xpPercent}%`;
  }
  
  // Dynamically update simulated values in the Stats Tab
  const sessionsVal = document.querySelector(".stat-card:nth-child(3) .stat-val");
  const timeVal = document.querySelector(".stat-card:nth-child(1) .stat-val");
  if (sessionsVal && timeVal) {
    sessionsVal.textContent = `${48 + (currentStreak - 5)} Einheiten`;
    timeVal.textContent = `${(34.5 + (currentStreak - 5) * 0.4).toFixed(1)} Std.`;
  }
}


/* ---------- 4. App Mockup: Heatmap Befüllen ---------- */
const heatmap = document.getElementById("mockup-heatmap");
if (heatmap) {
  heatmap.innerHTML = "";
  // 105 cells (7x15 matrix)
  const levels = [
    0, 0, 0, 1, 0, 2, 0, 0, 1, 3, 0, 0, 2, 0, 4,
    0, 1, 0, 0, 3, 0, 1, 0, 0, 2, 0, 0, 1, 0, 0,
    2, 0, 0, 4, 0, 0, 3, 0, 1, 0, 0, 2, 0, 0, 3,
    0, 0, 1, 0, 0, 2, 0, 0, 4, 0, 0, 3, 0, 1, 0,
    0, 2, 0, 0, 3, 0, 1, 0, 0, 2, 0, 0, 4, 0, 0,
    1, 0, 0, 2, 0, 0, 3, 0, 1, 0, 0, 2, 0, 0, 4,
    0, 0, 3, 0, 1, 0, 0, 2, 0, 0, 4, 0, 0, 1, 0
  ];
  
  levels.forEach((lvl) => {
    const cell = document.createElement("div");
    cell.className = `heatmap-cell level-${lvl}`;
    const hrs = lvl === 0 ? "Keine Fokuszeit" : `${(lvl * 0.8 + 0.5).toFixed(1)} Std. gelernt`;
    cell.setAttribute("title", hrs);
    heatmap.appendChild(cell);
  });
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
