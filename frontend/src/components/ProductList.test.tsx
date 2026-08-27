import { describe, it, expect } from 'vitest'
import { createRoot } from 'react-dom/client'
import { act } from 'react-dom/test-utils'
import { ProductList } from './ProductList'

describe('ProductList', () => {
  it('shows loading state initially', () => {
    const container = document.createElement('div')
    document.body.appendChild(container)
    const root = createRoot(container)

    act(() => {
      root.render(<ProductList />)
    })

    expect(container.textContent).toContain('Loading...')

    act(() => {
      root.unmount()
    })
    document.body.removeChild(container)
  })
})
