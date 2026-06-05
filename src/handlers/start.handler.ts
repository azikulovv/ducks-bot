import { Bot, InputFile } from 'grammy'
import { BotContext } from '../types/context'
import { openAppKeyboard } from '../keyboards/common.keyboard'
import { trackTelegramPromoStart } from '../api/promo-links.api'
import { extractStartPayload, isValidPromoCode } from '../utils/promo'
import { START_MESSAGE } from '../constants/messages'
import path from 'path'

export function registerStartHandler(bot: Bot<BotContext>) {
  bot.command('start', async (ctx) => {
    const payload = extractStartPayload(ctx)
    const promoCode = payload && isValidPromoCode(payload) ? payload : undefined

    if (payload && !promoCode) {
      console.warn('INVALID_PROMO_CODE_SKIPPED:', {
        telegramUserId: ctx.from?.id,
        promoCode: payload,
      })
    }

    if (ctx.from?.id && promoCode) {
      void trackTelegramPromoStart({
        telegramUserId: ctx.from.id,
        promoCode,
      })

      if (ctx.session) {
        ctx.session.promoCode = promoCode
      }
    }

    await ctx.replyWithPhoto(new InputFile(path.resolve('assets/start.jpg')), {
      caption: START_MESSAGE,
      reply_markup: openAppKeyboard(promoCode),
    })
  })
}
