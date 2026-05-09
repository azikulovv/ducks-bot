import { Bot } from 'grammy'
import { BotContext } from '../types/context'
import { getUserByTelegramId, createUser } from '../api/users.api'

export function authMiddleware(bot: Bot<BotContext>) {
  bot.use(async (ctx, next) => {
    const telegramId = ctx.from?.id

    if (!telegramId) {
      return next()
    }

    let user = await getUserByTelegramId(telegramId)

    if (!user) {
      user = await createUser({
        telegram_id: telegramId.toString(),
        name: ctx.from?.first_name || null,
      })
    }

    ctx.user = user

    console.log(user)
    return next()
  })
}
