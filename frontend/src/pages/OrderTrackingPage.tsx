import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import PageContainer from "@/widgets/PageContainer";
import Header from "@/widgets/Header";
import { api } from "@/lib/api";
import type { Order } from "@/lib/api";
import { MapPin, Package, Clock, CheckCircle } from "lucide-react";
import { cn } from "@/lib/utils";

export default function OrderTrackingPage() {
  const { id } = useParams<{ id: string }>();
  const [order, setOrder] = useState<Order | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function loadOrder() {
      if (!id) return;
      try {
        const res = await api.get(`/orders/${id}`);
        setOrder(res.data);
      } catch (error) {
        console.error("Failed to load order:", error);
      } finally {
        setIsLoading(false);
      }
    }
    loadOrder();
  }, [id]);

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case "completed":
        return "bg-green-100 text-green-800";
      case "processing":
        return "bg-blue-100 text-blue-800";
      case "paid":
        return "bg-yellow-100 text-yellow-800";
      case "cancelled":
        return "bg-red-100 text-red-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status.toLowerCase()) {
      case "completed":
        return <CheckCircle className="h-5 w-5" />;
      case "processing":
        return <Package className="h-5 w-5" />;
      default:
        return <Clock className="h-5 w-5" />;
    }
  };

  if (isLoading) {
    return (
      <PageContainer>
        <Header title="Order Tracking" />
        <div className="p-4 text-center text-muted-foreground">Loading...</div>
      </PageContainer>
    );
  }

  if (!order) {
    return (
      <PageContainer>
        <Header title="Order Tracking" />
        <div className="p-4 text-center text-muted-foreground">Order not found</div>
      </PageContainer>
    );
  }

  return (
    <PageContainer>
      <Header title={`Order #${order.id.slice(0, 8)}`} />
      
      <div className="p-4 space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-muted-foreground">Order Status</p>
            <div className="flex items-center gap-2 mt-1">
              {getStatusIcon(order.status)}
              <span className={cn("px-2 py-1 rounded-full text-xs font-medium", getStatusColor(order.status))}>
                {order.status.toUpperCase()}
              </span>
            </div>
          </div>
          <div className="text-right">
            <p className="text-2xl font-bold">€{parseFloat(order.total).toFixed(2)}</p>
            <p className="text-xs text-muted-foreground">
              {new Date(order.created_at).toLocaleDateString()}
            </p>
          </div>
        </div>

        <div className="border rounded-lg p-4 space-y-4">
          <h3 className="font-semibold flex items-center gap-2">
            <MapPin className="h-4 w-4" />
            Delivery Address
          </h3>
          <p className="text-sm text-muted-foreground">
            Will be updated once order is processed
          </p>
        </div>

        {order.items && order.items.length > 0 && (
          <div className="border rounded-lg p-4 space-y-3">
            <h3 className="font-semibold">Order Items</h3>
            {order.items.map((item) => (
              <div key={item.id} className="flex justify-between text-sm">
                <span>Product #{item.product_id.slice(0, 8)}</span>
                <span>x{item.quantity} - €{parseFloat(item.unit_price).toFixed(2)}</span>
              </div>
            ))}
          </div>
        )}

        <div className="border rounded-lg p-4">
          <h3 className="font-semibold mb-3">Tracking Timeline</h3>
          <div className="space-y-3">
            <div className="flex items-center gap-3">
              <div className="w-2 h-2 rounded-full bg-green-500" />
              <div>
                <p className="text-sm font-medium">Order Created</p>
                <p className="text-xs text-muted-foreground">
                  {new Date(order.created_at).toLocaleString()}
                </p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <div className={`w-2 h-2 rounded-full ${order.status === "paid" || order.status === "processing" || order.status === "completed" ? "bg-green-500" : "bg-gray-300"}`} />
              <div>
                <p className="text-sm font-medium">Payment Confirmed</p>
                <p className="text-xs text-muted-foreground">
                  {order.status === "paid" || order.status === "processing" || order.status === "completed" ? "Completed" : "Pending"}
                </p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <div className={`w-2 h-2 rounded-full ${order.status === "processing" || order.status === "completed" ? "bg-green-500" : "bg-gray-300"}`} />
              <div>
                <p className="text-sm font-medium">Processing</p>
                <p className="text-xs text-muted-foreground">
                  {order.status === "processing" || order.status === "completed" ? "In progress" : "Waiting"}
                </p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <div className={`w-2 h-2 rounded-full ${order.status === "completed" ? "bg-green-500" : "bg-gray-300"}`} />
              <div>
                <p className="text-sm font-medium">Delivered</p>
                <p className="text-xs text-muted-foreground">
                  {order.status === "completed" ? "Completed" : "Waiting"}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </PageContainer>
  );
}
