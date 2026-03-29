import { useEffect, useRef } from 'react'

const WORDS = ['AYANIKA', 'PAUL']

export default function Hero() {
  const canvasRef = useRef(null)
  const initialized = useRef(false)

  // letter animation
  useEffect(() => {
    if (initialized.current) return
    initialized.current = true
    let delay = 0.4
    WORDS.forEach((word, wi) => {
      const el = document.getElementById(`word${wi + 1}`)
      if (!el) return
      el.innerHTML = ''
      word.split('').forEach((ch) => {
        const span = document.createElement('span')
        span.className = 'letter'
        span.textContent = ch
        span.style.animationDelay = delay + 's'
        delay += 0.07
        el.appendChild(span)
      })
    })
  }, [])

  // subtle particle canvas
  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    let stars = []
    let raf

    const resize = () => {
      canvas.width  = canvas.offsetWidth
      canvas.height = canvas.offsetHeight
      stars = Array.from({ length: 80 }, () => ({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        r: Math.random() * 1.2 + 0.2,
        t: Math.random() * Math.PI * 2,
        s: Math.random() * 0.008 + 0.003,
      }))
    }

    const draw = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height)
      stars.forEach(s => {
        s.t += s.s
        const alpha = 0.08 + 0.12 * Math.sin(s.t)
        ctx.beginPath()
        ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2)
        ctx.fillStyle = `rgba(0,0,0,${alpha})`
        ctx.fill()
      })
      raf = requestAnimationFrame(draw)
    }

    resize()
    draw()
    window.addEventListener('resize', resize)
    return () => { cancelAnimationFrame(raf); window.removeEventListener('resize', resize) }
  }, [])

  return (
    <section id="hero">
      <canvas ref={canvasRef} className="hero-canvas" aria-hidden="true" />
      <p className="hero-eyebrow">// Full Stack Developer building AI-powered systems</p>
      <h1 className="hero-name" aria-label="Ayanika Paul">
        <span className="word" id="word1" />
        <span className="word" id="word2" />
      </h1>
      <div className="hero-bottom">
        <p className="hero-role">
          Building <span>AI-powered systems</span> and scalable full-stack applications that solve real-world problems.
        </p>
        <div className="hero-links">
          <a href="https://github.com/Ayanika0812" target="_blank" rel="noopener noreferrer">GitHub</a>
          <a href="https://linkedin.com/in/ayanika-paul" target="_blank" rel="noopener noreferrer">LinkedIn</a>
          <a href="mailto:contactayanika@gmail.com">Email</a>
        </div>
      </div>
      <span className="hero-scroll-hint">↓</span>
    </section>
  )
}
