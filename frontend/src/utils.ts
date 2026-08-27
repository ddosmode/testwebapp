export function formatPrice(price: string | number): string {
  const num = typeof price === 'string' ? Number(price) : price
  if (Number.isNaN(num)) return '0.00'
  return num.toFixed(2)
}

export function isPositiveNumber(value: number): boolean {
  return Number.isFinite(value) && value > 0
}
