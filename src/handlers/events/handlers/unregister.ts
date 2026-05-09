import { unregisterFromEvent } from '../../../api/events.api'
import { BotContext } from '../../../types/context'

export async function unregister(ctx: BotContext, data: string[]) {
  if (!ctx.user) {
    return ctx.answerCallbackQuery({
      text: 'Нужно привязать аккаунт',
    })
  }

  const eventId = data[2]

  await unregisterFromEvent(eventId, ctx.user.telegram_id)

  await ctx.answerCallbackQuery({
    text: '❌ Вы отписались',
  })
}
