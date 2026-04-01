export default function SectionHeader({ children }) {
  return (
    <div style={{
      display: 'flex', alignItems: 'center', gap: '0.5rem',
      margin: '1.75rem 0 0.85rem',
      paddingBottom: '0.55rem',
      borderBottom: '1px solid var(--border)',
      animation: 'fadeIn 0.3s ease',
    }}>
      <span style={{
        fontSize: '0.72rem', fontWeight: 700, color: 'var(--tx2)',
        textTransform: 'uppercase', letterSpacing: '0.12em',
      }}>
        {children}
      </span>
    </div>
  )
}
