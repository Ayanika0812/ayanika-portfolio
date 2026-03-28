import { useReveal } from '../hooks/useReveal'

export default function Positioning() {
  const ref = useReveal()

  return (
    <section id="positioning">
      <div className="positioning-inner reveal" ref={ref}>
        <p className="pos-text">
          I build <span>AI-powered systems</span> and scalable web applications,
          focusing on real-world usability, performance, and clean architecture.
        </p>
      </div>
    </section>
  )
}
