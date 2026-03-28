import { useRef, useEffect } from 'react'

const SKILLS = ['React', 'Next.js', 'Python', 'FastAPI', 'ML / AI', 'Tailwind', 'Node.js', 'MongoDB']

export default function Skills() {
  const headerRef = useRef(null)
  const cellRefs  = useRef([])

  useEffect(() => {
    const els = [headerRef.current, ...cellRefs.current].filter(Boolean)
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) entry.target.classList.add('visible')
          else entry.target.classList.remove('visible')
        })
      },
      { threshold: 0.12 }
    )
    els.forEach((el) => observer.observe(el))
    return () => observer.disconnect()
  }, [])

  return (
    <section id="skills">
      <div className="section-header reveal" ref={headerRef}>
        <span className="section-num">03</span>
        <h2 className="section-title">Skills</h2>
      </div>
      <div className="skills-grid">
        {SKILLS.map((skill, i) => (
          <div
            key={skill}
            className={`skill-cell reveal${i % 2 !== 0 ? ' from-right' : ''}`}
            style={{ '--i': i }}
            ref={(el) => (cellRefs.current[i] = el)}
          >
            {skill}
          </div>
        ))}
      </div>
    </section>
  )
}
