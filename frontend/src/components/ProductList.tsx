import React, { useState, useEffect } from 'react'

export interface Product {
  id: string
  name: string
  price: string
  is_active: boolean
}

export function ProductList() {
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetch('/catalog/products')
      .then((res) => {
        if (!res.ok) throw new Error('Failed to fetch')
        return res.json()
      })
      .then(setProducts)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <p>Loading...</p>
  if (error) return <p>Error: {error}</p>

  return (
    <ul>
      {products.map((p) => (
        <li key={p.id}>
          {p.name} - {p.price}
        </li>
      ))}
    </ul>
  )
}
