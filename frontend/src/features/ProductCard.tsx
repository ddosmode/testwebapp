import { Link } from "react-router-dom";
import type { Product } from "@/lib/api";
import { ShoppingCart } from "lucide-react";

interface ProductCardProps {
  product: Product;
}

export default function ProductCard({ product }: ProductCardProps) {
  return (
    <Link
      to={`/product/${product.id}`}
      className="block bg-card rounded-lg border shadow-sm overflow-hidden hover:shadow-md transition-shadow"
    >
      <div className="aspect-square bg-muted flex items-center justify-center">
        <ShoppingCart className="h-12 w-12 text-muted-foreground" />
      </div>
      <div className="p-3">
        <h3 className="font-medium text-sm truncate">{product.name}</h3>
        <p className="text-xs text-muted-foreground mt-1 line-clamp-2">
          {product.description}
        </p>
        <div className="mt-2 flex items-center justify-between">
          <span className="text-sm font-semibold text-primary">
            €{parseFloat(product.price).toFixed(2)}
          </span>
          <span className="text-xs text-muted-foreground">In stock</span>
        </div>
      </div>
    </Link>
  );
}
