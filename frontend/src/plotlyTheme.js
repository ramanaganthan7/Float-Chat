/**
 * Shared Plotly dark-ocean theme for AlgoFloat.
 */

export const CHART_COLORS = [
  '#00D4FF','#0094C6','#00C6B8','#4ECDC4',
  '#44A5E0','#7ECEF4','#1A6FA0','#B8E4F9',
]

/**
 * Returns a Plotly layout object with the ocean dark theme applied.
 * Spread your own overrides on top.
 */
export function oceanLayout(overrides = {}) {
  return {
    paper_bgcolor: '#0A1628',
    plot_bgcolor:  '#0D2240',
    font: { family:'Inter, sans-serif', color:'#E8F4FD', size:12 },
    colorway: CHART_COLORS,
    xaxis: {
      gridcolor:'#1A3355', linecolor:'#1A3355',
      tickfont:{ color:'#8FACC8' }, title_font:{ color:'#8FACC8' },
    },
    yaxis: {
      gridcolor:'#1A3355', linecolor:'#1A3355',
      tickfont:{ color:'#8FACC8' }, title_font:{ color:'#8FACC8' },
    },
    legend: {
      bgcolor:'rgba(10,22,40,0.88)', bordercolor:'#1A3355', borderwidth:1,
      font:{ color:'#8FACC8', size:11 },
    },
    margin: { l:44, r:16, t:44, b:44 },
    hoverlabel: {
      bgcolor:'#0D2240', bordercolor:'#0094C6',
      font:{ color:'#E8F4FD', family:'Inter, sans-serif', size:12 },
    },
    title: { font:{ color:'#E8F4FD', size:13, family:'Inter, sans-serif' } },
    ...overrides,
  }
}

/** Plotly config — hide the mode bar, enable responsive sizing. */
export const plotConfig = {
  displayModeBar: true,
  displaylogo: false,
  modeBarButtonsToRemove: ['sendDataToCloud','editInChartStudio','lasso2d'],
  responsive: true,
}
