/* Lernreich — line icon set. Stroke-based, 24px grid, currentColor. */
const _ip = { fill: 'none', stroke: 'currentColor', strokeWidth: 1.75, strokeLinecap: 'round', strokeLinejoin: 'round' };

function Svg({ children, size }) {
  return (
    <svg viewBox="0 0 24 24" width={size || 24} height={size || 24} {..._ip}>{children}</svg>
  );
}

const Icon = {
  timer: (p) => <Svg {...p}><circle cx="12" cy="13" r="8" /><path d="M12 13V9" /><path d="M9 2h6" /><path d="M19 6l1.5-1.5" /></Svg>,
  stats: (p) => <Svg {...p}><path d="M4 20V10" /><path d="M10 20V4" /><path d="M16 20v-7" /><path d="M3 20h18" /></Svg>,
  calendar: (p) => <Svg {...p}><rect x="3.5" y="5" width="17" height="16" rx="2.5" /><path d="M3.5 9.5h17" /><path d="M8 3v4M16 3v4" /></Svg>,
  journal: (p) => <Svg {...p}><path d="M5 4.5A1.5 1.5 0 0 1 6.5 3H18a1 1 0 0 1 1 1v15.5" /><path d="M19 19.5H6.5A1.5 1.5 0 0 0 5 21V4.5" /><path d="M9 8h6M9 11.5h4" /></Svg>,
  settings: (p) => <Svg {...p}><circle cx="12" cy="12" r="3" /><path d="M12 2.5v2M12 19.5v2M2.5 12h2M19.5 12h2M5 5l1.5 1.5M17.5 17.5L19 19M19 5l-1.5 1.5M6.5 17.5L5 19" /></Svg>,
  moon: (p) => <Svg {...p}><path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5Z" /></Svg>,
  sun: (p) => <Svg {...p}><circle cx="12" cy="12" r="4" /><path d="M12 2v2.5M12 19.5V22M2 12h2.5M19.5 12H22M4.6 4.6l1.8 1.8M17.6 17.6l1.8 1.8M19.4 4.6l-1.8 1.8M6.4 17.6l-1.8 1.8" /></Svg>,
  play: (p) => <Svg {...p}><path d="M8 5.5v13l11-6.5-11-6.5Z" /></Svg>,
  pause: (p) => <Svg {...p}><path d="M9 5v14M15 5v14" /></Svg>,
  resume: (p) => <Svg {...p}><path d="M4 12a8 8 0 1 0 2.3-5.6" /><path d="M4 4v3.5h3.5" /></Svg>,
  stop: (p) => <Svg {...p}><rect x="6.5" y="6.5" width="11" height="11" rx="2.5" /></Svg>,
  coffee: (p) => <Svg {...p}><path d="M5 9h11v4a4 4 0 0 1-4 4H9a4 4 0 0 1-4-4V9Z" /><path d="M16 10h2a2.5 2.5 0 0 1 0 5h-2" /><path d="M8 3.5c-.6.7-.6 1.3 0 2M11.5 3.5c-.6.7-.6 1.3 0 2" /></Svg>,
  flame: (p) => <Svg {...p}><path d="M12 3c1 3.5 4.5 4.8 4.5 9a4.5 4.5 0 0 1-9 0c0-1.4.5-2.4 1.2-3.2C9 10 10.5 10 10.5 7.5c1 .8 1.5 1.6 1.5 2.5C13.5 8.5 12.8 5.5 12 3Z" /></Svg>,
  clock: (p) => <Svg {...p}><circle cx="12" cy="12" r="8.5" /><path d="M12 7v5l3.5 2" /></Svg>,
  trophy: (p) => <Svg {...p}><path d="M7 4h10v4a5 5 0 0 1-10 0V4Z" /><path d="M7 5H4.5v1.5A3.5 3.5 0 0 0 8 10M17 5h2.5v1.5A3.5 3.5 0 0 1 16 10" /><path d="M12 13v3M9 20h6M10 16h4l.5 4h-5l.5-4Z" /></Svg>,
  target: (p) => <Svg {...p}><circle cx="12" cy="12" r="8.5" /><circle cx="12" cy="12" r="4.5" /><circle cx="12" cy="12" r="1" fill="currentColor" stroke="none" /></Svg>,
  bolt: (p) => <Svg {...p}><path d="M13 2 4.5 13.5H11l-1 8.5L19.5 10H13l0-8Z" /></Svg>,
  check: (p) => <Svg {...p}><path d="M5 12.5l4.5 4.5L19 6.5" /></Svg>,
  chevL: (p) => <Svg {...p}><path d="M14.5 5.5 8 12l6.5 6.5" /></Svg>,
  chevR: (p) => <Svg {...p}><path d="M9.5 5.5 16 12l-6.5 6.5" /></Svg>,
  plus: (p) => <Svg {...p}><path d="M12 5v14M5 12h14" /></Svg>,
  folder: (p) => <Svg {...p}><path d="M3.5 7.5A1.5 1.5 0 0 1 5 6h4l2 2.5h6A1.5 1.5 0 0 1 18.5 10v6.5A1.5 1.5 0 0 1 17 18H5a1.5 1.5 0 0 1-1.5-1.5v-9Z" /></Svg>,
  export: (p) => <Svg {...p}><path d="M12 15V4M8 7.5 12 4l4 3.5" /><path d="M5 14v4a1.5 1.5 0 0 0 1.5 1.5h11A1.5 1.5 0 0 0 19 18v-4" /></Svg>,
  refresh: (p) => <Svg {...p}><path d="M20 11a8 8 0 1 0-.5 4" /><path d="M20 4v5h-5" /></Svg>,
  book: (p) => <Svg {...p}><path d="M12 6.5C10.5 5 8 4.5 4.5 5v13c3.5-.5 6 0 7.5 1.5C13.5 18 16 17.5 19.5 18V5C16 4.5 13.5 5 12 6.5Z" /><path d="M12 6.5v13" /></Svg>,
  sparkle: (p) => <Svg {...p}><path d="M12 3c.6 3.8 1.7 4.9 5.5 5.5C13.7 9.1 12.6 10.2 12 14c-.6-3.8-1.7-4.9-5.5-5.5C10.3 7.9 11.4 6.8 12 3Z" /><path d="M18 14c.3 1.6.7 2 2.3 2.3-1.6.3-2 .7-2.3 2.3-.3-1.6-.7-2-2.3-2.3 1.6-.3 2-.7 2.3-2.3Z" /></Svg>,
  pencil: (p) => <Svg {...p}><path d="M14.5 5.5l4 4L8 20l-4.5 1L4.5 16.5 14.5 5.5Z" /><path d="M12.5 7.5l4 4" /></Svg>,
};

window.Icon = Icon;
