import PageContainer from "@/widgets/PageContainer";
import Header from "@/widgets/Header";
import { useNavigate } from "react-router-dom";
import { User, FileText, ShoppingCart, Settings, LogOut, ChevronRight } from "lucide-react";
import { Button } from "@/shared/ui/button";

export default function ProfilePage() {
  const navigate = useNavigate();

  const menuItems = [
    { label: "My Orders", icon: ShoppingCart, path: "/orders" },
    { label: "Documents", icon: FileText, path: "/documents" },
    { label: "Settings", icon: Settings, path: "/settings" },
  ];

  return (
    <PageContainer>
      <Header title="Profile" />
      
      <div className="p-4 space-y-6">
        <div className="flex items-center gap-4 p-4 bg-card rounded-lg border">
          <div className="w-16 h-16 rounded-full bg-muted flex items-center justify-center">
            <User className="h-8 w-8 text-muted-foreground" />
          </div>
          <div>
            <h2 className="font-semibold">Guest User</h2>
            <p className="text-sm text-muted-foreground">Tap to view profile</p>
          </div>
        </div>

        <div className="space-y-2">
          {menuItems.map((item) => (
            <button
              key={item.path}
              onClick={() => navigate(item.path)}
              className="w-full p-4 rounded-lg border flex items-center justify-between hover:bg-muted transition-colors"
            >
              <div className="flex items-center gap-3">
                <item.icon className="h-5 w-5 text-muted-foreground" />
                <span className="font-medium text-sm">{item.label}</span>
              </div>
              <ChevronRight className="h-4 w-4 text-muted-foreground" />
            </button>
          ))}
        </div>

        <Button
          variant="outline"
          className="w-full"
          onClick={() => alert("Logged out")}
        >
          <LogOut className="h-4 w-4 mr-2" />
          Log Out
        </Button>
      </div>
    </PageContainer>
  );
}
