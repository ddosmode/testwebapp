import { type ReactNode, useEffect } from "react";
import { useTelegram } from "@/lib/telegram";

interface TelegramProviderProps {
  children: ReactNode;
}

export default function TelegramProvider({ children }: TelegramProviderProps) {
  const { webApp, ready, expand } = useTelegram();

  useEffect(() => {
    if (webApp) {
      ready();
      expand();
    }
  }, [webApp]);

  return <>{children}</>;
}
