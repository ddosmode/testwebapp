import { type ReactNode } from "react";
import { cn } from "@/lib/utils";

interface PageContainerProps {
  children: ReactNode;
  className?: string;
  withNav?: boolean;
}

export default function PageContainer({ children, className, withNav = true }: PageContainerProps) {
  return (
    <div className={cn("min-h-screen bg-background", withNav && "pb-20", className)}>
      <main className="max-w-lg mx-auto">{children}</main>
    </div>
  );
}
