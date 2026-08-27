import PageContainer from "@/widgets/PageContainer";
import Header from "@/widgets/Header";
import CartItem from "@/features/CartItem";
import { useCartStore } from "@/entities/cartStore";
import { useNavigate } from "react-router-dom";
import { ShoppingCart } from "lucide-react";

export default function CartPage() {
  const navigate = useNavigate();
  const items = useCartStore((state) => state.items);
  const getTotal = useCartStore((state) => state.getTotal);
  const clearCart = useCartStore((state) => state.clearCart);
  const getItemCount = useCartStore((state) => state.getItemCount);

  const total = getTotal();
  const itemCount = getItemCount();

  return (
    <PageContainer>
      <Header title={`Cart (${itemCount})`} />
      
      <div className="p-4 space-y-4">
        {items.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-20 text-center">
            <ShoppingCart className="h-16 w-16 text-muted-foreground mb-4" />
            <h2 className="text-lg font-semibold mb-2">Your cart is empty</h2>
            <p className="text-sm text-muted-foreground mb-4">
              Browse our catalog and add some items
            </p>
            <button
              onClick={() => navigate("/")}
              className="px-4 py-2 bg-primary text-primary-foreground rounded-lg text-sm font-medium"
            >
              Browse Catalog
            </button>
          </div>
        ) : (
          <>
            <div className="space-y-3">
              {items.map((item) => (
                <CartItem
                  key={item.product.id}
                  product={item.product}
                  quantity={item.quantity}
                />
              ))}
            </div>

            <div className="border-t pt-4 space-y-3">
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Subtotal</span>
                <span className="font-medium">€{total.toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Delivery</span>
                <span className="font-medium">€5.00</span>
              </div>
              <div className="flex justify-between text-lg font-bold">
                <span>Total</span>
                <span>€{(total + 5).toFixed(2)}</span>
              </div>

              <button
                onClick={() => navigate("/checkout")}
                className="w-full py-3 bg-primary text-primary-foreground rounded-lg font-medium hover:bg-primary/90 transition-colors"
              >
                Proceed to Checkout
              </button>

              <button
                onClick={clearCart}
                className="w-full py-2 text-destructive text-sm hover:underline"
              >
                Clear Cart
              </button>
            </div>
          </>
        )}
      </div>
    </PageContainer>
  );
}
