/* Lernreich — Sidebar */
function Sidebar({ view, setView, theme, toggleTheme, onSettings }) {
  const D = window.DATA;
  const I = window.Icon;
  const nav = [
    { id: 'timer', label: 'Fokus-Timer', icon: I.timer },
    { id: 'stats', label: 'Statistik', icon: I.stats },
    { id: 'calendar', label: 'Kalender', icon: I.calendar },
    { id: 'journal', label: 'Journal', icon: I.journal },
  ];

  // last 7 days streak dots
  const dots = [];
  for (let i = 6; i >= 0; i--) {
    const d = new Date(D.today.getTime() - i * 86400000);
    const t = D.totals[D.iso(d)];
    dots.push(!!(t && t.seconds >= 600));
  }

  const pct = Math.min(100, Math.round(D.xpInLevel / D.xpCost * 100));

  return (
    <aside className="sidebar">
      <div className="brand">
        <img src="assets/lernreich.png" alt="Lernreich" />
        <div>
          <div className="bn">Lernreich</div>
          <div className="bv">FOCUS TIMER</div>
        </div>
      </div>

      <div className="profile">
        <div className="pf-top">
          <div className="avatar">{D.user.initials}</div>
          <div style={{ minWidth: 0 }}>
            <div className="pf-name">{D.user.name}</div>
            <div className="pf-sub">
              <I.flame size={13} style={{ color: 'var(--accent)' }} />
              {D.streak} Tage Serie
            </div>
          </div>
        </div>
        <div className="streak-dots">
          {dots.map((on, i) => <div key={i} className={'streak-dot' + (on ? ' on' : '')} />)}
        </div>
      </div>

      <nav className="nav">
        <div className="nav-label">Navigation</div>
        {nav.map((n) => {
          const Ico = n.icon;
          return (
            <button key={n.id} className={'nav-btn' + (view === n.id ? ' active' : '')} onClick={() => setView(n.id)}>
              <Ico /> {n.label}
            </button>
          );
        })}
      </nav>

      <div className="side-spacer" />

      <div className="xp-card">
        <div className="xp-row">
          <div className="xp-lvl"><span className="chip">LVL {D.level}</span></div>
          <div className="xp-num">{D.xpInLevel} / {D.xpCost} XP</div>
        </div>
        <div className="xp-track"><div className="xp-fill" style={{ width: pct + '%' }} /></div>
        <div className="xp-num" style={{ marginTop: 7, fontSize: 11, color: 'var(--faint)' }}>
          Noch {D.xpCost - D.xpInLevel} XP bis Level {D.level + 1}
        </div>
      </div>

      <div className="side-tools">
        <button className="icon-btn" title="Einstellungen" onClick={onSettings}><I.settings /></button>
        <button className="icon-btn" title="Farbschema" onClick={toggleTheme}>
          {theme === 'dark' ? <I.sun /> : <I.moon />}
        </button>
        <span className="ver">v1.3</span>
      </div>
    </aside>
  );
}
window.Sidebar = Sidebar;
