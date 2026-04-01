import { useEffect, useState, useMemo } from 'react'
import createPlotlyComponent from 'react-plotly.js/factory'
import Plotly from 'plotly.js-dist-min'
import { fetchTrends } from '../api'
import { oceanLayout, CHART_COLORS, plotConfig } from '../plotlyTheme'
import PageHeader from '../components/PageHeader'
import SectionHeader from '../components/SectionHeader'
import MetricCard from '../components/MetricCard'
import Spinner from '../components/Spinner'

const Plot = createPlotlyComponent(Plotly)

const ICON = (
  <svg width="22" height="22" fill="none" viewBox="0 0 24 24" stroke="white" strokeWidth="1.8">
    <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
  </svg>
)

const PARAMS = [
  { key: 'TEMP', label: 'Temperature (°C)', color: CHART_COLORS[0] },
  { key: 'PSAL', label: 'Salinity (PSU)',   color: CHART_COLORS[1] },
  { key: 'PRES', label: 'Pressure (dbar)',  color: CHART_COLORS[2] },
]

export default function Trends() {
  const [rawData, setRawData]   = useState(null)
  const [error, setError]       = useState(null)
  const [param, setParam]       = useState('TEMP')
  const [showMarkers, setShowMarkers] = useState(false)
  const [selPlatforms, setSelPlatforms] = useState(null)

  useEffect(() => {
    fetchTrends().then(d => { setRawData(d) }).catch(e => setError(e.message))
  }, [])

  const allPlatforms = useMemo(
    () => rawData ? [...new Set(rawData.map(d => d.PLATFORM_NUMBER))].sort() : [],
    [rawData]
  )

  const filtered = useMemo(() => {
    if (!rawData) return []
    if (!selPlatforms || selPlatforms.length === 0) return rawData
    const s = new Set(selPlatforms)
    return rawData.filter(d => s.has(d.PLATFORM_NUMBER))
  }, [rawData, selPlatforms])

  if (error)    return <div style={{ color: 'var(--err)', padding: '2rem' }}>Error: {error}</div>
  if (!rawData) return <Spinner label="Loading trends data…" />

  const pInfo  = PARAMS.find(p => p.key === param)
  const pLabel = pInfo.label
  const values = filtered.map(d => d[param]).filter(v => v != null)
  const mean   = values.reduce((s,v)=>s+v,0) / values.length
  const std    = Math.sqrt(values.reduce((s,v)=>s+(v-mean)**2,0)/values.length)

  const activePlatforms = selPlatforms?.length ? selPlatforms : allPlatforms

  // ── Time series — one trace per platform ──────────────────────────────────
  const tsTraces = activePlatforms.map((p, i) => {
    const rows = filtered.filter(d => d.PLATFORM_NUMBER === p)
    return {
      type: 'scatter',
      mode: showMarkers ? 'lines+markers' : 'lines',
      name: String(p),
      x: rows.map(d => d.TIME),
      y: rows.map(d => d[param]),
      line: { color: CHART_COLORS[i % CHART_COLORS.length], width: 2 },
      marker: { size: 5 },
      hovertemplate: `Float ${p}<br>Time: %{x}<br>${param}: %{y:.2f}<extra></extra>`,
    }
  })

  // ── Depth profile ─────────────────────────────────────────────────────────
  const sample = filtered.slice(0, 3000)
  const depthTraces = activePlatforms.map((p, i) => {
    const rows = sample.filter(d => d.PLATFORM_NUMBER === p)
    return {
      type: 'scatter', mode: 'markers', name: String(p),
      x: rows.map(d => d[param]), y: rows.map(d => d.PRES),
      marker: { color: CHART_COLORS[i % CHART_COLORS.length], size: 5, opacity: 0.65 },
      hovertemplate: `${param}: %{x:.2f}<br>Depth: %{y:.1f} dbar<extra>Float ${p}</extra>`,
    }
  })

  // ── Box plots ─────────────────────────────────────────────────────────────
  const boxTraces = activePlatforms.map((p, i) => ({
    type: 'box', name: String(p), boxmean: true,
    y: filtered.filter(d => d.PLATFORM_NUMBER === p).map(d => d[param]),
    marker: { color: CHART_COLORS[i % CHART_COLORS.length] },
  }))

  // ── T-S diagram ───────────────────────────────────────────────────────────
  const ts4k = filtered.slice(0, 4000)

  // ── Rolling mean ──────────────────────────────────────────────────────────
  const byTime = {}
  filtered.forEach(d => { if (!byTime[d.TIME]) byTime[d.TIME]=[]; byTime[d.TIME].push(d[param]) })
  const rollKeys = Object.keys(byTime).sort()
  const rawMean  = rollKeys.map(t => { const v=byTime[t]; return v.reduce((s,x)=>s+x,0)/v.length })
  const W        = Math.max(3, Math.floor(rollKeys.length/10))
  const rolling  = rawMean.map((_, i) => {
    const sl = rawMean.slice(Math.max(0,i-W+1), i+1)
    return sl.reduce((s,v)=>s+v,0)/sl.length
  })

  const BASE_LAYOUT = { ...oceanLayout().xaxis }

  return (
    <div style={{ animation: 'fadeUp 0.4s ease' }}>
      <PageHeader icon={ICON} title="Parameter Trends"
        subtitle="Time-series, depth profiles, T-S diagrams, and rolling mean analysis across all ARGO floats." />

      {/* Controls */}
      <div style={{
        display: 'flex', gap: '1rem', alignItems: 'flex-end', flexWrap: 'wrap',
        marginBottom: '1rem',
        padding: '0.85rem 1rem',
        background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 'var(--r)',
      }}>
        {/* Parameter pills */}
        <div>
          <div style={{ fontSize: '0.68rem', fontWeight: 700, color: 'var(--tx2)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '0.35rem' }}>Parameter</div>
          <div style={{ display: 'flex', gap: '0.4rem' }}>
            {PARAMS.map(({ key, label }) => (
              <button key={key} onClick={() => setParam(key)}
                style={{
                  padding: '0.35rem 0.75rem', borderRadius: 20,
                  background: param === key ? 'linear-gradient(135deg,var(--a1),var(--a2))' : 'var(--surf2)',
                  border: `1px solid ${param === key ? 'transparent' : 'var(--border)'}`,
                  color: param === key ? '#fff' : 'var(--tx2)',
                  fontSize: '0.8rem', fontWeight: 600, cursor: 'pointer', transition: 'all 0.15s',
                }}>
                {key}
              </button>
            ))}
          </div>
        </div>

        {/* Platform select */}
        <div>
          <div style={{ fontSize: '0.68rem', fontWeight: 700, color: 'var(--tx2)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '0.35rem' }}>Platforms</div>
          <select
            value={selPlatforms?.length ? selPlatforms[0] : ''}
            onChange={e => {
              const v = Number(e.target.value)
              setSelPlatforms(v ? [v] : null)
            }}
            style={{
              background: '#0D2240', border: '1px solid var(--border)', borderRadius: 'var(--rs)',
              color: '#E8F4FD', padding: '0.38rem 0.7rem', fontSize: '0.82rem',
              outline: 'none', minWidth: 160, cursor: 'pointer',
            }}
          >
            <option value="" style={{ background:'#0D2240', color:'#E8F4FD' }}>All ({allPlatforms.length})</option>
            {allPlatforms.map(p => <option key={p} value={p} style={{ background:'#0D2240', color:'#E8F4FD' }}>{p}</option>)}
          </select>
        </div>

        {/* Markers toggle */}
        <label style={{ display: 'flex', alignItems: 'center', gap: '0.45rem', fontSize: '0.85rem', color: 'var(--tx2)', cursor: 'pointer' }}>
          <input type="checkbox" checked={showMarkers} onChange={e => setShowMarkers(e.target.checked)}
            style={{ accentColor: 'var(--a3)', width: 14, height: 14 }} />
          Show markers
        </label>
      </div>

      {/* Stats */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4,1fr)', gap: '0.75rem', marginBottom: '1.25rem' }}>
        <MetricCard label={`Min ${param}`}  value={Math.min(...values).toFixed(2)} delay="0s" />
        <MetricCard label={`Max ${param}`}  value={Math.max(...values).toFixed(2)} delay="0.07s" />
        <MetricCard label={`Mean ${param}`} value={mean.toFixed(2)} delay="0.14s" />
        <MetricCard label="Std Dev"         value={std.toFixed(3)} delay="0.21s" />
      </div>

      {/* ── Time Series (full width) ── */}
      <SectionHeader>Time Series</SectionHeader>
      <Plot data={tsTraces}
        layout={oceanLayout({
          height: 420,
          title: { text: `${pLabel} over Time`, font: { color: '#E8F4FD', size: 13 } },
          xaxis: { ...BASE_LAYOUT, title: { text: 'Date / Time', font: { color: 'var(--tx2)' } } },
          yaxis: { ...oceanLayout().yaxis, title: { text: pLabel, font: { color: 'var(--tx2)' } } },
        })}
        config={plotConfig} useResizeHandler style={{ width: '100%' }}
      />

      <hr className="divider" />

      {/* ── Depth + Box (2 col) ── */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.25rem' }}>
        <div>
          <SectionHeader>Depth Profile</SectionHeader>
          <Plot data={depthTraces}
            layout={oceanLayout({
              height: 400,
              title: { text: `${pLabel} vs Depth`, font: { color: '#E8F4FD', size: 13 } },
              xaxis: { ...BASE_LAYOUT, title: { text: pLabel, font: { color: 'var(--tx2)' } } },
              yaxis: { ...oceanLayout().yaxis, autorange: 'reversed', title: { text: 'Pressure / Depth (dbar)', font: { color: 'var(--tx2)' } } },
            })}
            config={plotConfig} useResizeHandler style={{ width: '100%' }}
          />
        </div>
        <div>
          <SectionHeader>Distribution by Float</SectionHeader>
          <Plot data={boxTraces}
            layout={oceanLayout({
              height: 400, showlegend: false,
              title: { text: `${pLabel} per Float`, font: { color: '#E8F4FD', size: 13 } },
              xaxis: { ...BASE_LAYOUT, title: { text: 'Platform', font: { color: 'var(--tx2)' } } },
              yaxis: { ...oceanLayout().yaxis, title: { text: pLabel, font: { color: 'var(--tx2)' } } },
            })}
            config={plotConfig} useResizeHandler style={{ width: '100%' }}
          />
        </div>
      </div>

      <hr className="divider" />

      {/* ── T-S Diagram (full width) ── */}
      <SectionHeader>T-S Diagram</SectionHeader>
      <Plot
        data={[{
          type: 'scatter', mode: 'markers',
          x: ts4k.map(d => d.PSAL),
          y: ts4k.map(d => d.TEMP),
          marker: {
            color: ts4k.map(d => d.PRES),
            colorscale: [[0,'#020B18'],[0.4,'#0094C6'],[0.75,'#00C6B8'],[1,'#00D4FF']],
            showscale: true, size: 4, opacity: 0.72,
            colorbar: {
              title: { text: 'Pressure (dbar)', font: { color: '#8FACC8', size: 10 } },
              tickfont: { color: '#8FACC8' }, thickness: 14, outlinecolor: '#1A3355',
            },
          },
          hovertemplate: 'Sal: %{x:.3f}<br>Temp: %{y:.2f} °C<extra></extra>',
        }]}
        layout={oceanLayout({
          height: 400,
          title: { text: 'T-S Diagram — Temperature vs Salinity (coloured by Pressure)', font: { color: '#E8F4FD', size: 13 } },
          xaxis: { ...BASE_LAYOUT, title: { text: 'Salinity (PSU)', font: { color: 'var(--tx2)' } } },
          yaxis: { ...oceanLayout().yaxis, title: { text: 'Temperature (°C)', font: { color: 'var(--tx2)' } } },
          margin: { l: 44, r: 60, t: 44, b: 44 },
        })}
        config={plotConfig} useResizeHandler style={{ width: '100%' }}
      />

      <hr className="divider" />

      {/* ── Rolling Mean (full width) ── */}
      <SectionHeader>Rolling Mean Analysis</SectionHeader>
      <Plot
        data={[
          { type: 'scatter', mode: 'lines', name: 'Raw mean', x: rollKeys, y: rawMean, line: { color: '#1E3A5F', width: 1.5 }, opacity: 0.7 },
          { type: 'scatter', mode: 'lines', name: 'Rolling mean', x: rollKeys, y: rolling, line: { color: 'var(--a3)', width: 2.5 } },
        ]}
        layout={oceanLayout({
          height: 320,
          title: { text: `Daily Mean ${pLabel} with Rolling Smooth`, font: { color: '#E8F4FD', size: 13 } },
          xaxis: { ...BASE_LAYOUT, title: { text: 'Date / Time', font: { color: 'var(--tx2)' } } },
          yaxis: { ...oceanLayout().yaxis, title: { text: `Mean ${pLabel}`, font: { color: 'var(--tx2)' } } },
        })}
        config={plotConfig} useResizeHandler style={{ width: '100%' }}
      />

      <p style={{ fontSize: '0.78rem', color: 'var(--tx3)', marginTop: '1rem' }}>
        {filtered.length.toLocaleString()} records · {activePlatforms.length} float(s) ·
        Date range: {filtered[0]?.TIME?.slice(0,10)} to {filtered[filtered.length-1]?.TIME?.slice(0,10)}
      </p>
    </div>
  )
}
