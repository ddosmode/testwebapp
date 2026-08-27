import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL || "/api";

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export interface Product {
  id: string;
  category_id: string;
  name: string;
  description: string;
  price: string;
  is_active: boolean;
  image_url?: string;
}

export interface Category {
  id: string;
  name: string;
  is_active: boolean;
}

export interface CartItem {
  product: Product;
  quantity: number;
}

export interface Order {
  id: string;
  total: string;
  status: string;
  created_at: string;
  items?: OrderItem[];
}

export interface OrderItem {
  id: string;
  product_id: string;
  quantity: number;
  unit_price: string;
}

export interface City {
  id: string;
  name: string;
  is_active: boolean;
}

export interface PaymentMethod {
  id: string;
  name: string;
  code: string;
  is_active: boolean;
}

export interface LegalDocument {
  id: string;
  title: string;
  content: string;
  version: string;
  accepted_at?: string;
}
