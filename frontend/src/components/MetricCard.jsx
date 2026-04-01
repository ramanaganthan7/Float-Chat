import { useEffect, useState, useRef } from 'react'

function useCountUp(target, duration = 900) {
  const [display, setDisplay] = useState(null)
  const rafRef = useRef(null)

  useEffect(() => {
    const numeric = parseFloat(String(target).replace(/,/g, ''))
    if (isNaN(numeric)) { setDisplay(target); return }

    const start = performance.now()
    function tick(now) {
      const elapsed  = now - start
      const progress = Math.min(1, elapsed / duration)
      const eased    = 1 - Math.pow(1 - progress, 3) // ease-out cubic
      const current  = numeric * eased
      // format like the original: if it was an int show int, else keep decimals
      const isInt    = Number.isInteger(numeric)
      setDisplay(isInt
        ? Math.round(current).toLocaleString()
        : current.toFixed(String(target).includes('.') ? String(target).split('.')[1].length : 2)
      )
      if (progress < 1) rafRef.current = requestAnimationFrame(tick)
    }
    rafRef.current = requestAnimationFrame(tick)
    return () => cancelAnimationFrame(rafRef.current)
  }, [target, duration])

  return display ?? target
}

export default function MetricCard({ label, value, sub, delay = '0s', color = 'var(--a3)' }) {
  const displayed = useCountUp(value)

  return (
    <div
      style={{
        background: 'linear-gradient(135deg,var(--surface),var(--surf2))',
        border: '1px solid var(--border)',
        borderRadius: 'var(--r)',
        padding: '1.25rem 1.25rem 1rem',
        position: 'relative',
        overflow: 'hidden',
        boxShadow: 'var(--sh)',
        transition: 'transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s',
        animation: `fadeUp 0.4s ease ${delay} both`,
        cursor: 'default',
      }}
      onMouseEnter={e => {
        e.currentTarget.style.transform = 'translateY(-4px)'
        e.currentTarget.style.boxShadow = 'var(--sh2)'
        e.currentTarget.style.borderColor = 'rgba(0,148,198,0.4)'
      }}
      onMouseLeave={e => {
        e.currentTarget.style.transform = ''
        e.currentTarget.style.boxShadow = 'var(--sh)'
        e.currentTarget.style.borderColor = 'var(--border)'
      }}
    >
      {/* top gradient bar */}
      <div style={{
        position: 'absolute', top: 0, left: 0, right: 0, height: 2,
        background: 'linear-gradient(90deg,var(--a1),var(--a2),var(--a3))',
      }} />
      {/* ambient glow */}
      <div style={{
        position: 'absolute', top: -20, right: -20, width: 80, height: 80,
        background: `radial-gradient(circle, ${color}18 0%, transparent 70%)`,
        borderRadius: '50%', pointerEvents: 'none',
      }} />

      <div style={{
        fontSize: '0.7rem', fontWeight: 700, color: 'var(--tx2)',
        textTransform: 'uppercase', letterSpacing: '0.1em', marginBottom: '0.6rem',
      }}>
        {label}
      </div>
      <div style={{
        fontSize: '2rem', fontWeight: 800, color, lineHeight: 1,
        fontVariantNumeric: 'tabular-nums',
        letterSpacing: '-0.02em',
      }}>
        {displayed}
      </div>
      {sub && (
        <div style={{ fontSize: '0.75rem', color: 'var(--ok)', marginTop: '0.4rem', fontWeight: 500 }}>
          {sub}
        </div>
      )}
    </div>
  )
}
