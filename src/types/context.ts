import type { Context } from 'grammy'
import type { TelegramUser } from './api/user'

export interface BotContext extends Context {
  user?: TelegramUser | null
}
