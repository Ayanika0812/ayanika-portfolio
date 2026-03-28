const SKILLS = [
  'React','✦','Next.js','✦','Python','✦','FastAPI','✦',
  'Machine Learning','✦','Tailwind CSS','✦','Node.js','✦',
  'MongoDB','✦','Full Stack','✦','AI Engineer','✦',
]

// duplicate for seamless infinite scroll
const items = [...SKILLS, ...SKILLS]

export default function Marquee() {
  return (
    <div className="marquee-wrap" aria-hidden="true">
      <div className="marquee-track">
        {items.map((s, i) => (
          <span key={i} className={s === '✦' ? 'dot' : ''}>{s}</span>
        ))}
      </div>
    </div>
  )
}
