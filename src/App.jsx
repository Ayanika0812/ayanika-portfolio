import { useEffect } from 'react'
import Cursor      from './components/Cursor'
import Nav         from './components/Nav'
import Hero        from './components/Hero'
import Marquee     from './components/Marquee'
import Positioning from './components/Positioning'
import Stats       from './components/Stats'
import Projects    from './components/Projects'
import Experience  from './components/Experience'
import Skills      from './components/Skills'
import Contact     from './components/Contact'

const TRACKER_URL = import.meta.env.VITE_TRACKER_URL || 'http://127.0.0.1:8000'

export default function App() {
  useEffect(() => {
    // track visit
    fetch(`${TRACKER_URL}/track`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ referrer: document.referrer || 'direct' }),
    }).catch(() => {})
  }, [])

  return (
    <>
      <Cursor />
      <Nav />
      <Hero />
      <Marquee />
      <Positioning />
      <Stats />
      <Projects />
      <Experience />
      <Skills />
      <Contact />
      <footer>
        <span>© 2026 Ayanika Paul</span>
        <span>Full Stack Developer &amp; AI Engineer</span>
      </footer>
    </>
  )
}
