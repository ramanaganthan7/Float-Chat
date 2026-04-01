import { useState, useRef, useEffect } from 'react'
import createPlotlyComponent from 'react-plotly.js/factory'
import Plotly from 'plotly.js-dist-min'
import { postChat } from '../api'
import { oceanLayout, CHART_COLORS, plotConfig } from '../plotlyTheme'
import PageHeader from '../components/PageHeader'

const Plot = createPlotlyComponent(Plotly)

const ICON = (
  <svg width="22" height="22" fill="none" viewBox="0 0 24 24" stroke="white" strokeWidth="1.8">
    <path strokeLinecap="round" strokeLinejoin="round"
      d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-3 3-3-3z" />
  </svg>
)

const EXAMPLES = [
  'Show me the top 10 highest temperature readings',
  'Average salinity per platform',
  'List all floats and their cycle counts',
  'Pressure vs temperature for platform 5906343',
  'Which float has the deepest observations?',
  'Temperature readings above 28°C',
]

function toCsv(data, columns) {
  const rows = data.map(r => columns.map(c => JSON.stringify(r[c] ?? '')).join(','))
  return [columns.join(','), ...rows].join('\n')
}

function autoChart(data, columns) {
  if (!data?.length) return null
  if (columns.includes('TIME')) {
    const yCols = ['TEMP','PSAL','PRES',...columns.filter(c => typeof data[0][c]==='number' && c!=='TIME')]
    const yCol = yCols.find(c => columns.includes(c) && c !== 'TIME')
    if (!yCol) return null
    const sorted = [...data].sort((a,b)=>a.TIME<b.TIME?-1:1)
    const platforms = columns.includes('PLATFORM_NUMBER')
      ? [...new Set(sorted.map(d=>d.PLATFORM_NUMBER))]
      : [null]
    return {
      traces: platforms.map((p,i) => {
        const rows = p!==null ? sorted.filter(d=>d.PLATFORM_NUMBER===p) : sorted
        return { type:'scatter', mode:'lines', name: p!==null?String(p):yCol,
          x: rows.map(d=>d.TIME), y: rows.map(d=>d[yCol]),
          line: { color: CHART_COLORS[i%CHART_COLORS.length], width: 2 } }
      }),
      layout: oceanLayout({ height:320,
        title: { text:`${yCol} over Time`, font:{color:'#E8F4FD',size:13} },
        xaxis: { ...oceanLayout().xaxis, title:{text:'Date/Time',font:{color:'#8FACC8'}} },
        yaxis: { ...oceanLayout().yaxis, title:{text:yCol,font:{color:'#8FACC8'}} } }),
    }
  }
  const numCols = columns.filter(c => data[0] && typeof data[0][c]==='number')
  if (numCols.length >= 2) {
    return {
      traces: [{ type:'scatter', mode:'markers',
        x: data.map(d=>d[numCols[0]]), y: data.map(d=>d[numCols[1]]),
        marker: { color: CHART_COLORS[0], opacity: 0.7, size: 6 } }],
      layout: oceanLayout({ height:320,
        title: { text:`${numCols[0]} vs ${numCols[1]}`, font:{color:'#E8F4FD',size:13} },
        xaxis: { ...oceanLayout().xaxis, title:{text:numCols[0],font:{color:'#8FACC8'}} },
        yaxis: { ...oceanLayout().yaxis, title:{text:numCols[1],font:{color:'#8FACC8'}} } }),
    }
  }
  return null
}

export default function Chatbot() {
  const [messages, setMessages] = useState([])
  const [input, setInput]       = useState('')
  const [loading, setLoading]   = useState(false)
  const [sqlOpen, setSqlOpen]   = useState({})
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  async function send() {
    const text = input.trim()
    if (!text || loading) return
    setInput('')
    setMessages(prev => [...prev, { role:'user', text }])
    setLoading(true)
    try {
      const res = await postChat(text)
      setMessages(prev => [...prev, { role:'assistant', res }])
    } catch (e) {
      setMessages(prev => [...prev, { role:'assistant', res:{ error: e.message } }])
    }
    setLoading(false)
  }

  function handleKey(e) {
    if (e.key==='Enter' && !e.shiftKey) { e.preventDefault(); send() }
  }

  function download(data, columns) {
    const a = document.createElement('a')
    a.href = URL.createObjectURL(new Blob([toCsv(data, columns)],{type:'text/csv'}))
    a.download = 'query_results.csv'; a.click()
  }

  return (
    <div style={{ animation:'fadeUp 0.4s ease', display:'flex', flexDirection:'column', height:'calc(100vh - 4rem)', overflow:'hidden' }}>
      <PageHeader icon={ICON} title="Chat with Ocean Data"
        subtitle="Ask anything in plain English — the AI generates SQL and the database executes it instantly." />

      <div style={{ flex:1, display:'flex', gap:'1.25rem', overflow:'hidden', minHeight:0 }}>

        {/* ── Left: schema + examples ── */}
        <div style={{
          width: 200, flexShrink:0, display:'flex', flexDirection:'column', gap:'0.6rem',
          overflowY:'auto', paddingBottom:'0.5rem', minHeight:0,
        }}>
          <div style={{ fontSize:'0.67rem', fontWeight:700, color:'var(--tx3)', textTransform:'uppercase', letterSpacing:'0.12em' }}>
            Schema
          </div>
          <div style={{
            background:'#060F1E', border:'1px solid var(--border)', borderRadius:8,
            padding:'0.65rem 0.7rem',
            fontFamily:"'JetBrains Mono',monospace", fontSize:'0.7rem', lineHeight:1.75,
          }}>
            <span style={{color:'#8FACC8'}}>TABLE </span>
            <span style={{color:'#00D4FF', fontWeight:700}}>argo_profiles</span><br/>
            {[
              ['#4ECDC4','PLATFORM_NUMBER'],
              ['#4ECDC4','CYCLE_NUMBER'],
              ['#00D4FF','PRES'],
              ['#44A5E0','PSAL'],
              ['#00C6B8','TEMP'],
              ['#4ECDC4','LATITUDE'],
              ['#4ECDC4','LONGITUDE'],
              ['#4ECDC4','TIME'],
            ].map(([c,n]) => (
              <span key={n}>&nbsp;&nbsp;<span style={{color:c}}>{n}</span><br/></span>
            ))}
          </div>

          <div style={{ fontSize:'0.67rem', fontWeight:700, color:'var(--tx3)', textTransform:'uppercase', letterSpacing:'0.12em', marginTop:'0.25rem' }}>
            Examples
          </div>
          {EXAMPLES.map(ex => (
            <div key={ex} onClick={() => setInput(ex)}
              style={{
                padding:'0.4rem 0.6rem',
                background:'rgba(0,148,198,0.06)', border:'1px solid rgba(0,148,198,0.14)',
                borderRadius:6, fontSize:'0.75rem', color:'var(--tx2)',
                cursor:'pointer', transition:'all 0.15s', lineHeight:1.45,
              }}
              onMouseEnter={e => { e.currentTarget.style.background='rgba(0,148,198,0.14)'; e.currentTarget.style.color='var(--a3)'; e.currentTarget.style.borderColor='rgba(0,148,198,0.3)' }}
              onMouseLeave={e => { e.currentTarget.style.background='rgba(0,148,198,0.06)'; e.currentTarget.style.color='var(--tx2)'; e.currentTarget.style.borderColor='rgba(0,148,198,0.14)' }}
            >
              {ex}
            </div>
          ))}

          {messages.length > 0 && (
            <button onClick={() => setMessages([])}
              style={{
                marginTop:'auto', padding:'0.4rem', background:'rgba(255,107,107,0.07)',
                border:'1px solid rgba(255,107,107,0.2)', borderRadius:7,
                color:'var(--err)', fontSize:'0.78rem', fontWeight:600,
                cursor:'pointer', transition:'background 0.15s',
              }}
              onMouseEnter={e => e.currentTarget.style.background='rgba(255,107,107,0.15)'}
              onMouseLeave={e => e.currentTarget.style.background='rgba(255,107,107,0.07)'}
            >
              Clear chat
            </button>
          )}
        </div>

        {/* ── Right: chat ── */}
        <div style={{ flex:1, display:'flex', flexDirection:'column', overflow:'hidden', minWidth:0 }}>

          {/* AI status */}
          <div style={{
            display:'inline-flex', alignItems:'center', gap:'0.45rem',
            padding:'0.28rem 0.8rem', marginBottom:'0.75rem',
            background:'rgba(0,200,150,0.07)', border:'1px solid rgba(0,200,150,0.2)',
            borderRadius:24, fontSize:'0.72rem', fontWeight:600, color:'var(--ok)',
            letterSpacing:'0.05em', alignSelf:'flex-start',
          }}>
            <span style={{ width:7, height:7, borderRadius:'50%', background:'var(--ok)', animation:'pulseGlow 2s ease infinite', display:'inline-block' }}/>
            AI ready
          </div>

          {/* Messages */}
          <div style={{ flex:1, overflowY:'auto', display:'flex', flexDirection:'column', gap:'0.65rem', paddingRight:'0.3rem' }}>
            {messages.length===0 && !loading && (
              <div style={{
                flex:1, display:'flex', flexDirection:'column',
                alignItems:'center', justifyContent:'center',
                color:'var(--tx3)', fontSize:'0.9rem', gap:'0.5rem',
                animation:'fadeIn 0.4s ease',
              }}>
                <svg width="40" height="40" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="1" opacity="0.35">
                  <path strokeLinecap="round" strokeLinejoin="round"
                    d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-3 3-3-3z" />
                </svg>
                Ask a question or click an example to start
              </div>
            )}

            {messages.map((msg, i) => {
              if (msg.role==='user') return (
                <div key={i} style={{ display:'flex', justifyContent:'flex-end' }}>
                  <div style={{
                    maxWidth:'72%', padding:'0.7rem 1rem',
                    background:'linear-gradient(135deg,rgba(0,148,198,0.18),rgba(0,198,184,0.12))',
                    border:'1px solid rgba(0,148,198,0.28)',
                    borderRadius:'12px 12px 4px 12px',
                    fontSize:'0.9rem', color:'var(--tx)', lineHeight:1.55,
                    animation:'fadeUp 0.25s ease',
                  }}>
                    {msg.text}
                  </div>
                </div>
              )

              const { res } = msg
              const chart = res?.data ? autoChart(res.data, res.columns??[]) : null

              return (
                <div key={i} style={{
                  background:'linear-gradient(135deg,var(--surface),var(--surf2))',
                  border:'1px solid var(--border)', borderRadius:'4px 12px 12px 12px',
                  padding:'0.85rem 1rem', animation:'fadeUp 0.3s ease',
                }}>
                  {res?.error && (
                    <div style={{ color:'var(--err)', fontSize:'0.875rem', background:'rgba(255,107,107,0.07)', border:'1px solid rgba(255,107,107,0.2)', borderRadius:8, padding:'0.6rem 0.8rem' }}>
                      {res.error}
                    </div>
                  )}

                  {res?.sql && (
                    <div style={{ marginBottom:'0.65rem' }}>
                      <button onClick={() => setSqlOpen(p=>({...p,[i]:!p[i]}))}
                        style={{ display:'flex', alignItems:'center', gap:'0.4rem', background:'none', border:'none', color:'var(--a3)', fontSize:'0.8rem', fontWeight:600, cursor:'pointer', padding:0 }}>
                        <svg width="12" height="12" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2"
                          style={{ transform: sqlOpen[i]?'rotate(90deg)':'rotate(0deg)', transition:'transform 0.2s' }}>
                          <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7"/>
                        </svg>
                        Generated SQL
                      </button>
                      {sqlOpen[i] && (
                        <pre style={{ marginTop:'0.45rem', background:'#060F1E', border:'1px solid var(--border)', borderRadius:7, padding:'0.65rem 0.8rem', fontFamily:"'JetBrains Mono',monospace", fontSize:'0.78rem', color:'var(--a3)', overflowX:'auto', lineHeight:1.6 }}>
                          {res.sql}
                        </pre>
                      )}
                    </div>
                  )}

                  {res?.data && res.data.length > 0 && (
                    <>
                      <div style={{ display:'inline-flex', alignItems:'center', gap:'0.4rem', padding:'0.25rem 0.65rem', background:'rgba(0,200,150,0.09)', border:'1px solid rgba(0,200,150,0.22)', borderRadius:24, fontSize:'0.72rem', fontWeight:600, color:'var(--ok)', marginBottom:'0.6rem' }}>
                        <svg width="10" height="10" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2.5"><path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7"/></svg>
                        {(res.row_count??res.data.length).toLocaleString()} row{res.row_count!==1?'s':''}
                        {res.row_count > 100 && <span style={{color:'var(--tx3)',fontWeight:400}}>&nbsp;(showing 100)</span>}
                      </div>

                      {/* table */}
                      <div style={{ overflowX:'auto', marginBottom:'0.65rem', border:'1px solid var(--border)', borderRadius:8, maxHeight:300 }}>
                        <table style={{ width:'100%', borderCollapse:'collapse', fontFamily:"'JetBrains Mono',monospace", fontSize:'0.72rem' }}>
                          <thead style={{ position:'sticky', top:0, zIndex:1 }}>
                            <tr style={{ background:'var(--surf2)' }}>
                              {res.columns.map(c => (
                                <th key={c} style={{ padding:'0.45rem 0.65rem', textAlign:'left', color:'var(--tx2)', fontWeight:700, borderBottom:'1px solid var(--border)', whiteSpace:'nowrap', fontSize:'0.64rem', textTransform:'uppercase', letterSpacing:'0.06em' }}>{c}</th>
                              ))}
                            </tr>
                          </thead>
                          <tbody>
                            {res.data.map((row, ri) => (
                              <tr key={ri} style={{ background: ri%2===0?'var(--surface)':'var(--surf2)', transition:'background 0.12s' }}
                                onMouseEnter={e=>e.currentTarget.style.background='rgba(0,148,198,0.08)'}
                                onMouseLeave={e=>e.currentTarget.style.background=ri%2===0?'var(--surface)':'var(--surf2)'}
                              >
                                {res.columns.map(c => (
                                  <td key={c} style={{ padding:'0.4rem 0.65rem', color:'var(--tx)', borderBottom:'1px solid rgba(26,51,85,0.4)', whiteSpace:'nowrap' }}>
                                    {row[c]??'—'}
                                  </td>
                                ))}
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>

                      <button onClick={() => download(res.data, res.columns)}
                        style={{ marginBottom:'0.65rem', padding:'0.35rem 0.85rem', background:'rgba(0,148,198,0.09)', border:'1px solid rgba(0,148,198,0.22)', borderRadius:7, color:'var(--a3)', fontSize:'0.78rem', fontWeight:600, cursor:'pointer', transition:'background 0.15s' }}
                        onMouseEnter={e=>e.currentTarget.style.background='rgba(0,148,198,0.18)'}
                        onMouseLeave={e=>e.currentTarget.style.background='rgba(0,148,198,0.09)'}>
                        Download CSV
                      </button>

                      {chart && (
                        <Plot data={chart.traces} layout={chart.layout}
                          config={plotConfig} useResizeHandler style={{ width:'100%' }} />
                      )}
                    </>
                  )}

                  {res?.data?.length===0 && !res?.error && (
                    <div style={{ color:'var(--tx2)', fontSize:'0.875rem' }}>
                      Query ran successfully but returned 0 rows.
                    </div>
                  )}
                </div>
              )
            })}

            {/* Typing indicator */}
            {loading && (
              <div style={{ display:'flex', animation:'fadeIn 0.25s ease' }}>
                <div style={{ background:'var(--surface)', border:'1px solid var(--border)', borderRadius:'4px 12px 12px 12px', padding:'0.7rem 1rem', display:'flex', gap:'5px', alignItems:'center' }}>
                  {[0,0.18,0.36].map(d => (
                    <div key={d} style={{ width:8, height:8, borderRadius:'50%', background:'var(--a3)', animation:`blink 1.2s ease ${d}s infinite` }}/>
                  ))}
                </div>
              </div>
            )}

            <div ref={bottomRef}/>
          </div>

          {/* Input */}
          <div style={{ paddingTop:'0.75rem', borderTop:'1px solid var(--border)', marginTop:'0.5rem' }}>
            <div style={{ display:'flex', gap:'0.6rem' }}>
              <textarea value={input} onChange={e=>setInput(e.target.value)} onKeyDown={handleKey}
                placeholder="e.g. Show me temperature readings above 28°C …"
                rows={2}
                style={{
                  flex:1, resize:'none',
                  background:'var(--surf2)', border:'1px solid var(--border)',
                  borderRadius:10, color:'var(--tx)',
                  fontFamily:"'Inter',sans-serif", fontSize:'0.9rem',
                  padding:'0.65rem 1rem', outline:'none', lineHeight:1.55,
                  transition:'border-color 0.2s, box-shadow 0.2s',
                }}
                onFocus={e=>{e.target.style.borderColor='var(--a3)';e.target.style.boxShadow='0 0 0 3px rgba(0,212,255,0.10)'}}
                onBlur={e=>{e.target.style.borderColor='var(--border)';e.target.style.boxShadow='none'}}
              />
              <button onClick={send} disabled={loading||!input.trim()}
                style={{
                  alignSelf:'stretch', padding:'0 1.25rem',
                  background: loading||!input.trim() ? 'rgba(0,148,198,0.25)' : 'linear-gradient(135deg,var(--a1),var(--a2))',
                  border:'none', borderRadius:10, color:'#fff',
                  fontWeight:700, fontSize:'0.875rem',
                  cursor: loading||!input.trim() ? 'not-allowed' : 'pointer',
                  transition:'all 0.2s', whiteSpace:'nowrap',
                  boxShadow: loading||!input.trim() ? 'none' : '0 2px 12px rgba(0,148,198,0.3)',
                }}
                onMouseEnter={e=>{ if(!loading&&input.trim()) e.currentTarget.style.transform='translateY(-1px)' }}
                onMouseLeave={e=>{ e.currentTarget.style.transform='' }}
              >
                {loading ? '…' : 'Ask'}
              </button>
            </div>
            <div style={{ marginTop:'0.35rem', fontSize:'0.72rem', color:'var(--tx3)' }}>
              Enter to send · Shift+Enter for new line
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
