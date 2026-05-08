import { Context } from 'grammy'

export interface TelegramUser {
  id: number
  email: string
  telegram_id: number
}

export interface BotContext extends Context {
  user?: TelegramUser | null
}
