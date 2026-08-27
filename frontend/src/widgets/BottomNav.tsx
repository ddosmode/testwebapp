import { Link, useLocation } from "react-router-dom";
import { cn } from "@/lib/utils";
import { ShoppingCart, FileText, User, Home } from "lucide-react";

const navItems = [
  { to: "/", label: "Catalog", icon: Home },
  { to: "/cart", label: "Cart", icon: ShoppingCart },
  { to: "/documents", label: "Docs", icon: FileText },
  { to: "/profile", label: "Profile", icon: User },
];

export default function BottomNav() {
  const location = useLocation();

  return (
    <nav className="fixed bottom-0 left-0 right-0 border-t bg-background z-50">
      <div className="flex items-center justify-around h-16 max-w-lg mx-auto">
        {navItems.map((item) => {
          const isActive = location.pathname === item.to || 
            (item.to !== "/" && location.pathname.startsWith(item.to));
          return (
            <Link
              key={item.to}
              to={item.to}
              className={cn(
                "flex flex-col items-center justify-center flex-1 h-full text-xs transition-colors",
                isActive ? "text-primary" : "text-muted-foreground"
              )}
            >
              <item.icon className="h-5 w-5 mb-1" />
              {item.label}
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
