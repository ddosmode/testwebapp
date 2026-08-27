import { useCartStore } from "@/entities/cartStore";
import type { Product } from "@/lib/api";

interface CartItemProps {
  product: Product;
  quantity: number;
}

export default function CartItem({ product, quantity }: CartItemProps) {
  const removeItem = useCartStore((state) => state.removeItem);
  const updateQuantity = useCartStore((state) => state.updateQuantity);

  return (
    <div className="flex gap-3 p-3 bg-card rounded-lg border">
      <div className="w-16 h-16 bg-muted rounded-md flex items-center justify-center flex-shrink-0">
        <span className="text-xs text-muted-foreground">IMG</span>
      </div>
      <div className="flex-1 min-w-0">
        <h3 className="font-medium text-sm truncate">{product.name}</h3>
        <p className="text-sm font-semibold text-primary mt-1">
          €{parseFloat(product.price).toFixed(2)}
        </p>
        <div className="flex items-center gap-2 mt-2">
          <button
            onClick={() => updateQuantity(product.id, quantity - 1)}
            className="w-6 h-6 rounded-full border flex items-center justify-center text-xs hover:bg-muted"
          >
            -
          </button>
          <span className="text-sm w-8 text-center">{quantity}</span>
          <button
            onClick={() => updateQuantity(product.id, quantity + 1)}
            className="w-6 h-6 rounded-full border flex items-center justify-center text-xs hover:bg-muted"
          >
            +
          </button>
          <button
            onClick={() => removeItem(product.id)}
            className="ml-auto text-xs text-destructive hover:underline"
          >
            Remove
          </button>
        </div>
      </div>
    </div>
  );
}
