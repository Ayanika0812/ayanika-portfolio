import { useRef, useEffect, useState } from 'react'

const PROJECTS = [
  {
    name: 'AI Project Reviewer',
    desc: 'AI-powered system for structured code analysis using LLMs, featuring dual-mode prompting and multi-model fallback for reliable feedback.',
    tags: ['AI / ML', 'FastAPI', 'React', 'Gemini'],
    live: 'https://ai-project-reviewer.vercel.app/',
    github: null,
    featured: true,
    fromRight: false,
    preview: 'https://ai-project-reviewer.vercel.app/',
  },
  {
    name: 'Hotel Booking App',
    desc: 'Full-stack MERN booking platform with Clerk authentication, Stripe payments, and real-time room availability.',
    tags: ['Full Stack', 'Node.js', 'MongoDB'],
    live: 'https://quickstay-orcin-rho.vercel.app/',
    github: null,
    featured: false,
    fromRight: true,
    preview: null,
  },
  {
    name: 'Movie Recommender',
    desc: 'Content-based recommender using cosine similarity on 5,000+ TMDB movies — built with Scikit-learn and a Streamlit UI.',
    tags: ['Python', 'ML'],
    live: null,
    github: 'https://github.com/Ayanika0812/Movie_Recommender_System',
    featured: false,
    fromRight: false,
    preview: null,
  },
  {
    name: 'E-Commerce Platform',
    desc: 'Fully responsive storefront with product browsing, filtering, and cart — built in React with Context API.',
    tags: ['React', 'Tailwind'],
    live: 'https://ayanika0812.github.io/Happyhaul-ecommerce/',
    github: null,
    featured: false,
    fromRight: true,
    preview: null,
  },
]

function PreviewModal({ url, onClose }) {
  return (
    <div className="preview-overlay" onClick={onClose}>
      <div className="preview-modal" onClick={e => e.stopPropagation()}>
        <div className="preview-bar">
          <span className="preview-url">{url}</span>
          <button className="preview-close" onClick={onClose}>✕</button>
        </div>
        <iframe src={url} title="Project Preview" className="preview-iframe" />
      </div>
    </div>
  )
}

function ProjectItem({ project }) {
  const ref = useRef(null)
  const [showPreview, setShowPreview] = useState(false)

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
    <>
      <li ref={ref} className={`project-item reveal${project.fromRight ? ' from-right' : ''}${project.featured ? ' featured' : ''}`}>
        <div className="project-left">
          <div className="project-name-row">
            <span className="project-name">{project.name}</span>
            {project.featured && <span className="featured-tag">Featured</span>}
          </div>
          {project.desc && <p className="project-desc">{project.desc}</p>}
          <div className="project-meta">
            {project.tags.map((t) => (
              <span className="project-tag" key={t}>{t}</span>
            ))}
          </div>
        </div>
        <div className={`project-links${project.featured ? ' project-preview-wrap' : ''}`}>
          {project.featured && project.preview && (
            <div className="preview-thumb">
              <iframe src={project.preview} title="preview" tabIndex="-1" />
            </div>
          )}
          {project.preview && (
            <button className="project-link preview-btn" onClick={() => setShowPreview(true)}>
              PREVIEW ⊙
            </button>
          )}
          {project.github && (
            <a href={project.github} target="_blank" rel="noopener noreferrer" className="project-link">
              GITHUB ↗
            </a>
          )}
          {project.live && (
            <a href={project.live} target="_blank" rel="noopener noreferrer" className="project-link">
              LIVE ↗
            </a>
          )}
        </div>
      </li>
      {showPreview && <PreviewModal url={project.preview} onClose={() => setShowPreview(false)} />}
    </>
  )
}

export default function Projects() {
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
    <section id="projects">
      <div className="section-header reveal" ref={headerRef}>
        <span className="section-num">01</span>
        <h2 className="section-title">Selected Work</h2>
      </div>
      <ul className="project-list">
        {PROJECTS.map((p) => <ProjectItem key={p.name} project={p} />)}
      </ul>
    </section>
  )
}
