import { useReveal } from '../hooks/useReveal'

const STATS = [
  { number: '96.8%', label: 'ML Model Accuracy' },
  { number: '60%',   label: 'Reduction in Manual Work' },
  { number: '40%',   label: 'Improvement in Task Efficiency' },
]

export default function Stats() {
  const ref = useReveal()

  return (
    <section id="stats" className="reveal" ref={ref}>
      {STATS.map((s, i) => (
        <div className="stat-item" key={i}>
          <span className="stat-number">{s.number}</span>
          <span className="stat-label">{s.label}</span>
        </div>
      ))}
    </section>
  )
}
