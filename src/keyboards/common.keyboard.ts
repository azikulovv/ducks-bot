import { InlineKeyboard } from 'grammy'
import { env } from '../config/env'

export function openAppKeyboard() {
  return new InlineKeyboard().webApp('🦆 Открыть DUCK’S App', env.MINI_APP_URL)
}
