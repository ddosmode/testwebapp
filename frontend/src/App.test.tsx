import { describe, it, expect } from 'vitest'
import { createRoot } from 'react-dom/client'
import { act } from 'react-dom/test-utils'
import App from './App'

describe('App', () => {
  it('renders the heading', () => {
    const container = document.createElement('div')
    document.body.appendChild(container)
    const root = createRoot(container)

    act(() => {
      root.render(<App />)
    })

    expect(container.textContent).toContain('Legal Commerce Platform')

    act(() => {
      root.unmount()
    })
    document.body.removeChild(container)
  })
})
