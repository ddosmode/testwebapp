import { cn } from "@/lib/utils";

function ScrollArea({ className, children, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div className={cn("relative overflow-hidden", className)} {...props}>
      <div className="h-full w-full rounded-md">{children}</div>
    </div>
  );
}

export { ScrollArea };
