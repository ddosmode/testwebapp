import { useState, useEffect } from 'react'
import { api } from '@/lib/api'

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
    api.get('/catalog/products')
      .then((res) => setProducts(res.data))
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
