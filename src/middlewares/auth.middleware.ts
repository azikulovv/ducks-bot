import { Bot } from 'grammy'
import { BotContext } from '../types/context'
import { getUserByTelegramId } from '../api/users.api'
import { openAppKeyboard } from '../keyboards/common.keyboard'

const PUBLIC_COMMANDS = new Set(['start', 'rules', 'support'])
const PUBLIC_CALLBACKS = new Set(['about:open'])

export function authMiddleware(bot: Bot<BotContext>) {
  bot.use(async (ctx, next) => {
    const telegramId = ctx.from?.id

    if (!telegramId) {
      return next()
    }

    const command = getCommand(ctx.message?.text)
    const callbackData = ctx.callbackQuery?.data

    if (command && PUBLIC_COMMANDS.has(command)) {
      return next()
    }

    if (callbackData && PUBLIC_CALLBACKS.has(callbackData)) {
      return next()
    }

    const user = await getUserByTelegramId({
      telegramUserId: telegramId,
    })

    if (!user) {
      await ctx.reply('🦆 Сначала авторизуйтесь через мини-приложение', {
        reply_markup: openAppKeyboard(),
      })

      return
    }

    ctx.user = user

    return next()
  })
}

function getCommand(text?: string) {
  if (!text?.startsWith('/')) {
    return null
  }

  return text.split(' ')[0].replace('/', '')
}
