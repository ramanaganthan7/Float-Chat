export default function Spinner({ label = 'Loading…' }) {
  return (
    <div style={{
      display: 'flex', flexDirection: 'column', alignItems: 'center',
      justifyContent: 'center', gap: '1rem', padding: '3rem',
      animation: 'fadeIn 0.3s ease',
    }}>
      <div style={{
        width: 36, height: 36,
        border: '3px solid var(--border)',
        borderTopColor: 'var(--a3)',
        borderRadius: '50%',
        animation: 'spin 0.7s linear infinite',
      }} />
      <span style={{ color: 'var(--tx2)', fontSize: '0.875rem' }}>{label}</span>
    </div>
  )
}
