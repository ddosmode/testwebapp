export function getTelegramWebApp() {
  if (typeof window !== "undefined" && (window as any).Telegram?.WebApp) {
    return (window as any).Telegram.WebApp;
  }
  return null;
}

export function isTelegramEnvironment(): boolean {
  return typeof window !== "undefined" && !!(window as any).Telegram?.WebApp;
}

export function useTelegram() {
  const webApp = getTelegramWebApp();
  
  return {
    webApp,
    initDataUnsafe: webApp?.initDataUnsafe || null,
    user: webApp?.initDataUnsafe?.user || null,
    isTelegram: !!webApp,
    ready: () => webApp?.ready(),
    expand: () => webApp?.expand(),
    HapticFeedback: webApp?.HapticFeedback,
    MainButton: webApp?.MainButton,
    BackButton: webApp?.BackButton,
  };
}

export function verifyInitData(_initData: string): boolean {
  const webApp = getTelegramWebApp();
  if (!webApp) return false;
  
  try {
    return webApp.initData !== undefined;
  } catch {
    return false;
  }
}
