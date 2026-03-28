import { useEffect } from 'react'

const HOVER_SELECTORS = 'a, button, .skill-cell, .stat-item, .project-item, .exp-item'

export default function Cursor() {
  useEffect(() => {
    const cur = document.getElementById('cursor')

    const move = (e) => {
      cur.style.left = e.clientX + 'px'
      cur.style.top  = e.clientY + 'px'
    }

    // use event delegation — works for all elements including dynamically rendered ones
    const over = (e) => {
      if (e.target.closest(HOVER_SELECTORS)) {
        cur.classList.add('hover')
      }
    }

    const out = (e) => {
      if (e.target.closest(HOVER_SELECTORS)) {
        cur.classList.remove('hover')
      }
    }

    document.addEventListener('mousemove', move)
    document.addEventListener('mouseover', over)
    document.addEventListener('mouseout', out)

    return () => {
      document.removeEventListener('mousemove', move)
      document.removeEventListener('mouseover', over)
      document.removeEventListener('mouseout', out)
    }
  }, [])

  return <div id="cursor" />
}
