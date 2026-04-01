import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Sidebar from './components/Sidebar'
import Home     from './pages/Home'
import Overview from './pages/Overview'
import MapPage  from './pages/MapPage'
import Trends   from './pages/Trends'
import Chatbot  from './pages/Chatbot'

export default function App() {
  return (
    <BrowserRouter>
      <Sidebar />
      <main style={{
        marginLeft: 'var(--sidebar)',
        width: 'calc(100% - var(--sidebar))',
        padding: '1.75rem 2.25rem 2.5rem',
        minHeight: '100vh',
        background: 'linear-gradient(160deg,#020B18 0%,#040D1C 60%,#020B18 100%)',
        boxSizing: 'border-box',
      }}>
        <Routes>
          <Route path="/"        element={<Home />} />
          <Route path="/overview" element={<Overview />} />
          <Route path="/map"      element={<MapPage />} />
          <Route path="/trends"   element={<Trends />} />
          <Route path="/chatbot"  element={<Chatbot />} />
        </Routes>
      </main>
    </BrowserRouter>
  )
}
