import { registerToEvent } from '../../../api/events.api'
import { BotContext } from '../../../types/context'

export async function register(ctx: BotContext, data: string[]) {
  if (!ctx.user) {
    return ctx.answerCallbackQuery({
      text: 'Нужно привязать аккаунт',
    })
  }

  const eventId = data[2]

  await registerToEvent(eventId, ctx.user.telegram_id)

  await ctx.answerCallbackQuery({
    text: '✅ Вы записаны',
  })
}
