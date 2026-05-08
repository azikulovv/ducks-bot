import { MiddlewareFn } from 'grammy'
import { BotContext } from '../types/context'
import { getUserByTelegramId } from '../api/users.api'

export const authMiddleware: MiddlewareFn<BotContext> = async (ctx, next) => {
  const telegramId = ctx.from?.id

  if (!telegramId) {
    return next()
  }

  const user = await getUserByTelegramId(telegramId)

  ctx.user = user

  await next()
}
