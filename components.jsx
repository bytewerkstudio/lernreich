/* Lernreich — shared UI components */

function Ring({ value, size = 220, stroke = 14, track, color, children, rounded = true }) {
  const r = (size - stroke) / 2;
  const c = 2 * Math.PI * r;
  const off = c * (1 - Math.max(0, Math.min(1, value)));
  return (
    <div style={{ position: 'relative', width: size, height: size }}>
      <svg width={size} height={size} style={{ transform: 'rotate(-90deg)' }}>
        <circle cx={size / 2} cy={size / 2} r={r} fill="none"
          stroke={track || 'var(--heat-track)'} strokeWidth={stroke} />
        <circle cx={size / 2} cy={size / 2} r={r} fill="none"
          stroke={color || 'var(--accent)'} strokeWidth={stroke}
          strokeDasharray={c} strokeDashoffset={off}
          strokeLinecap={rounded ? 'round' : 'butt'}
          style={{ transition: 'stroke-dashoffset .6s cubic-bezier(.2,.7,.2,1)' }} />
      </svg>
      <div style={{ position: 'absolute', inset: 0, display: 'grid', placeItems: 'center', textAlign: 'center' }}>
        {children}
      </div>
    </div>
  );
}

function Slider({ value, min, max, step, onChange, suffix, format }) {
  const pct = ((value - min) / (max - min)) * 100;
  const label = format ? format(value) : `${value}${suffix || ''}`;
  return (
    <div className="sl-wrap">
      <input
        type="range" min={min} max={max} step={step} value={value}
        onChange={(e) => onChange(parseFloat(e.target.value))}
        className="sl-input"
        style={{ background: `linear-gradient(90deg, var(--accent) ${pct}%, var(--heat-track) ${pct}%)` }}
      />
      <span className="sl-val mono">{label}</span>
    </div>
  );
}

function StatTile({ icon, label, value, sub, accent }) {
  const I = window.Icon;
  const Ico = I[icon];
  return (
    <div className="stat-tile card">
      <div className="st-head">
        <span className="st-ico" style={accent ? { color: accent, background: `color-mix(in oklab, ${accent} 13%, transparent)` } : {}}>
          <Ico size={17} />
        </span>
        <span className="st-label">{label}</span>
      </div>
      <div className="st-value mono">{value}</div>
      <div className="st-sub">{sub}</div>
    </div>
  );
}

/* GitHub-style heatmap, last `weeks` weeks ending this week */
function Heatmap({ weeks = 18 }) {
  const D = window.DATA;
  const monday = D.monday;
  const start = new Date(monday.getTime() - (weeks - 1) * 7 * 86400000);
  const cols = [];
  const monthMarks = [];
  let lastMonth = -1;
  const MN = ['Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez'];
  for (let w = 0; w < weeks; w++) {
    const first = new Date(start.getTime() + w * 7 * 86400000);
    if (first.getMonth() !== lastMonth && first.getDate() <= 7) {
      monthMarks[w] = MN[first.getMonth()];
      lastMonth = first.getMonth();
    }
    const cells = [];
    for (let r = 0; r < 7; r++) {
      const d = new Date(first.getTime() + r * 86400000);
      let lvl = -1; // future
      if (d <= D.today) {
        const sc = (D.totals[D.iso(d)] || {}).seconds || 0;
        const frac = sc / D.goalSec;
        lvl = sc <= 0 ? 0 : frac >= 1 ? 4 : frac >= 0.6 ? 3 : frac >= 0.25 ? 2 : 1;
      }
      cells.push({ lvl, date: d, sc: (D.totals[D.iso(d)] || {}).seconds || 0 });
    }
    cols.push(cells);
  }
  const heat = ['var(--heat-0)', 'color-mix(in oklab, var(--accent) 24%, var(--heat-0))', 'color-mix(in oklab, var(--accent) 48%, var(--heat-0))', 'color-mix(in oklab, var(--accent) 74%, transparent)', 'var(--accent)'];
  const dayLbl = ['Mo', '', 'Mi', '', 'Fr', '', ''];
  return (
    <div className="heatmap">
      <div className="hm-months">
        <div className="hm-daycol" />
        {cols.map((_, w) => <div key={w} className="hm-month">{monthMarks[w] || ''}</div>)}
      </div>
      <div className="hm-grid">
        <div className="hm-daycol">
          {dayLbl.map((l, i) => <div key={i} className="hm-dlabel">{l}</div>)}
        </div>
        {cols.map((cells, w) => (
          <div key={w} className="hm-col">
            {cells.map((c, r) => (
              <div key={r} className="hm-cell"
                title={c.lvl < 0 ? '' : `${D.iso(c.date)} · ${D.fmtHM(c.sc)}`}
                style={{ background: c.lvl < 0 ? 'transparent' : heat[c.lvl], opacity: c.lvl < 0 ? 0 : 1 }} />
            ))}
          </div>
        ))}
      </div>
      <div className="hm-legend">
        <span>weniger</span>
        {heat.map((h, i) => <span key={i} className="hm-cell" style={{ background: h }} />)}
        <span>mehr</span>
      </div>
    </div>
  );
}

function WeekBars() {
  const D = window.DATA;
  const max = Math.max(D.goalSec, ...D.weekBars.map((b) => b.seconds));
  return (
    <div className="weekbars">
      {D.weekBars.map((b, i) => {
        const h = b.future ? 0 : Math.max(3, (b.seconds / max) * 100);
        const hit = b.seconds >= D.goalSec;
        return (
          <div key={i} className="wb-col">
            <div className="wb-track">
              <div className="wb-goal" style={{ bottom: (D.goalSec / max * 100) + '%' }} />
              <div className="wb-fill" style={{
                height: h + '%',
                background: b.future ? 'transparent' : (hit ? 'var(--accent)' : 'color-mix(in oklab, var(--accent) 38%, var(--heat-0))'),
              }} />
            </div>
            <div className={'wb-lbl' + (b.today ? ' today' : '')}>{b.label}</div>
          </div>
        );
      })}
    </div>
  );
}

Object.assign(window, { Ring, Slider, StatTile, Heatmap, WeekBars });
