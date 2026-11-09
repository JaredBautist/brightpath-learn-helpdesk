export function HelpHeader() {
  return (
    <header>
      <div className="masthead">
        <div className="brand">
          <span className="brand-mark" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round">
              <path d="M4 5.5h5a4 4 0 0 1 3 1.4 4 4 0 0 1 3-1.4h5v13h-5a4 4 0 0 0-3 1.4 4 4 0 0 0-3-1.4H4z" />
              <path d="M12 7v12" />
            </svg>
          </span>
          <span>BrightPath <span className="brand-secondary">Learn</span></span>
        </div>
        <span className="masthead-label">Help Center</span>
      </div>
      <div className="intro">
        <p className="eyebrow">A little guidance, whenever you need it</p>
        <h1>How can we help?</h1>
        <p className="intro-description">Ask about your lessons, coaching, or account.<br className="desktop-break" /> Get answers with supporting sources.</p>
      </div>
    </header>
  );
}
