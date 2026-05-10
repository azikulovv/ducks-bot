import { Bot } from 'grammy'
import { BotContext } from '../types/context'
import { getUserByTelegramId, createUser } from '../api/users.api'
import { openAppKeyboard } from '../keyboards/common.keyboard'

export function authMiddleware(bot: Bot<BotContext>) {
  bot.use(async (ctx, next) => {
    const telegramId = ctx.from?.id

    if (!telegramId) {
      return next()
    }

    const user = await getUserByTelegramId(telegramId)

    if (!user) {
      await ctx.reply(
        `
🦆 Добро пожаловать в DUCK’S Club
Доступные команды:

/events
/ratingpoker
/ratingdart
/ratingbill
/rules
/support
      `,
        {
          reply_markup: openAppKeyboard(),
        },
      )

      return
    }

    ctx.user = user

    return next()
  })
}
