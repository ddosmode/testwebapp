import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import PageContainer from "@/widgets/PageContainer";
import Header from "@/widgets/Header";
import { api } from "@/lib/api";
import type { PaymentMethod } from "@/lib/api";
import { Button } from "@/shared/ui/button";
import { Check, CreditCard } from "lucide-react";

export default function PaymentMethodsPage() {
  const navigate = useNavigate();
  const [methods, setMethods] = useState<PaymentMethod[]>([]);
  const [selectedMethod, setSelectedMethod] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function loadMethods() {
      try {
        const res = await api.get("/payments/methods");
        setMethods(res.data);
      } catch (error) {
        console.error("Failed to load payment methods:", error);
      } finally {
        setIsLoading(false);
      }
    }
    loadMethods();
  }, []);

  const handlePlaceOrder = async () => {
    if (!selectedMethod) {
      alert("Please select a payment method");
      return;
    }
    try {
      await api.post("/orders", {
        payment_method_id: selectedMethod,
      });
      alert("Order placed successfully!");
      navigate("/orders");
    } catch (error) {
      console.error("Failed to place order:", error);
      alert("Failed to place order. Please try again.");
    }
  };

  return (
    <PageContainer>
      <Header title="Payment Method" />
      
      <div className="p-4 space-y-4">
        <p className="text-sm text-muted-foreground">
          Select your preferred payment method
        </p>

        {isLoading ? (
          <div className="text-center py-12 text-muted-foreground">Loading...</div>
        ) : (
          <div className="space-y-2">
            {methods.map((method) => (
              <button
                key={method.id}
                onClick={() => setSelectedMethod(method.id)}
                className={`w-full p-4 rounded-lg border text-left flex items-center justify-between transition-colors ${
                  selectedMethod === method.id
                    ? "border-primary bg-primary/5"
                    : "hover:bg-muted"
                }`}
              >
                <div className="flex items-center gap-3">
                  <CreditCard className="h-5 w-5 text-muted-foreground" />
                  <span className="font-medium">{method.name}</span>
                </div>
                {selectedMethod === method.id && (
                  <Check className="h-5 w-5 text-primary" />
                )}
              </button>
            ))}
          </div>
        )}

        <div className="flex gap-3 pt-4">
          <Button
            variant="outline"
            className="flex-1"
            onClick={() => navigate(-1)}
          >
            Back
          </Button>
          <Button
            className="flex-1"
            onClick={handlePlaceOrder}
            disabled={!selectedMethod}
          >
            Place Order
          </Button>
        </div>
      </div>
    </PageContainer>
  );
}
