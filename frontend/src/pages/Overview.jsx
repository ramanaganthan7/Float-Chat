import { useEffect, useState } from 'react'
import createPlotlyComponent from 'react-plotly.js/factory'
import Plotly from 'plotly.js-dist-min'
import { fetchOverview } from '../api'
import { oceanLayout, CHART_COLORS, plotConfig } from '../plotlyTheme'
import PageHeader from '../components/PageHeader'
import MetricCard from '../components/MetricCard'
import SectionHeader from '../components/SectionHeader'
import Spinner from '../components/Spinner'

const Plot = createPlotlyComponent(Plotly)

const ICON = (
  <svg width="22" height="22" fill="none" viewBox="0 0 24 24" stroke="white" strokeWidth="1.8">
    <rect x="3" y="3" width="7" height="7" rx="1.5" />
    <rect x="14" y="3" width="7" height="7" rx="1.5" />
    <rect x="3" y="14" width="7" height="7" rx="1.5" />
    <rect x="14" y="14" width="7" height="7" rx="1.5" />
  </svg>
)

export default function Overview() {
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchOverview().then(setData).catch(e => setError(e.message))
  }, [])

  if (error) return <div style={{ color: 'var(--err)', padding: '2rem' }}>Error: {error}</div>
  if (!data) return <Spinner label="Loading overview data…" />

  const corrCols = ['TEMP', 'PSAL', 'PRES']
  const corrZ = corrCols.map(r => corrCols.map(c => data.corr[r]?.[c] ?? 0))

  const platLabels = data.platform_summary.map(p => String(p.PLATFORM_NUMBER))
  const platRecords = data.platform_summary.map(p => p.records)
  const platAvgTemp = data.platform_summary.map(p => p.avg_temp)

  return (
    <div style={{ animation: 'fadeUp 0.4s ease' }}>
      <PageHeader icon={ICON} title="Dataset Overview"
        subtitle="Summary statistics, KPI metrics, and parameter distributions across the ARGO dataset." />

      {/* KPIs */}
      <SectionHeader>Key Metrics</SectionHeader>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4,1fr)', gap: '1rem' }}>
        <MetricCard label="Total Records"  value={data.total_records.toLocaleString()} delay="0s" />
        <MetricCard label="Unique Floats"  value={data.unique_floats.toLocaleString()} delay="0.08s" />
        <MetricCard label="Avg Temp (°C)"  value={data.avg_temp} delay="0.16s" />
        <MetricCard label="Avg Salinity"   value={data.avg_salinity} delay="0.24s" />
      </div>

      <hr className="divider" />

      {/* Dataset sample */}
      <SectionHeader>Dataset Snapshot (first 20 rows)</SectionHeader>
      <div style={{
        overflowX: 'auto', border: '1px solid var(--border)',
        borderRadius: 'var(--r)', boxShadow: 'var(--sh)',
      }}>
        <table style={{
          width: '100%', borderCollapse: 'collapse',
          fontFamily: "'JetBrains Mono',monospace", fontSize: '0.75rem',
        }}>
          <thead>
            <tr style={{ background: 'var(--surf2)' }}>
              {data.sample.length > 0 &&
                Object.keys(data.sample[0]).map(col => (
                  <th key={col} style={{
                    padding: '0.6rem 0.75rem', textAlign: 'left',
                    color: 'var(--tx2)', fontWeight: 700,
                    borderBottom: '1px solid var(--border)',
                    whiteSpace: 'nowrap', fontSize: '0.68rem',
                    textTransform: 'uppercase', letterSpacing: '0.06em',
                  }}>
                    {col}
                  </th>
                ))
              }
            </tr>
          </thead>
          <tbody>
            {data.sample.map((row, i) => (
              <tr key={i} style={{
                background: i % 2 === 0 ? 'var(--surface)' : 'var(--surf2)',
                transition: 'background 0.15s',
              }}
              onMouseEnter={e => e.currentTarget.style.background = 'rgba(0,148,198,0.08)'}
              onMouseLeave={e => e.currentTarget.style.background = i % 2 === 0 ? 'var(--surface)' : 'var(--surf2)'}
              >
                {Object.values(row).map((val, j) => (
                  <td key={j} style={{
                    padding: '0.5rem 0.75rem', color: 'var(--tx)',
                    borderBottom: '1px solid rgba(26,51,85,0.5)',
                    whiteSpace: 'nowrap',
                  }}>
                    {val ?? '—'}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <hr className="divider" />

      {/* Distributions */}
      <SectionHeader>Parameter Distributions</SectionHeader>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3,1fr)', gap: '1rem' }}>
        {[
          { key: 'temp_values', label: 'Temperature (°C)',  color: CHART_COLORS[0] },
          { key: 'psal_values', label: 'Salinity (PSU)',    color: CHART_COLORS[1] },
          { key: 'pres_values', label: 'Pressure (dbar)',   color: CHART_COLORS[2] },
        ].map(({ key, label, color }) => (
          <Plot
            key={key}
            data={[{
              type: 'histogram', x: data[key], nbinsx: 45,
              marker: { color, opacity: 0.85, line: { width: 0 } },
              name: label,
            }]}
            layout={oceanLayout({
              height: 300, showlegend: false,
              title: { text: label, font: { color: '#E8F4FD', size: 13 } },
              xaxis: { ...oceanLayout().xaxis, title: { text: label, font: { color: 'var(--tx2)' } } },
              yaxis: { ...oceanLayout().yaxis, title: { text: 'Count', font: { color: 'var(--tx2)' } } },
              margin: { l: 44, r: 12, t: 40, b: 44 },
            })}
            config={plotConfig}
            useResizeHandler style={{ width: '100%' }}
          />
        ))}
      </div>

      <hr className="divider" />

      {/* Correlation + scatter */}
      <SectionHeader>Correlation Analysis</SectionHeader>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
        <Plot
          data={[{
            type: 'heatmap',
            z: corrZ, x: corrCols, y: corrCols,
            colorscale: [[0,'#020B18'],[0.3,'#0A1628'],[0.6,'#0094C6'],[1,'#00D4FF']],
            text: corrZ.map(r => r.map(v => v.toFixed(3))),
            texttemplate: '%{text}',
            textfont: { size: 14, color: '#E8F4FD' },
            showscale: true, zmin: -1, zmax: 1,
            colorbar: { tickfont: { color: 'var(--tx2)' }, thickness: 14, outlinecolor: 'var(--border)' },
          }]}
          layout={oceanLayout({
            height: 320, title: { text: 'Correlation Matrix', font: { color: '#E8F4FD', size: 13 } },
            margin: { l: 44, r: 60, t: 40, b: 44 },
          })}
          config={plotConfig} useResizeHandler style={{ width: '100%' }}
        />

        {/* Per-platform bar */}
        <Plot
          data={[{
            type: 'bar',
            x: platLabels, y: platRecords,
            marker: {
              color: platAvgTemp,
              colorscale: [[0,'#0A1628'],[0.5,'#0094C6'],[1,'#00D4FF']],
              showscale: true,
              colorbar: { title: { text: 'Avg Temp', font: { color: 'var(--tx2)', size: 10 } }, tickfont: { color: 'var(--tx2)' }, thickness: 14, outlinecolor: 'var(--border)' },
            },
            name: 'Records',
          }]}
          layout={oceanLayout({
            height: 320,
            title: { text: 'Records per Float (coloured by Avg Temp)', font: { color: '#E8F4FD', size: 13 } },
            xaxis: { ...oceanLayout().xaxis, title: { text: 'Platform', font: { color: 'var(--tx2)' } } },
            yaxis: { ...oceanLayout().yaxis, title: { text: 'Record Count', font: { color: 'var(--tx2)' } } },
            margin: { l: 44, r: 60, t: 40, b: 44 },
          })}
          config={plotConfig} useResizeHandler style={{ width: '100%' }}
        />
      </div>

      <p style={{ fontSize: '0.78rem', color: 'var(--tx3)', marginTop: '1.5rem' }}>
        Dataset: {data.total_records.toLocaleString()} records · {data.unique_floats} floats · Source: ARGO Global Float Array
      </p>
    </div>
  )
}
