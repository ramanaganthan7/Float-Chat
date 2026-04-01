import { NavLink } from 'react-router-dom'
import './Sidebar.css'

const NAV = [
  {
    to: '/',
    label: 'Home',
    icon: (
      <svg width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="1.8">
        <path strokeLinecap="round" strokeLinejoin="round" d="M3 12l9-9 9 9M5 10v9a1 1 0 001 1h4v-5h4v5h4a1 1 0 001-1v-9" />
      </svg>
    ),
  },
  {
    to: '/overview',
    label: 'Overview',
    icon: (
      <svg width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="1.8">
        <rect x="3" y="3" width="7" height="7" rx="1.5" />
        <rect x="14" y="3" width="7" height="7" rx="1.5" />
        <rect x="3" y="14" width="7" height="7" rx="1.5" />
        <rect x="14" y="14" width="7" height="7" rx="1.5" />
      </svg>
    ),
  },
  {
    to: '/map',
    label: 'Map',
    icon: (
      <svg width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="1.8">
        <circle cx="12" cy="12" r="9.5" />
        <path strokeLinecap="round" d="M2.5 12 Q7 8.5 12 12 Q17 15.5 21.5 12" />
        <path strokeLinecap="round" d="M12 2.5v19" opacity="0.35" />
      </svg>
    ),
  },
  {
    to: '/trends',
    label: 'Trends',
    icon: (
      <svg width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="1.8">
        <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
      </svg>
    ),
  },
  {
    to: '/chatbot',
    label: 'Chatbot',
    icon: (
      <svg width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="1.8">
        <path strokeLinecap="round" strokeLinejoin="round"
          d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-3 3-3-3z" />
      </svg>
    ),
  },
]

export default function Sidebar() {
  return (
    <aside className="sidebar">
      {/* Brand */}
      <div className="sidebar__brand">
        <div className="sidebar__logo">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
            <circle cx="12" cy="12" r="9.5" stroke="#00D4FF" strokeWidth="1.4" />
            <path d="M2.5 12 Q7 8.5 12 12 Q17 15.5 21.5 12" stroke="#00D4FF" strokeWidth="1.4" strokeLinecap="round" fill="none" />
            <path d="M2.5 12 Q7 15.5 12 12 Q17 8.5 21.5 12" stroke="#00C6B8" strokeWidth="1.4" strokeLinecap="round" fill="none" />
            <circle cx="12" cy="7.5" r="1.5" fill="#00D4FF" />
          </svg>
          <span className="sidebar__brand-name">AlgoFloat</span>
        </div>
        <div className="sidebar__brand-sub">Ocean Intelligence Platform</div>
      </div>

      {/* Navigation */}
      <nav className="sidebar__nav">
        <div className="sidebar__nav-label">Navigation</div>
        {NAV.map(({ to, label, icon }) => (
          <NavLink
            key={to}
            to={to}
            end={to === '/'}
            className={({ isActive }) =>
              'sidebar__link' + (isActive ? ' sidebar__link--active' : '')
            }
          >
            <span className="sidebar__link-icon">{icon}</span>
            {label}
          </NavLink>
        ))}
      </nav>

      {/* Footer */}
      <div className="sidebar__footer">
        <div className="sidebar__footer-line">ARGO Float Array</div>
        <div className="sidebar__footer-line">Gemini 2.0 Flash</div>
        <div className="sidebar__footer-line sidebar__footer-line--dim">v0.1.0</div>
      </div>
    </aside>
  )
}
