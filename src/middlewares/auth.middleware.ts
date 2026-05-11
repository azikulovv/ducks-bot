import { Bot } from 'grammy'
import { BotContext } from '../types/context'
import { getUserByTelegramId } from '../api/users.api'
import { openAppKeyboard } from '../keyboards/common.keyboard'

export function authMiddleware(bot: Bot<BotContext>) {
  bot.use(async (ctx, next) => {
    const telegramId = ctx.from?.id

    if (!telegramId) {
      return next()
    }

    const user = await getUserByTelegramId(telegramId)

    if (!user) {
      await ctx.reply(`🦆 Сначало авторизуйтесь через мини приложение`, {
        reply_markup: openAppKeyboard(),
      })

      return
    }

    ctx.user = user

    return next()
  })
}
