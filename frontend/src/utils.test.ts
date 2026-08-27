import { describe, it, expect } from 'vitest'
import { formatPrice, isPositiveNumber } from './utils'

describe('formatPrice', () => {
  it('formats a number to 2 decimal places', () => {
    expect(formatPrice(9.9)).toBe('9.90')
  })

  it('formats a string number', () => {
    expect(formatPrice('19.99')).toBe('19.99')
  })

  it('returns 0.00 for NaN', () => {
    expect(formatPrice(NaN)).toBe('0.00')
  })
})

describe('isPositiveNumber', () => {
  it('returns true for positive numbers', () => {
    expect(isPositiveNumber(1)).toBe(true)
    expect(isPositiveNumber(0.1)).toBe(true)
  })

  it('returns false for zero and negative', () => {
    expect(isPositiveNumber(0)).toBe(false)
    expect(isPositiveNumber(-1)).toBe(false)
  })

  it('returns false for NaN', () => {
    expect(isPositiveNumber(NaN)).toBe(false)
  })
})
