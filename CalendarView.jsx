/* Lernreich — Kalender view */
function CalendarView() {
  const D = window.DATA;
  const I = window.Icon;
  const MN = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'];
  const [ym, setYm] = React.useState({ y: D.today.getFullYear(), m: D.today.getMonth() });

  const shift = (d) => setYm((p) => {
    let m = p.m + d, y = p.y;
    if (m < 0) { m = 11; y--; } if (m > 11) { m = 0; y++; }
    return { y, m };
  });

  const first = new Date(ym.y, ym.m, 1);
  const lead = (first.getDay() + 6) % 7; // Mon start
  const daysIn = new Date(ym.y, ym.m + 1, 0).getDate();

  const cells = [];
  for (let i = 0; i < lead; i++) cells.push(null);
  for (let d = 1; d <= daysIn; d++) cells.push(d);
  while (cells.length % 7 !== 0) cells.push(null);

  // month stats
  let monthSec = 0, activeDays = 0, bestSec = 0, bestDay = null;
  for (let d = 1; d <= daysIn; d++) {
    const k = D.iso(new Date(ym.y, ym.m, d));
    const sc = (D.totals[k] || {}).seconds || 0;
    if (sc > 0) { monthSec += sc; activeDays++; }
    if (sc > bestSec) { bestSec = sc; bestDay = d; }
  }
  const goalSec = D.goalSec;

  const heatColor = (sc) => {
    if (sc <= 0) return null;
    const f = sc / goalSec;
    const pct = f >= 1 ? 100 : f >= 0.6 ? 72 : f >= 0.25 ? 46 : 26;
    return `color-mix(in oklab, var(--accent) ${pct}%, var(--heat-0))`;
  };

  return (
    <div>
      <div className="view-head">
        <div className="eyebrow">Verlauf</div>
        <h1 className="view-title">Lern-Kalender</h1>
        <p className="view-sub">Jeder ausgefüllte Tag zählt — halte deine Serie am Leben.</p>
      </div>

      <div className="stats-2col">
        <div className="card panel">
          <div className="cal-head">
            <div className="cal-month">{MN[ym.m]} {ym.y}</div>
            <div className="cal-nav">
              <button className="icon-btn" onClick={() => shift(-1)}><I.chevL /></button>
              <button className="icon-btn" onClick={() => shift(1)}><I.chevR /></button>
            </div>
          </div>
          <div className="cal-grid">
            {['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So'].map((d) => <div key={d} className="cal-dow">{d}</div>)}
            {cells.map((d, i) => {
              if (d === null) return <div key={i} className="cal-cell empty" />;
              const dateObj = new Date(ym.y, ym.m, d);
              const sc = (D.totals[D.iso(dateObj)] || {}).seconds || 0;
              const isToday = D.iso(dateObj) === D.iso(D.today);
              const col = heatColor(sc);
              const barW = sc > 0 ? Math.max(28, Math.min(100, sc / goalSec * 100)) : 0;
              return (
                <div key={i} className={'cal-cell' + (isToday ? ' today' : '')}>
                  <div className="cn">{d}</div>
                  {sc > 0 && <div className="cm">{Math.round(sc / 60)}m</div>}
                  {sc > 0 && <div className="cbar" style={{ width: barW + '%', background: col }} />}
                </div>
              );
            })}
          </div>
          <div className="cal-legend">
            <span>weniger</span>
            {[0.2, 0.4, 0.7, 1].map((f, i) => (
              <span key={i} className="hm-cell" style={{ width: 13, height: 13, background: heatColor(f * goalSec) }} />
            ))}
            <span>mehr</span>
          </div>
        </div>

        <div className="cal-side">
          <div className="card panel">
            <div className="panel-title" style={{ marginBottom: 14 }}>{MN[ym.m]} im Überblick</div>
            <div className="ov-list">
              <div className="ov-row"><span className="ov-k">Gesamt</span><span className="ov-v mono">{D.fmtHM(monthSec)}</span></div>
              <div className="ov-row"><span className="ov-k">Lerntage</span><span className="ov-v mono">{activeDays}</span></div>
              <div className="ov-row"><span className="ov-k">Ø pro Lerntag</span><span className="ov-v mono">{activeDays ? D.fmtHM(monthSec / activeDays) : '—'}</span></div>
              <div className="ov-row"><span className="ov-k">Bester Tag</span><span className="ov-v mono">{bestDay ? `${bestDay}. (${D.fmtHM(bestSec)})` : '—'}</span></div>
            </div>
          </div>

          <div className="card panel" style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
            <span className="m-ico" style={{ width: 42, height: 42, borderRadius: 12, background: 'var(--accent)', color: 'var(--accent-ink)', display: 'grid', placeItems: 'center', flex: '0 0 42px' }}>
              <I.flame size={22} />
            </span>
            <div style={{ minWidth: 0 }}>
              <div style={{ fontSize: 17, fontWeight: 800, whiteSpace: 'nowrap' }}>{D.streak} Tage Serie</div>
              <div className="st-sub">Lern heute, um sie zu verlängern.</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
window.CalendarView = CalendarView;
