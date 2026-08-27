import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { ProductList } from '../components/ProductList'

describe('ProductList', () => {
  it('shows loading state initially', () => {
    render(<ProductList />)
    expect(screen.getByText('Loading...')).toBeDefined()
  })
})
