/* Lernreich — Lernjournal view */
function JournalView() {
  const D = window.DATA;
  const I = window.Icon;
  const MN = ['Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez'];
  const [entries, setEntries] = React.useState(D.journal);
  const [draft, setDraft] = React.useState('');
  const [subject, setSubject] = React.useState('Datenstrukturen');

  const fmtDate = (s) => {
    const d = new Date(s + 'T00:00:00');
    if (D.iso(d) === D.iso(D.today)) return 'Heute';
    const y = new Date(D.today.getTime() - 86400000);
    if (D.iso(d) === D.iso(y)) return 'Gestern';
    return `${d.getDate()}. ${MN[d.getMonth()]}`;
  };

  const save = () => {
    const text = draft.trim();
    if (!text) return;
    setEntries([{ date: D.iso(D.today), subject, minutes: 0, text, tags: [] }, ...entries]);
    setDraft('');
  };

  return (
    <div>
      <div className="view-head" style={{ display: 'flex', alignItems: 'flex-end', justifyContent: 'space-between' }}>
        <div>
          <div className="eyebrow">Notizen</div>
          <h1 className="view-title">Lernjournal</h1>
          <p className="view-sub">Was hast du verstanden? Halte Durchbrüche und offene Fragen fest.</p>
        </div>
        <button className="btn btn-ghost"><I.folder /> Ordner öffnen</button>
      </div>

      <div style={{ maxWidth: 760 }}>
        <div className="card jr-compose" style={{ marginBottom: 18 }}>
          <textarea value={draft} onChange={(e) => setDraft(e.target.value)}
            placeholder="Was hast du heute gelernt? Ein Satz reicht — der Moment zählt." />
          <div className="jr-compose-foot">
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <span className="muted" style={{ fontSize: 12.5, fontWeight: 600 }}>Fach</span>
              <select className="input" style={{ width: 'auto', padding: '7px 10px', fontSize: 13 }}
                value={subject} onChange={(e) => setSubject(e.target.value)}>
                {D.subjects.map((s) => <option key={s.name}>{s.name}</option>)}
              </select>
            </div>
            <button className="btn btn-primary" style={{ padding: '10px 16px' }} onClick={save}>
              <I.pencil /> Notiz merken
            </button>
          </div>
        </div>

        <div className="jr-list">
          {entries.map((e, i) => (
            <div key={i} className="card jr-card">
              <div className="jr-top">
                <span className="jr-date">{fmtDate(e.date)}</span>
                <span className="jr-dot" />
                <span className="jr-subject">{e.subject}</span>
                {e.minutes > 0 && <span className="jr-min">{e.minutes} min</span>}
              </div>
              <div className="jr-text">{e.text}</div>
              {e.tags && e.tags.length > 0 && (
                <div className="jr-tags">
                  {e.tags.map((t, k) => (
                    <span key={k} className="tag"><I.sparkle size={12} /> {t}</span>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
window.JournalView = JournalView;
