import { useEffect, useRef } from 'react'

export default function Nav() {
  const navRef = useRef(null)

  useEffect(() => {
    let lastY = 0
    const nav = navRef.current

    const onScroll = () => {
      const y = window.scrollY
      if (y > lastY && y > 80) {
        nav.style.transform = 'translateY(-100%)'
      } else {
        nav.style.transform = 'translateY(0)'
      }
      lastY = y
    }

    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  return (
    <nav ref={navRef}>
      <span className="nav-logo">AP</span>
      <ul>
        <li><a href="#projects">Projects</a></li>
        <li><a href="#experience">Exp</a></li>
        <li><a href="#skills">Skills</a></li>
        <li><a href="#contact">Contact</a></li>
      </ul>
    </nav>
  )
}
