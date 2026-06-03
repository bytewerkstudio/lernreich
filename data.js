/* Lernreich — deterministic mock data for the prototype */
(function () {
  // seeded RNG
  let s = 20260602;
  const rnd = () => { s = (s * 1664525 + 1013904223) % 4294967296; return s / 4294967296; };

  const DAY = 86400000;
  const today = new Date(2026, 5, 2); // 2 Jun 2026 (months 0-indexed)
  today.setHours(0, 0, 0, 0);
  const iso = (d) => d.toISOString().slice(0, 10);

  const subjects = [
    { name: 'Analysis II', tint: 0 },
    { name: 'Datenstrukturen', tint: 1 },
    { name: 'Organische Chemie', tint: 2 },
    { name: 'Statistik', tint: 3 },
    { name: 'Englisch B2', tint: 4 },
  ];

  const dailyGoalH = 2.0;
  const goalSec = dailyGoalH * 3600;

  // build ~140 days of activity with a believable rhythm + a live streak
  const totals = {};
  const days = 147;
  for (let i = days - 1; i >= 0; i--) {
    const d = new Date(today.getTime() - i * DAY);
    const dow = d.getDay(); // 0 Sun
    let base = 0.55;
    if (dow === 0) base = 0.32;             // Sun lighter
    if (dow === 6) base = 0.42;
    if (dow === 2 || dow === 3) base = 0.78; // mid-week heavy
    // occasional rest days
    const roll = rnd();
    let sec = 0;
    if (roll > 0.16) {
      const intensity = base * (0.5 + rnd() * 1.15);
      sec = Math.round(intensity * goalSec);
      sec = Math.min(sec, 9000);
    }
    // guarantee a strong recent streak (last 9 days all active)
    if (i < 9) sec = Math.max(sec, Math.round((0.45 + rnd() * 0.9) * goalSec));
    if (sec > 0) {
      const xp = Math.round(sec / 3600 * 100);
      totals[iso(d)] = { seconds: sec, xp };
    }
  }

  // streak (consecutive active days ending today)
  let streak = 0;
  for (let i = 0; ; i++) {
    const k = iso(new Date(today.getTime() - i * DAY));
    if (totals[k] && totals[k].seconds >= 600) streak++; else break;
  }

  const totalSeconds = Object.values(totals).reduce((a, b) => a + b.seconds, 0);
  const totalXP = Math.round(totalSeconds / 3600 * 100);

  // level math (matches the app)
  const level = Math.max(1, Math.floor((1 + Math.sqrt(1 + 0.08 * totalXP)) / 2));
  const xpForLevel = 50 * level * (level - 1);
  const xpInLevel = totalXP - xpForLevel;
  const xpCost = level * 100;

  const todaySec = (totals[iso(today)] || {}).seconds || 0;

  // this week (Mon start)
  const monday = new Date(today);
  const back = (monday.getDay() + 6) % 7;
  monday.setDate(monday.getDate() - back);
  let weekSec = 0;
  const weekBars = [];
  for (let i = 0; i < 7; i++) {
    const d = new Date(monday.getTime() + i * DAY);
    const sc = (totals[iso(d)] || {}).seconds || 0;
    if (d <= today) weekSec += sc;
    weekBars.push({ label: ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So'][i], seconds: sc, future: d > today, today: iso(d) === iso(today) });
  }

  // sessions list (recent)
  const sessions = [];
  const sessSubjects = ['Datenstrukturen', 'Analysis II', 'Statistik', 'Organische Chemie', 'Englisch B2', 'Analysis II', 'Datenstrukturen'];
  const sessGoals = ['AVL-Bäume wiederholen', 'Mehrfachintegrale üben', 'Hypothesentests', 'Reaktionsmechanismen', 'Vokabeln + Hörverstehen', 'Konvergenzkriterien', 'Hashing & Kollisionen'];
  for (let i = 0; i < 7; i++) {
    const d = new Date(today.getTime() - i * DAY);
    const sec = (totals[iso(d)] || {}).seconds || Math.round(1.2 * 3600);
    sessions.push({
      date: iso(d),
      subject: sessSubjects[i],
      goal: sessGoals[i],
      seconds: sec,
      xp: Math.round(sec / 3600 * 100),
      done: i % 4 !== 1,
    });
  }

  // journal entries
  const journal = [
    { date: iso(today), subject: 'Datenstrukturen', minutes: 95, text: 'AVL-Rotationen endlich verstanden — links-rechts-Fall war der Knackpunkt. Morgen Rot-Schwarz-Bäume.', tags: ['Durchbruch'] },
    { date: iso(new Date(today.getTime() - DAY)), subject: 'Analysis II', minutes: 70, text: 'Satz von Fubini durchgerechnet. Reihenfolge der Integration noch unsicher, Übung 4 offen.', tags: ['Wiederholen'] },
    { date: iso(new Date(today.getTime() - 2 * DAY)), subject: 'Statistik', minutes: 60, text: 'p-Wert vs. Signifikanzniveau geklärt. Karteikarten für Verteilungen angelegt.', tags: [] },
    { date: iso(new Date(today.getTime() - 3 * DAY)), subject: 'Organische Chemie', minutes: 110, text: 'SN1/SN2 Mechanismen — Übersichtstabelle gemacht. Stereochemie sitzt jetzt.', tags: ['Durchbruch'] },
    { date: iso(new Date(today.getTime() - 5 * DAY)), subject: 'Englisch B2', minutes: 45, text: 'Listening Unit 6. Neue Vokabeln in Anki. Aussprache /θ/ üben.', tags: [] },
  ];

  // spaced-repetition reviews due
  const reviews = [
    { subject: 'Datenstrukturen', topic: 'AVL-Rotationen', due: 'morgen', overdue: false },
    { subject: 'Organische Chemie', topic: 'SN1/SN2 Mechanismen', due: 'heute', overdue: true },
    { subject: 'Analysis II', topic: 'Konvergenzkriterien', due: 'in 3 Tagen', overdue: false },
  ];

  // milestones / achievements (gamification)
  const milestones = [
    { id: 'streak7', icon: 'flame', label: '7-Tage-Serie', sub: 'Eine Woche am Stück', done: true },
    { id: 'h100', icon: 'clock', label: '100 Stunden', sub: 'Gesamt-Fokuszeit', done: true },
    { id: 'early', icon: 'sun', label: 'Frühaufsteher', sub: '5× vor 8 Uhr gelernt', done: true },
    { id: 'lvl20', icon: 'trophy', label: 'Level 20', sub: `Noch ${20 - level} Level`, done: false },
    { id: 'streak30', icon: 'bolt', label: '30-Tage-Serie', sub: `${streak}/30 Tage`, done: false },
    { id: 'h250', icon: 'target', label: '250 Stunden', sub: 'Marathon-Lerner', done: false },
  ];

  function fmtHM(sec) {
    const m = Math.round(sec / 60);
    const h = Math.floor(m / 60), mm = m % 60;
    if (h && mm) return `${h} h ${mm} min`;
    if (h) return `${h} h`;
    return `${mm} min`;
  }

  window.DATA = {
    today, iso, totals, streak, bestStreak: Math.max(streak, 14),
    totalSeconds, totalXP, level, xpInLevel, xpCost,
    todaySec, weekSec, weekBars, dailyGoalH, goalSec,
    sessions, journal, reviews, milestones, subjects, monday,
    fmtHM,
    user: { name: 'Hijrat', initials: 'H' },
    sessionsCount: Object.keys(totals).length,
  };
})();
