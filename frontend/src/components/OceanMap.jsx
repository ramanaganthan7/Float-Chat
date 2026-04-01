/**
 * OceanMap — Real interactive Leaflet map with CartoDB Dark Matter tiles.
 * Renders ARGO float positions as colour-coded circle markers.
 */
import { useEffect, useRef } from 'react'
import { MapContainer, TileLayer, CircleMarker, Tooltip, useMap } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'

const PARAM_LABELS = {
  TEMP: 'Temperature (°C)',
  PSAL: 'Salinity (PSU)',
  PRES: 'Pressure (dbar)',
}

// 5-stop colour scale: deep navy → ocean blue → cyan → teal → warm
const COLOR_STOPS = [
  [2,  11,  24],   // t=0.00  #020B18
  [0,  80, 180],   // t=0.25  deep blue
  [0, 148, 198],   // t=0.50  ocean blue
  [0, 198, 184],   // t=0.75  teal
  [0, 212, 255],   // t=1.00  cyan
]

function lerp(a, b, t) { return a + (b - a) * t }

function valueToColor(value, min, max) {
  const t = Math.max(0, Math.min(1, (value - min) / (max - min || 1)))
  const scaled = t * (COLOR_STOPS.length - 1)
  const lo = Math.floor(scaled)
  const hi = Math.min(lo + 1, COLOR_STOPS.length - 1)
  const frac = scaled - lo
  const r = Math.round(lerp(COLOR_STOPS[lo][0], COLOR_STOPS[hi][0], frac))
  const g = Math.round(lerp(COLOR_STOPS[lo][1], COLOR_STOPS[hi][1], frac))
  const b = Math.round(lerp(COLOR_STOPS[lo][2], COLOR_STOPS[hi][2], frac))
  return `rgb(${r},${g},${b})`
}

// Legend gradient stops for display
function colorAt(t) {
  const scaled = t * (COLOR_STOPS.length - 1)
  const lo = Math.floor(scaled)
  const hi = Math.min(lo + 1, COLOR_STOPS.length - 1)
  const frac = scaled - lo
  const r = Math.round(lerp(COLOR_STOPS[lo][0], COLOR_STOPS[hi][0], frac))
  const g = Math.round(lerp(COLOR_STOPS[lo][1], COLOR_STOPS[hi][1], frac))
  const b = Math.round(lerp(COLOR_STOPS[lo][2], COLOR_STOPS[hi][2], frac))
  return `rgb(${r},${g},${b})`
}

// Flyto centre when data changes
function MapController({ center }) {
  const map = useMap()
  useEffect(() => { map.setView(center, map.getZoom()) }, [center])
  return null
}

export default function OceanMap({ data, colorBy = 'TEMP', height = 560 }) {
  if (!data || data.length === 0) return null

  const values  = data.map(d => d[colorBy]).filter(v => v != null)
  const minVal  = Math.min(...values)
  const maxVal  = Math.max(...values)
  const midVal  = ((minVal + maxVal) / 2).toFixed(2)

  const centerLat = data.reduce((s, d) => s + d.LATITUDE,  0) / data.length
  const centerLon = data.reduce((s, d) => s + d.LONGITUDE, 0) / data.length

  const LABEL = PARAM_LABELS[colorBy] || colorBy

  return (
    <div style={{ position: 'relative', borderRadius: 12, overflow: 'hidden',
                  border: '1px solid #1A3355', boxShadow: '0 4px 24px rgba(0,0,0,0.4)' }}>
      <MapContainer
        center={[centerLat, centerLon]}
        zoom={3}
        style={{ height, width: '100%', background: '#020B18' }}
        preferCanvas
        zoomControl
      >
        <MapController center={[centerLat, centerLon]} />

        <TileLayer
          url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright" style="color:#8FACC8">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions" style="color:#8FACC8">CARTO</a>'
          subdomains="abcd"
          maxZoom={19}
        />

        {data.map((d, i) => {
          const val   = d[colorBy]
          const color = val != null ? valueToColor(val, minVal, maxVal) : '#1A3355'
          return (
            <CircleMarker
              key={i}
              center={[d.LATITUDE, d.LONGITUDE]}
              radius={5}
              pathOptions={{
                fillColor: color,
                fillOpacity: 0.85,
                color: 'rgba(0,0,0,0.3)',
                weight: 0.5,
              }}
            >
              <Tooltip sticky>
                <div style={{
                  background: '#0A1628', border: '1px solid #1A3355',
                  borderRadius: 8, padding: '0.5rem 0.7rem',
                  fontFamily: 'Inter, sans-serif', fontSize: 12, color: '#E8F4FD',
                  lineHeight: 1.7, minWidth: 160,
                }}>
                  <div style={{ fontWeight: 700, color: '#00D4FF', marginBottom: 4 }}>
                    Float {d.PLATFORM_NUMBER}
                  </div>
                  <div style={{ color: '#8FACC8' }}>Cycle: {d.CYCLE_NUMBER}</div>
                  <div style={{ color: '#8FACC8' }}>Time: {String(d.TIME).slice(0, 16)}</div>
                  <hr style={{ border: 'none', borderTop: '1px solid #1A3355', margin: '4px 0' }} />
                  <div>Temp: <span style={{ color: '#00D4FF', fontWeight: 600 }}>{d.TEMP?.toFixed(2)} °C</span></div>
                  <div>Salinity: <span style={{ color: '#00C6B8', fontWeight: 600 }}>{d.PSAL?.toFixed(3)}</span></div>
                  <div>Pressure: <span style={{ color: '#7ECEF4', fontWeight: 600 }}>{d.PRES?.toFixed(1)} dbar</span></div>
                  <div style={{ color: '#8FACC8', marginTop: 2 }}>
                    {d.LATITUDE?.toFixed(3)}° / {d.LONGITUDE?.toFixed(3)}°
                  </div>
                </div>
              </Tooltip>
            </CircleMarker>
          )
        })}
      </MapContainer>

      {/* Colour legend overlay */}
      <div style={{
        position: 'absolute', bottom: 28, right: 12, zIndex: 1000,
        background: 'rgba(10,22,40,0.92)', border: '1px solid #1A3355',
        borderRadius: 8, padding: '0.5rem 0.75rem', minWidth: 130,
        backdropFilter: 'blur(6px)',
      }}>
        <div style={{ fontSize: 10, fontWeight: 700, color: '#8FACC8',
                      textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: 6 }}>
          {LABEL}
        </div>
        <div style={{
          height: 10, borderRadius: 5,
          background: `linear-gradient(to right, ${colorAt(0)}, ${colorAt(0.5)}, ${colorAt(1)})`,
          marginBottom: 4,
        }} />
        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
          <span style={{ fontSize: 9, color: '#8FACC8' }}>{minVal.toFixed(1)}</span>
          <span style={{ fontSize: 9, color: '#8FACC8' }}>{midVal}</span>
          <span style={{ fontSize: 9, color: '#8FACC8' }}>{maxVal.toFixed(1)}</span>
        </div>
      </div>
    </div>
  )
}
