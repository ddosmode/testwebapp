import { BrowserRouter, Routes, Route } from "react-router-dom";
import CatalogPage from "@/pages/CatalogPage";
import CartPage from "@/pages/CartPage";
import ProfilePage from "@/pages/ProfilePage";
import DocumentsPage from "@/pages/DocumentsPage";
import ProductPage from "@/pages/ProductPage";
import CheckoutPage from "@/pages/CheckoutPage";
import OrdersPage from "@/pages/OrdersPage";
import OrderTrackingPage from "@/pages/OrderTrackingPage";
import PaymentMethodsPage from "@/pages/PaymentMethodsPage";
import CitySelectionPage from "@/pages/CitySelectionPage";
import LegalAcceptancePage from "@/pages/LegalAcceptancePage";
import BottomNav from "@/widgets/BottomNav";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<CatalogPage />} />
        <Route path="/cart" element={<CartPage />} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="/documents" element={<DocumentsPage />} />
        <Route path="/product/:id" element={<ProductPage />} />
        <Route path="/checkout" element={<CheckoutPage />} />
        <Route path="/orders" element={<OrdersPage />} />
        <Route path="/orders/:id" element={<OrderTrackingPage />} />
        <Route path="/payment-methods" element={<PaymentMethodsPage />} />
        <Route path="/city" element={<CitySelectionPage />} />
        <Route path="/legal" element={<LegalAcceptancePage />} />
      </Routes>
      <BottomNav />
    </BrowserRouter>
  );
}
