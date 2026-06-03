/* Lernreich — App shell */
const ACCENTS = {
  indigo: '#4659e6',
  gold:   '#c2902f',
  sage:   '#1f8a5b',
  clay:   '#c1623a',
  violet: '#7257d6',
};

const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{
  "accent": "#4659e6",
  "dark": false,
  "radius": "weich"
}/*EDITMODE-END*/;

function inkFor(hex) {
  const h = hex.replace('#', '');
  const r = parseInt(h.slice(0, 2), 16) / 255, g = parseInt(h.slice(2, 4), 16) / 255, b = parseInt(h.slice(4, 6), 16) / 255;
  const lin = (c) => (c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4));
  const L = 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b);
  return L > 0.55 ? '#1b1606' : '#ffffff';
}

const RADII = {
  kantig: { sm: '5px', md: '7px', lg: '9px', xl: '12px' },
  weich:  { sm: '9px', md: '13px', lg: '18px', xl: '24px' },
  rund:   { sm: '13px', md: '18px', lg: '24px', xl: '30px' },
};

function App() {
  const [t, setTweak] = window.useTweaks(TWEAK_DEFAULTS);
  const [view, setView] = React.useState('timer');

  // Synchronize theme with the parent page
  React.useEffect(() => {
    const handleMsg = (e) => {
      if (e.data && e.data.type === 'setTheme') {
        setTweak('dark', e.data.theme === 'dark');
      }
    };
    window.addEventListener('message', handleMsg);

    try {
      const parentTheme = window.parent.document.documentElement.getAttribute('data-theme');
      if (parentTheme) {
        setTweak('dark', parentTheme === 'dark');
      }
    } catch (err) {
      const storedTheme = localStorage.getItem("theme");
      if (storedTheme) {
        setTweak('dark', storedTheme === 'dark');
      }
    }

    return () => window.removeEventListener('message', handleMsg);
  }, [setTweak]);
  const [tm, setTm] = React.useState({
    phase: 'setup',
    subject: 'Analysis II',
    goal: 'Kapitel 4: Mehrfachintegrale',
    durationMin: 60, popupMin: 15, dailyGoalH: 2.0,
    checklist: [true, true, false, false],
    running: false, elapsed: 0, onBreak: false, breakElapsed: 0,
  });

  // live timer
  React.useEffect(() => {
    if (tm.phase !== 'active') return;
    const id = setInterval(() => {
      setTm((p) => {
        if (p.onBreak) {
          const be = Math.min(5 * 60, p.breakElapsed + 1);
          return { ...p, breakElapsed: be };
        }
        if (!p.running) return p;
        const target = p.durationMin * 60;
        const el = Math.min(target, p.elapsed + 1);
        return { ...p, elapsed: el, running: el < target ? p.running : false };
      });
    }, 1000);
    return () => clearInterval(id);
  }, [tm.phase, tm.running, tm.onBreak, tm.durationMin]);

  const api = {
    set: (k, v) => setTm((p) => ({ ...p, [k]: v })),
    toggleCheck: (i) => setTm((p) => { const c = [...p.checklist]; c[i] = !c[i]; return { ...p, checklist: c }; }),
    start: () => setTm((p) => ({ ...p, phase: 'active', running: true, onBreak: false, elapsed: p.elapsed || 0 })),
    toggleRun: () => setTm((p) => ({ ...p, running: !p.running, onBreak: false })),
    toggleBreak: () => setTm((p) => ({ ...p, onBreak: !p.onBreak, running: false, breakElapsed: p.onBreak ? p.breakElapsed : 0 })),
    finish: () => setTm((p) => ({ ...p, phase: 'setup', running: false, onBreak: false, elapsed: 0, breakElapsed: 0 })),
  };

  const accent = t.accent || ACCENTS.indigo;
  const r = RADII[t.radius] || RADII.weich;
  const rootStyle = {
    '--accent': accent,
    '--accent-ink': inkFor(accent),
    '--r-sm': r.sm, '--r-md': r.md, '--r-lg': r.lg, '--r-xl': r.xl,
  };

  const Views = window;
  return (
    <div className="app-root" data-theme={t.dark ? 'dark' : 'light'} style={rootStyle}>
      <Views.Sidebar view={view} setView={setView}
        theme={t.dark ? 'dark' : 'light'}
        toggleTheme={() => setTweak('dark', !t.dark)}
        onSettings={() => window.postMessage({ type: '__activate_edit_mode' }, '*')} />

      <div className="content">
        <div className="view" key={view}>
          {view === 'timer' && <Views.TimerView tm={tm} api={api} />}
          {view === 'stats' && <Views.StatsView />}
          {view === 'calendar' && <Views.CalendarView />}
          {view === 'journal' && <Views.JournalView />}
        </div>
      </div>

      <window.TweaksPanel title="Tweaks">
        <window.TweakSection label="Marke" />
        <window.TweakColor label="Akzentfarbe" value={t.accent}
          options={Object.values(ACCENTS)}
          onChange={(v) => setTweak('accent', v)} />
        <window.TweakSection label="Darstellung" />
        <window.TweakToggle label="Dunkelmodus" value={t.dark}
          onChange={(v) => setTweak('dark', v)} />
        <window.TweakRadio label="Ecken" value={t.radius}
          options={['kantig', 'weich', 'rund']}
          onChange={(v) => setTweak('radius', v)} />
      </window.TweaksPanel>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
