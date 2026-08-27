import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'

function Hello() {
  return <div>Hello</div>
}

describe('smoke', () => {
  it('renders a div', () => {
    render(<Hello />)
    expect(screen.getByText('Hello')).toBeDefined()
  })
})
