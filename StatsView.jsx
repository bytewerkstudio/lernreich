/* Lernreich — Statistik view (gamification-forward) */
function StatsView() {
  const D = window.DATA;
  const I = window.Icon;
  const { Ring, StatTile, Heatmap, WeekBars } = window;

  const todayXP = (D.totals[D.iso(D.today)] || {}).xp || 0;
  const todayPct = Math.round(Math.min(1, D.todaySec / D.goalSec) * 100);
  const lvlPct = D.xpInLevel / D.xpCost;

  return (
    <div>
      <div className="view-head">
        <div className="eyebrow">Übersicht</div>
        <h1 className="view-title">Deine Statistik</h1>
        <p className="view-sub">Fortschritt, Serien und Meilensteine auf einen Blick.</p>
      </div>

      <div className="stat-grid">
        <StatTile icon="clock" label="Heute" value={D.fmtHM(D.todaySec)} sub={`${todayPct}% vom Tagesziel`} />
        <StatTile icon="calendar" label="Diese Woche" value={D.fmtHM(D.weekSec)} sub={`+${todayXP} XP heute`} accent="#1f9d57" />
        <StatTile icon="flame" label="Serie" value={`${D.streak} Tage`} sub={`Rekord ${D.bestStreak} Tage`} accent="#e0894a" />
        <StatTile icon="bolt" label="Gesamt" value={D.fmtHM(D.totalSeconds)} sub={`${D.totalXP.toLocaleString('de')} XP gesammelt`} accent="#7257d6" />
      </div>

      {/* level hero */}
      <div className="card level-hero" style={{ marginBottom: 18 }}>
        <Ring value={lvlPct} size={104} stroke={11}>
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: 10, fontWeight: 800, color: 'var(--muted)', letterSpacing: '.5px' }}>LEVEL</div>
            <div className="mono" style={{ fontSize: 28, fontWeight: 700, lineHeight: 1 }}>{D.level}</div>
          </div>
        </Ring>
        <div className="lh-r">
          <div className="lh-lvl">LEVEL {D.level} · LERNZEIT-PROFI</div>
          <div className="lh-title">{D.xpCost - D.xpInLevel} XP bis Level {D.level + 1}</div>
          <div className="lh-track"><div style={{ width: (lvlPct * 100) + '%' }} /></div>
          <div className="lh-sub">{D.xpInLevel} / {D.xpCost} XP in diesem Level · {D.totalXP.toLocaleString('de')} XP insgesamt</div>
        </div>
      </div>

      <div className="stats-2col" style={{ marginBottom: 18 }}>
        <div className="card panel">
          <div className="panel-head">
            <div className="panel-title">Lern-Aktivität</div>
            <div className="panel-meta">{D.fmtHM(D.weekSec)} diese Woche</div>
          </div>
          <Heatmap weeks={17} />
        </div>

        <div className="card panel">
          <div className="panel-head">
            <div className="panel-title">Meilensteine</div>
            <div className="panel-meta">{D.milestones.filter((m) => m.done).length}/{D.milestones.length}</div>
          </div>
          <div className="miles">
            {D.milestones.map((m) => {
              const Ico = I[m.icon];
              return (
                <div key={m.id} className={'mile' + (m.done ? ' done' : ' locked')}>
                  <span className="m-ico"><Ico size={19} /></span>
                  <div style={{ minWidth: 0 }}>
                    <div className="m-l">{m.label}</div>
                    <div className="m-s">{m.sub}</div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      <div className="stats-2col">
        <div className="card panel">
          <div className="panel-head">
            <div className="panel-title">Diese Woche</div>
            <div className="panel-meta">Ziel {D.dailyGoalH} h / Tag</div>
          </div>
          <WeekBars />
        </div>

        <div className="card panel">
          <div className="panel-head">
            <div className="panel-title">Wiederholen</div>
            <div className="panel-meta">Spaced Repetition</div>
          </div>
          <div>
            {D.reviews.map((r, i) => (
              <div key={i} className="rev-item">
                <span className={'rev-dot' + (r.overdue ? ' over' : '')} />
                <div className="rev-main">
                  <div className="rev-topic">{r.topic}</div>
                  <div className="rev-sub">{r.subject}</div>
                </div>
                <span className={'rev-due' + (r.overdue ? ' over' : '')}>{r.due}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
window.StatsView = StatsView;
