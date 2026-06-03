/* Lernreich — Timer view (setup + active) */
const FOCUS_ITEMS = ['Handy weggelegt', 'Wasser bereit', 'Aufgabe klar', 'Tabs geschlossen'];

function fmtClock(sec) {
  sec = Math.max(0, Math.floor(sec));
  const h = Math.floor(sec / 3600), m = Math.floor((sec % 3600) / 60), s = sec % 60;
  const p = (n) => String(n).padStart(2, '0');
  return `${p(h)}:${p(m)}:${p(s)}`;
}

function TimerView({ tm, api }) {
  const D = window.DATA;
  const I = window.Icon;
  const { Ring, Slider } = window;

  if (tm.phase === 'active') {
    const targetSec = tm.durationMin * 60;
    const prog = Math.min(1, tm.elapsed / targetSec);
    const earned = Math.floor(tm.elapsed / 3600 * 100);
    const remain = Math.max(0, targetSec - tm.elapsed);
    const isBreak = tm.onBreak;
    return (
      <div className="active-wrap">
        <div className={'active-phase' + (isBreak ? ' break' : '')}>
          {isBreak ? 'Pause' : (tm.running ? 'Fokus läuft' : 'Pausiert')}
        </div>
        <div className="active-subject">{tm.subject || 'Allgemein'}</div>
        <div className="active-goal">{tm.goal || 'Konzentriert arbeiten'}</div>

        <Ring value={isBreak ? (tm.breakElapsed / (5 * 60)) : prog} size={250} stroke={15}
          color={isBreak ? 'var(--muted)' : 'var(--accent)'}>
          <div>
            <div className="ring-time mono">{fmtClock(isBreak ? tm.breakElapsed : tm.elapsed)}</div>
            <div className="ring-cap">{isBreak ? 'Pause · 5 min' : `Ziel ${tm.durationMin} min · ${Math.round(prog * 100)}%`}</div>
          </div>
        </Ring>

        <div className="active-meta">
          <div className="am-item"><div className="am-v mono" style={{ color: 'var(--accent)' }}>+{earned}</div><div className="am-k">XP verdient</div></div>
          <div className="am-item"><div className="am-v mono">{Math.ceil(remain / 60)}</div><div className="am-k">Min übrig</div></div>
          <div className="am-item"><div className="am-v">{D.streak}</div><div className="am-k">Tage Serie</div></div>
        </div>

        <div className="active-actions">
          <button className="btn btn-primary" onClick={api.toggleRun}>
            {tm.running ? <I.pause /> : <I.play />} {tm.running ? 'Pause' : 'Weiter'}
          </button>
          <button className="btn btn-ghost" onClick={api.toggleBreak}>
            <I.coffee /> {isBreak ? 'Pause beenden' : 'Kurze Pause'}
          </button>
          <button className="btn btn-ghost" onClick={api.finish}>
            <I.stop /> Beenden
          </button>
        </div>
        <div className="active-note">
          {prog >= 1 ? 'Ziel erreicht — du kannst ohne XP-Verlust beenden.' : 'Bewusst abbrechen: 3–5 min −10 %, danach −80 % der Session-XP.'}
        </div>
      </div>
    );
  }

  // ---- setup ----
  const todayPct = Math.min(1, D.todaySec / D.goalSec);
  return (
    <div className="timer-wrap">
      <div className="view-head">
        <div className="eyebrow">Fokus-Sitzung</div>
        <h1 className="view-title">Bereit für den nächsten Fokus?</h1>
        <p className="view-sub">Bereite deinen Kopf vor, schließe Ablenkungen und starte deine Session.</p>
      </div>

      <div className="card today-strip">
        <Ring value={todayPct} size={62} stroke={7}>
          <span className="mono" style={{ fontSize: 13, fontWeight: 700 }}>{Math.round(todayPct * 100)}%</span>
        </Ring>
        <div className="ts-info">
          <div className="ts-k">Heute gelernt</div>
          <div className="ts-v mono">{D.fmtHM(D.todaySec)} <small>/ {D.dailyGoalH} h Tagesziel</small></div>
          <div className="ts-bar"><div style={{ width: (todayPct * 100) + '%' }} /></div>
        </div>
        <div style={{ textAlign: 'right' }}>
          <div className="ts-k">Serie</div>
          <div className="ts-v" style={{ display: 'flex', alignItems: 'center', gap: 6, justifyContent: 'flex-end' }}>
            <I.flame size={18} style={{ color: 'var(--accent)' }} />{D.streak}
          </div>
        </div>
      </div>

      <div className="card setup-card">
        <div className="setup-sec">
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
            <div>
              <label className="field-label">Fach</label>
              <input className="input" value={tm.subject} onChange={(e) => api.set('subject', e.target.value)} placeholder="z. B. Analysis II" />
            </div>
            <div>
              <label className="field-label">Konkretes Lernziel</label>
              <input className="input" value={tm.goal} onChange={(e) => api.set('goal', e.target.value)} placeholder="z. B. Kapitel 4 wiederholen" />
            </div>
          </div>
        </div>

        <div className="setup-sec">
          <div className="sec-title">Einstellungen</div>
          <div className="slider-row">
            <span className="srl">Fokus-Dauer</span>
            <Slider value={tm.durationMin} min={5} max={150} step={5} onChange={(v) => api.set('durationMin', v)} format={(v) => `${v} min`} />
          </div>
          <div className="slider-row">
            <span className="srl">Erinnerung alle</span>
            <Slider value={tm.popupMin} min={5} max={90} step={5} onChange={(v) => api.set('popupMin', v)} format={(v) => `${v} min`} />
          </div>
          <div className="slider-row">
            <span className="srl">Tagesziel</span>
            <Slider value={tm.dailyGoalH} min={0.5} max={12} step={0.5} onChange={(v) => api.set('dailyGoalH', v)} format={(v) => `${v.toFixed(1)} h`} />
          </div>
        </div>

        <div className="setup-sec">
          <div className="sec-title">Fokus-Vorbereitung</div>
          <div className="checklist">
            {FOCUS_ITEMS.map((item, i) => (
              <div key={i} className={'chk' + (tm.checklist[i] ? ' on' : '')} onClick={() => api.toggleCheck(i)}>
                <span className="box"><I.check /></span>{item}
              </div>
            ))}
          </div>
        </div>

        <div className="setup-actions">
          <button className="btn btn-primary" onClick={api.start}><I.play /> Fokus starten</button>
          <button className="btn btn-ghost" onClick={api.start}><I.resume /> Sitzung fortsetzen</button>
        </div>
      </div>
    </div>
  );
}
window.TimerView = TimerView;
