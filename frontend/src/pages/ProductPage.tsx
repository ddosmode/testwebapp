import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import PageContainer from "@/widgets/PageContainer";
import Header from "@/widgets/Header";
import { api } from "@/lib/api";
import type { Product } from "@/lib/api";
import { useCartStore } from "@/entities/cartStore";
import { ShoppingCart } from "lucide-react";

export default function ProductPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [product, setProduct] = useState<Product | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [quantity, setQuantity] = useState(1);
  const addItem = useCartStore((state) => state.addItem);

  useEffect(() => {
    async function loadProduct() {
      if (!id) return;
      try {
        const res = await api.get(`/catalog/products/${id}`);
        setProduct(res.data);
      } catch (error) {
        console.error("Failed to load product:", error);
      } finally {
        setIsLoading(false);
      }
    }
    loadProduct();
  }, [id]);

  const handleAddToCart = () => {
    if (product) {
      addItem(product, quantity);
      alert("Added to cart!");
    }
  };

  if (isLoading) {
    return (
      <PageContainer>
        <Header title="Product" onBack={() => navigate(-1)} />
        <div className="p-4 text-center text-muted-foreground">Loading...</div>
      </PageContainer>
    );
  }

  if (!product) {
    return (
      <PageContainer>
        <Header title="Product" onBack={() => navigate(-1)} />
        <div className="p-4 text-center text-muted-foreground">Product not found</div>
      </PageContainer>
    );
  }

  return (
    <PageContainer>
      <Header title="Product Details" onBack={() => navigate(-1)} />
      
      <div className="aspect-square bg-muted flex items-center justify-center">
        <ShoppingCart className="h-24 w-24 text-muted-foreground" />
      </div>

      <div className="p-4 space-y-4">
        <div>
          <h1 className="text-2xl font-bold">{product.name}</h1>
          <p className="text-3xl font-bold text-primary mt-2">
            €{parseFloat(product.price).toFixed(2)}
          </p>
        </div>

        <div className="prose prose-sm max-w-none">
          <h3 className="font-semibold text-sm uppercase tracking-wider text-muted-foreground">
            Description
          </h3>
          <p className="text-sm mt-2 leading-relaxed">{product.description}</p>
        </div>

        <div className="flex items-center gap-4">
          <span className="text-sm font-medium">Quantity:</span>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setQuantity(Math.max(1, quantity - 1))}
              className="w-8 h-8 rounded-full border flex items-center justify-center hover:bg-muted"
            >
              -
            </button>
            <span className="w-8 text-center font-medium">{quantity}</span>
            <button
              onClick={() => setQuantity(quantity + 1)}
              className="w-8 h-8 rounded-full border flex items-center justify-center hover:bg-muted"
            >
              +
            </button>
          </div>
        </div>

        <button
          onClick={handleAddToCart}
          className="w-full py-3 bg-primary text-primary-foreground rounded-lg font-medium hover:bg-primary/90 transition-colors"
        >
          Add to Cart - €{(parseFloat(product.price) * quantity).toFixed(2)}
        </button>
      </div>
    </PageContainer>
  );
}
