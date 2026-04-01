export default function PageHeader({ icon, title, subtitle }) {
  return (
    <div style={{
      display: 'flex', alignItems: 'center', gap: '1rem',
      padding: '1.25rem 0 1rem',
      borderBottom: '1px solid var(--border)',
      marginBottom: '1.5rem',
      animation: 'fadeUp 0.35s ease',
    }}>
      <div style={{
        width: 46, height: 46, flexShrink: 0,
        background: 'linear-gradient(135deg,#0094C6,#00C6B8)',
        borderRadius: 11,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        boxShadow: '0 4px 16px rgba(0,148,198,0.35)',
      }}>
        {icon}
      </div>
      <div>
        <h1 style={{
          margin: 0, fontSize: '1.6rem', fontWeight: 800,
          background: 'linear-gradient(135deg,#E8F4FD 0%,#7ECEF4 50%,#00D4FF 100%)',
          WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent',
          backgroundClip: 'text', letterSpacing: '-0.025em',
        }}>
          {title}
        </h1>
        {subtitle && (
          <p style={{ margin: '0.3rem 0 0', color: 'var(--tx2)', fontSize: '0.88rem' }}>
            {subtitle}
          </p>
        )}
      </div>
    </div>
  )
}
