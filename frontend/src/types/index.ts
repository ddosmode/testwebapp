export interface RootState {
  user: TelegramUser | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

export interface TelegramUser {
  id: number;
  username?: string;
  first_name?: string;
  last_name?: string;
  photo_url?: string;
}
