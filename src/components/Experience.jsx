import { useRef, useEffect } from 'react'

const EXPERIENCE = [
  {
    role: 'Frontend Intern',
    company: 'MindFlix AI',
    period: 'Jan 2026 — Present',
    desc: 'Built secure auth workflows with Next.js + FastAPI, designed a centralized API layer, and implemented role-based access control.',
    fromRight: false,
  },
  {
    role: 'ML Intern',
    company: 'MIT Manipal CSE',
    period: 'Jun — Jul 2025',
    desc: 'Engineered diabetes prediction models achieving 96.8% accuracy and 0.96 ROC-AUC. Co-authored a research paper currently under review.',
    fromRight: true,
  },
  {
    role: 'Frontend Intern',
    company: 'Tax Hummer',
    period: 'Sept — Nov 2024',
    desc: 'Led development of the TH Service Desk in React + jQuery — reduced manual task tracking by 60% and improved team efficiency by 40%.',
    fromRight: false,
  },
]

function ExpItem({ exp }) {
  const ref = useRef(null)

  useEffect(() => {
    const el = ref.current
    if (!el) return
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) el.classList.add('visible')
        else el.classList.remove('visible')
      },
      { threshold: 0.12 }
    )
    observer.observe(el)
    return () => observer.disconnect()
  }, [])

  return (
    <li ref={ref} className={`exp-item reveal${exp.fromRight ? ' from-right' : ''}`}>
      <div>
        <p className="exp-role">{exp.role}</p>
        <p className="exp-company">{exp.company}</p>
        {exp.desc && <p className="exp-desc">{exp.desc}</p>}
      </div>
      <div className="exp-right">
        <span className="exp-period">{exp.period}</span>
      </div>
    </li>
  )
}

export default function Experience() {
  const headerRef = useRef(null)

  useEffect(() => {
    const el = headerRef.current
    if (!el) return
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) el.classList.add('visible')
        else el.classList.remove('visible')
      },
      { threshold: 0.12 }
    )
    observer.observe(el)
    return () => observer.disconnect()
  }, [])

  return (
    <section id="experience">
      <div className="section-header reveal from-right" ref={headerRef}>
        <span className="section-num">02</span>
        <h2 className="section-title">Experience</h2>
      </div>
      <ul className="exp-list">
        {EXPERIENCE.map((e) => <ExpItem key={e.company} exp={e} />)}
      </ul>
    </section>
  )
}
