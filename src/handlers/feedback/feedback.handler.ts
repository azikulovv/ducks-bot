import { Bot } from 'grammy'
import { BotContext } from '../../types/context'
import { sendFeedback } from '../../api/feedback.api'
import { isFeedbackMode, startFeedback, stopFeedback } from './feedback.state'

export function registerFeedbackHandler(bot: Bot<BotContext>) {
  bot.command('feedback', async (ctx) => {
    if (!ctx.user) {
      return ctx.reply('Сначала нужно авторизоваться')
    }

    const userId = String(ctx.user.id)
    startFeedback(userId)

    await ctx.reply('✍️ Напишите ваш отзыв одним сообщением')
  })

  bot.on('message:text', async (ctx) => {
    if (!ctx.user) return

    const userId = String(ctx.user.id)

    if (!isFeedbackMode(userId)) return

    try {
      const message = ctx.message.text

      await sendFeedback({
        telegramUserId: ctx.user.telegramId,
        message,
      })

      stopFeedback(userId)

      await ctx.reply('✅ Спасибо за ваш отзыв!')
    } catch (e) {
      // console.error(e)
      await ctx.reply('❌ Ошибка отправки. Попробуйте позже.')
    }
  })
}
