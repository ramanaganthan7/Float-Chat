import { useNavigate } from 'react-router-dom'

const CARDS = [
  {
    to: '/overview',
    title: 'Overview',
    desc: 'Dataset statistics, KPI metrics, and parameter distribution analysis.',
    color: '#00D4FF',
    icon: (
      <svg width="22" height="22" fill="none" viewBox="0 0 24 24" stroke="white" strokeWidth="1.7">
        <rect x="3" y="3" width="7" height="7" rx="1.5" />
        <rect x="14" y="3" width="7" height="7" rx="1.5" />
        <rect x="3" y="14" width="7" height="7" rx="1.5" />
        <rect x="14" y="14" width="7" height="7" rx="1.5" />
      </svg>
    ),
  },
  {
    to: '/map',
    title: 'Map',
    desc: 'Interactive global map of ARGO float positions with parameter overlays.',
    color: '#00C6B8',
    icon: (
      <svg width="22" height="22" fill="none" viewBox="0 0 24 24" stroke="white" strokeWidth="1.7">
        <circle cx="12" cy="12" r="9.5" />
        <path strokeLinecap="round" d="M2.5 12 Q7 8.5 12 12 Q17 15.5 21.5 12" />
        <path strokeLinecap="round" d="M12 2.5v19" opacity="0.35" />
      </svg>
    ),
  },
  {
    to: '/trends',
    title: 'Trends',
    desc: 'Time-series, depth profiles, T-S diagrams, and rolling mean analysis.',
    color: '#0094C6',
    icon: (
      <svg width="22" height="22" fill="none" viewBox="0 0 24 24" stroke="white" strokeWidth="1.7">
        <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
      </svg>
    ),
  },
  {
    to: '/chatbot',
    title: 'Chatbot',
    desc: 'Natural language queries — Gemini 2.0 Flash writes SQL in real time.',
    color: '#4ECDC4',
    icon: (
      <svg width="22" height="22" fill="none" viewBox="0 0 24 24" stroke="white" strokeWidth="1.7">
        <path strokeLinecap="round" strokeLinejoin="round"
          d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-3 3-3-3z" />
      </svg>
    ),
  },
]

const TAGS = [
  { label: 'SQLite', color: '#7ECEF4' },
  { label: 'Gemini 2.0 Flash', color: '#00C6B8' },
  { label: 'ARGO Float Array', color: '#00D4FF' },
  { label: 'FastAPI + React', color: '#4ECDC4' },
]

export default function Home() {
  const nav = useNavigate()

  return (
    <div style={{ animation: 'fadeUp 0.4s ease' }}>
      {/* ── Hero ── */}
      <div style={{
        position: 'relative', overflow: 'hidden',
        padding: '3.5rem 2.5rem 3rem',
        background: 'linear-gradient(135deg,#0A1628 0%,#0D2240 55%,#071626 100%)',
        border: '1px solid var(--border)', borderRadius: 16,
        marginBottom: '2rem',
      }}>
        {/* Glow orbs */}
        <div style={{
          position: 'absolute', top: -80, right: -80, width: 360, height: 360,
          background: 'radial-gradient(circle,rgba(0,148,198,0.13) 0%,transparent 70%)',
          borderRadius: '50%', pointerEvents: 'none',
        }} />
        <div style={{
          position: 'absolute', bottom: -100, left: '5%', width: 280, height: 280,
          background: 'radial-gradient(circle,rgba(0,198,184,0.10) 0%,transparent 70%)',
          borderRadius: '50%', pointerEvents: 'none',
        }} />
        {/* Animated accent bar */}
        <div style={{
          position: 'absolute', bottom: 0, left: 0, right: 0, height: 3,
          background: 'linear-gradient(90deg,#0094C6,#00C6B8,#00D4FF,#0094C6)',
          backgroundSize: '200% 100%',
          animation: 'gradientShift 3.5s ease infinite',
        }} />

        <div style={{ position: 'relative', zIndex: 1, maxWidth: 680 }}>
          {/* Live badge */}
          <div style={{
            display: 'inline-flex', alignItems: 'center', gap: '0.45rem',
            background: 'rgba(0,212,255,0.09)', border: '1px solid rgba(0,212,255,0.22)',
            borderRadius: 24, padding: '0.28rem 0.8rem',
            fontSize: '0.7rem', fontWeight: 700, color: '#00D4FF',
            letterSpacing: '0.08em', textTransform: 'uppercase',
            marginBottom: '1.25rem',
          }}>
            <span style={{
              width: 7, height: 7, borderRadius: '50%', background: '#00D4FF',
              animation: 'pulseGlow 1.8s ease infinite', display: 'inline-block',
            }} />
            Live Ocean Data
          </div>

          <h1 style={{
            margin: '0 0 0.8rem', fontWeight: 800, letterSpacing: '-0.03em',
            fontSize: 'clamp(1.9rem,3.5vw,2.8rem)', lineHeight: 1.15,
            background: 'linear-gradient(135deg,#E8F4FD 0%,#7ECEF4 45%,#00D4FF 100%)',
            WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent',
            backgroundClip: 'text',
          }}>
            AI-Powered ARGO<br />Ocean Data Explorer
          </h1>

          <p style={{
            margin: '0 0 2rem', color: 'var(--tx2)', fontSize: '1rem', lineHeight: 1.7,
          }}>
            Real-time oceanographic insights from the global ARGO profiling float array.
            Explore temperature, salinity, and pressure across the world's oceans — powered
            by Gemini 2.0 Flash and natural language SQL.
          </p>

          {/* Tech tags */}
          <div style={{ display: 'flex', gap: '0.6rem', flexWrap: 'wrap' }}>
            {TAGS.map(({ label, color }) => (
              <span key={label} style={{
                padding: '0.38rem 0.9rem',
                background: `${color}14`, border: `1px solid ${color}2A`,
                borderRadius: 24, fontSize: '0.77rem', fontWeight: 600, color,
              }}>
                {label}
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* ── Feature cards ── */}
      <div style={{
        display: 'grid', gridTemplateColumns: 'repeat(4,1fr)', gap: '1rem',
        marginBottom: '1.5rem',
      }}>
        {CARDS.map(({ to, title, desc, color, icon }, i) => (
          <div
            key={to}
            onClick={() => nav(to)}
            style={{
              background: 'linear-gradient(135deg,#0A1628,#0D2240)',
              border: '1px solid var(--border)', borderRadius: 12,
              padding: '1.5rem 1.25rem 1.4rem',
              position: 'relative', overflow: 'hidden',
              animation: `fadeUp 0.4s ease ${i * 0.07}s both`,
              transition: 'transform 0.22s, box-shadow 0.22s, border-color 0.22s',
              cursor: 'pointer',
            }}
            onMouseEnter={e => {
              e.currentTarget.style.transform = 'translateY(-5px)'
              e.currentTarget.style.boxShadow = '0 14px 36px rgba(0,148,198,0.22)'
              e.currentTarget.style.borderColor = `${color}55`
            }}
            onMouseLeave={e => {
              e.currentTarget.style.transform = ''
              e.currentTarget.style.boxShadow = ''
              e.currentTarget.style.borderColor = 'var(--border)'
            }}
          >
            <div style={{
              position: 'absolute', top: 0, left: 0, right: 0, height: 2,
              background: `linear-gradient(90deg,transparent,${color},transparent)`,
            }} />
            <div style={{
              width: 44, height: 44, borderRadius: 11, marginBottom: '1rem',
              background: `${color}12`, border: `1px solid ${color}28`,
              display: 'flex', alignItems: 'center', justifyContent: 'center',
            }}>
              {icon}
            </div>
            <div style={{ fontSize: '0.97rem', fontWeight: 700, color: 'var(--tx)', marginBottom: '0.45rem' }}>
              {title}
            </div>
            <div style={{ fontSize: '0.8rem', color: 'var(--tx2)', lineHeight: 1.6 }}>
              {desc}
            </div>
          </div>
        ))}
      </div>

      <hr className="divider" />
      <div style={{ textAlign: 'center', padding: '0.25rem 0' }}>
        <span style={{ fontSize: '0.73rem', color: 'var(--tx3)', letterSpacing: '0.04em' }}>
          Data: ARGO Global Float Array &nbsp;&middot;&nbsp; AI: Gemini 2.0 Flash &nbsp;&middot;&nbsp;
          Storage: SQLite &nbsp;&middot;&nbsp; Charts: Plotly
        </span>
      </div>
    </div>
  )
}
