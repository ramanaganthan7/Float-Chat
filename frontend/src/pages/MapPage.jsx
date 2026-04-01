import { useEffect, useState, useMemo } from 'react'
import createPlotlyComponent from 'react-plotly.js/factory'
import Plotly from 'plotly.js-dist-min'
import { fetchMap } from '../api'
import { oceanLayout, CHART_COLORS, plotConfig } from '../plotlyTheme'
import PageHeader from '../components/PageHeader'
import SectionHeader from '../components/SectionHeader'
import MetricCard from '../components/MetricCard'
import Spinner from '../components/Spinner'
import OceanMap from '../components/OceanMap'

const Plot = createPlotlyComponent(Plotly)

const ICON = (
  <svg width="22" height="22" fill="none" viewBox="0 0 24 24" stroke="white" strokeWidth="1.8">
    <circle cx="12" cy="12" r="9.5" />
    <path strokeLinecap="round" d="M2.5 12 Q7 8.5 12 12 Q17 15.5 21.5 12" />
    <path strokeLinecap="round" d="M12 2.5v19" opacity="0.35" />
  </svg>
)

const PARAM_LABELS = {
  TEMP: 'Temperature (°C)',
  PSAL: 'Salinity (PSU)',
  PRES: 'Pressure (dbar)',
}

export default function MapPage() {
  const [rawData, setRawData]     = useState(null)
  const [error, setError]         = useState(null)
  const [colorBy, setColorBy]     = useState('TEMP')
  const [selPlatforms, setSelPlatforms] = useState(null)

  useEffect(() => {
    fetchMap().then(d => { setRawData(d); setSelPlatforms(null) }).catch(e => setError(e.message))
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
  if (!rawData) return <Spinner label="Loading map data…" />

  const colorValues = filtered.map(d => d[colorBy])
  const avg = arr => arr.length ? arr.reduce((s, v) => s + (v ?? 0), 0) / arr.length : 0

  return (
    <div style={{ animation: 'fadeUp 0.4s ease' }}>
      <PageHeader icon={ICON} title="Float Locations Map"
        subtitle="Real-time global map of ARGO profiling float positions. Click any marker for full observation details." />

      {/* Controls bar */}
      <div style={{
        display: 'flex', gap: '1rem', alignItems: 'flex-end',
        flexWrap: 'wrap', marginBottom: '1rem',
        padding: '0.85rem 1rem',
        background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 'var(--r)',
      }}>
        <div>
          <div style={{ fontSize: '0.68rem', fontWeight: 700, color: 'var(--tx2)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '0.35rem' }}>
            Colour by
          </div>
          <div style={{ display: 'flex', gap: '0.4rem' }}>
            {Object.entries(PARAM_LABELS).map(([v, l]) => (
              <button key={v} onClick={() => setColorBy(v)}
                style={{
                  padding: '0.35rem 0.75rem', borderRadius: 20,
                  background: colorBy === v ? 'linear-gradient(135deg,var(--a1),var(--a2))' : 'var(--surf2)',
                  border: `1px solid ${colorBy === v ? 'transparent' : 'var(--border)'}`,
                  color: colorBy === v ? '#fff' : 'var(--tx2)',
                  fontSize: '0.8rem', fontWeight: 600, cursor: 'pointer',
                  transition: 'all 0.15s',
                }}>
                {v}
              </button>
            ))}
          </div>
        </div>

        <div>
          <div style={{ fontSize: '0.68rem', fontWeight: 700, color: 'var(--tx2)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '0.35rem' }}>
            Filter Platforms
          </div>
          <select
            multiple size={1}
            value={selPlatforms?.map(String) ?? ['']}
            onChange={e => {
              const vals = [...e.target.selectedOptions].map(o => Number(o.value)).filter(Boolean)
              setSelPlatforms(vals.length ? vals : null)
            }}
            style={{
              background: '#0D2240', border: '1px solid var(--border)',
              borderRadius: 'var(--rs)', color: '#E8F4FD', padding: '0.38rem 0.7rem',
              fontSize: '0.82rem', outline: 'none', minWidth: 160, cursor: 'pointer',
            }}
          >
            <option value="" style={{ background:'#0D2240', color:'#E8F4FD' }}>All platforms ({allPlatforms.length})</option>
            {allPlatforms.map(p => <option key={p} value={p} style={{ background:'#0D2240', color:'#E8F4FD' }}>{p}</option>)}
          </select>
        </div>

        <div style={{ marginLeft: 'auto', display: 'flex', gap: '0.4rem', alignItems: 'center' }}>
          <div style={{
            width: 8, height: 8, borderRadius: '50%', background: 'var(--ok)',
            animation: 'pulseGlow 2s ease infinite',
          }} />
          <span style={{ fontSize: '0.78rem', color: 'var(--tx2)' }}>
            {filtered.length.toLocaleString()} observations · {new Set(filtered.map(d => d.PLATFORM_NUMBER)).size} floats
          </span>
        </div>
      </div>

      {/* KPI strip */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4,1fr)', gap: '0.75rem', marginBottom: '1rem' }}>
        <MetricCard label="Visible Records" value={filtered.length} delay="0s" />
        <MetricCard label="Active Floats"   value={new Set(filtered.map(d => d.PLATFORM_NUMBER)).size} delay="0.06s" />
        <MetricCard label={`Avg ${colorBy}`} value={avg(colorValues).toFixed(2)} delay="0.12s" />
        <MetricCard
          label={`${colorBy} Range`}
          value={`${Math.min(...colorValues).toFixed(1)}–${Math.max(...colorValues).toFixed(1)}`}
          delay="0.18s"
        />
      </div>

      {/* ── REAL MAP ── */}
      <OceanMap data={filtered} colorBy={colorBy} height={560} />

      <hr className="divider" />

      {/* Geographic distributions */}
      <SectionHeader>Geographic Distribution</SectionHeader>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
        <div style={{ height: 280 }}>
          <Plot
            data={[{
              type: 'histogram',
              x: filtered.map(d => d.LATITUDE),
              nbinsx: 40,
              marker: { color: CHART_COLORS[0], opacity: 0.85, line: { width: 0 } },
              hovertemplate: 'Lat: %{x:.1f}°<br>Count: %{y}<extra></extra>',
            }]}
            layout={oceanLayout({
              height: 280, showlegend: false,
              title: { text: 'Latitude Distribution', font: { color: '#E8F4FD', size: 13 } },
              xaxis: { ...oceanLayout().xaxis, title: { text: 'Latitude (°)', font: { color: 'var(--tx2)' } } },
              yaxis: { ...oceanLayout().yaxis, title: { text: 'Count', font: { color: 'var(--tx2)' } } },
              margin: { l: 44, r: 12, t: 40, b: 44 },
            })}
            config={plotConfig} useResizeHandler style={{ width: '100%', height: '100%' }}
          />
        </div>
        <div style={{ height: 280 }}>
          <Plot
            data={[{
              type: 'histogram',
              x: filtered.map(d => d.LONGITUDE),
              nbinsx: 40,
              marker: { color: CHART_COLORS[2], opacity: 0.85, line: { width: 0 } },
              hovertemplate: 'Lon: %{x:.1f}°<br>Count: %{y}<extra></extra>',
            }]}
            layout={oceanLayout({
              height: 280, showlegend: false,
              title: { text: 'Longitude Distribution', font: { color: '#E8F4FD', size: 13 } },
              xaxis: { ...oceanLayout().xaxis, title: { text: 'Longitude (°)', font: { color: 'var(--tx2)' } } },
              yaxis: { ...oceanLayout().yaxis, title: { text: 'Count', font: { color: 'var(--tx2)' } } },
              margin: { l: 44, r: 12, t: 40, b: 44 },
            })}
            config={plotConfig} useResizeHandler style={{ width: '100%', height: '100%' }}
          />
        </div>
      </div>

      {/* Scatter: lat vs lon coloured by parameter */}
      <SectionHeader>Float Track Overview</SectionHeader>
      <div style={{ height: 400 }}>
        <Plot
          data={[{
            type: 'scatter',
            mode: 'markers',
            x: filtered.map(d => d.LONGITUDE),
            y: filtered.map(d => d.LATITUDE),
            marker: {
              color: colorValues,
              colorscale: [[0,'#020B18'],[0.25,'#00519E'],[0.5,'#0094C6'],[0.75,'#00C6B8'],[1,'#00D4FF']],
              showscale: true,
              size: 5,
              opacity: 0.75,
              colorbar: {
                title: { text: PARAM_LABELS[colorBy], font: { color: '#8FACC8', size: 11 } },
                tickfont: { color: '#8FACC8', size: 10 },
                outlinecolor: '#1A3355',
                thickness: 14,
              },
            },
            hovertemplate: `Float: %{customdata}<br>Lon: %{x:.3f}°<br>Lat: %{y:.3f}°<br>${colorBy}: %{marker.color:.2f}<extra></extra>`,
            customdata: filtered.map(d => d.PLATFORM_NUMBER),
          }]}
          layout={oceanLayout({
            height: 400,
            title: { text: `Float Tracks — coloured by ${PARAM_LABELS[colorBy]}`, font: { color: '#E8F4FD', size: 13 } },
            xaxis: { ...oceanLayout().xaxis, title: { text: 'Longitude (°)', font: { color: 'var(--tx2)' } } },
            yaxis: { ...oceanLayout().yaxis, title: { text: 'Latitude (°)', font: { color: 'var(--tx2)' } } },
            margin: { l: 44, r: 60, t: 44, b: 44 },
          })}
          config={plotConfig} useResizeHandler style={{ width: '100%', height: '100%' }}
        />
      </div>

      <p style={{ fontSize: '0.78rem', color: 'var(--tx3)', marginTop: '1rem' }}>
        {filtered.length.toLocaleString()} observations from {new Set(filtered.map(d => d.PLATFORM_NUMBER)).size} float(s) · CartoDB Dark Matter tiles · OpenStreetMap contributors
      </p>
    </div>
  )
}
