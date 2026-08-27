import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import App from '../App'

describe('App with ProductList', () => {
  it('renders ProductList via App', () => {
    render(<App />)
    expect(screen.getByText('Loading...')).toBeDefined()
  })
})
