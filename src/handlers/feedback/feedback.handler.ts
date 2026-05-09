import { Bot } from 'grammy'
import { BotContext } from '../../types/context'
import { sendFeedback } from '../../api/feedback.api'
import { isFeedbackMode, stopFeedback } from './feedback.state'

export function registerFeedbackHandler(bot: Bot<BotContext>) {
  bot.command('feedback', async (ctx) => {
    if (!ctx.user) {
      return ctx.reply('Сначала нужно авторизоваться')
    }

    await ctx.reply('✍️ Напишите ваш отзыв одним сообщением')
  })

  bot.on('message:text', async (ctx) => {
    if (!ctx.user) return

    const userId = ctx.user.id

    // if (!isFeedbackMode(String(userId))) return

    try {
      const message = ctx.message.text

      /**
       * send to backend
       */
      await sendFeedback({
        telegramUserId: ctx.user.telegram_id,
        message,
      })

      stopFeedback(String(userId))

      await ctx.reply('✅ Спасибо за ваш отзыв!')
    } catch (e) {
      console.error(e)

      await ctx.reply('❌ Ошибка отправки. Попробуйте позже.')
    }
  })
}
