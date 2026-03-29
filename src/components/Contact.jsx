import { useRef, useState } from 'react'
import { useReveal } from '../hooks/useReveal'

const TRACKER_URL = window.location.hostname === 'localhost'
  ? 'http://127.0.0.1:8000'
  : 'https://ayanika-tracker.onrender.com'

export default function Contact() {
  const ctaRef   = useReveal()
  const linksRef = useReveal()
  const formRef  = useReveal()

  const [name, setName]       = useState('')
  const [email, setEmail]     = useState('')
  const [message, setMessage] = useState('')
  const [status, setStatus]   = useState('idle') // idle | sending | done

  const handleSubmit = async (e) => {
    e.preventDefault()
    setStatus('sending')
    try {
      await fetch(`${TRACKER_URL}/contact`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, message }),
      })
      setStatus('done')
    } catch {
      window.location.href = `mailto:contactayanika@gmail.com?subject=Message from ${name}&body=${message}`
    }
  }

  return (
    <section id="contact">
      <div className="section-header reveal" ref={useReveal()}>
        <span className="section-num">04</span>
        <h2 className="section-title">Contact</h2>
      </div>
      <div className="contact-body">
        <p className="contact-cta reveal" ref={ctaRef}>
          Let's<br />Build<br /><span>Together.</span>
        </p>
        <div className="contact-links reveal from-right" ref={linksRef}>
          <a href="mailto:contactayanika@gmail.com">contactayanika@gmail.com</a>
          <a href="https://github.com/Ayanika0812" target="_blank" rel="noopener noreferrer">github.com/Ayanika0812</a>
          <a href="https://linkedin.com/in/ayanika-paul" target="_blank" rel="noopener noreferrer">linkedin.com/in/ayanika-paul</a>
        </div>

        <form className="contact-form reveal" ref={formRef} onSubmit={handleSubmit}>
          <div className="form-row">
            <div className="form-field">
              <label>Your Name</label>
              <input type="text" placeholder="Your name" required value={name} onChange={e => setName(e.target.value)} />
              <span className="field-line" />
            </div>
            <div className="form-field">
              <label>Your Email</label>
              <input type="email" placeholder="your@email.com" required value={email} onChange={e => setEmail(e.target.value)} />
              <span className="field-line" />
            </div>
          </div>
          <div className="form-row single">
            <div className="form-field">
              <label>Message</label>
              <textarea rows="4" placeholder="What's on your mind?" required value={message} onChange={e => setMessage(e.target.value)} />
              <span className="field-line" />
            </div>
          </div>
          {status !== 'done' && (
            <button type="submit" className="form-submit" disabled={status === 'sending'}>
              {status === 'sending' ? 'Sending...' : 'Send Message →'}
            </button>
          )}
          <div className={`form-success${status === 'done' ? ' show' : ''}`}>
            ✦ Message received — I'll get back to you soon.
          </div>
        </form>
      </div>
    </section>
  )
}
