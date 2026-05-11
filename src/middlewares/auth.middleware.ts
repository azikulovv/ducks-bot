import { Bot } from 'grammy'
import { BotContext } from '../types/context'
import { getUserByTelegramId } from '../api/users.api'
import { openAppKeyboard } from '../keyboards/common.keyboard'

const PUBLIC_COMMANDS = new Set(['start', 'rules', 'support'])

export function authMiddleware(bot: Bot<BotContext>) {
  bot.use(async (ctx, next) => {
    const telegramId = ctx.from?.id

    if (!telegramId) {
      return next()
    }

    if (ctx.message?.text?.startsWith('/')) {
      const command = ctx.message.text.split(' ')[0].replace('/', '')

      if (PUBLIC_COMMANDS.has(command)) {
        return next()
      }
    }

    const user = await getUserByTelegramId({
      telegramUserId: telegramId,
    })

    if (!user) {
      await ctx.reply('🦆 Сначала авторизуйтесь через мини приложение', {
        reply_markup: openAppKeyboard(),
      })

      return
    }

    ctx.user = user

    return next()
  })
}
