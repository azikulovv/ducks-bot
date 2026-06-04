import { InlineKeyboard } from 'grammy'
import { buildMiniAppUrl } from '../utils/promo'

export function openAppKeyboard(promoCode?: string) {
  return new InlineKeyboard()
    .webApp('🚀 Записаться на турнир', buildMiniAppUrl(promoCode))
    .row()
    .text('🗓️ Ближайшее расписание', 'events:list')
    .row()
    .text("🦆 Что такое DUCK'S SPACE", 'about:open')
}
