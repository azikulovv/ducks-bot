import { InlineKeyboard } from 'grammy'
import { buildMiniAppUrl } from '../utils/promo'

export function openAppKeyboard(promoCode?: string) {
  return new InlineKeyboard().webApp('🦆 Открыть DUCK’S App', buildMiniAppUrl(promoCode))
}
