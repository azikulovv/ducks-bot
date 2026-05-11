import { unregisterFromEvent } from '../../../api/events.api'
import { eventNavigationKeyboard } from '../../../keyboards/events.keyboard'
import { BotContext } from '../../../types/context'

export async function unregister(ctx: BotContext, data: string[]) {
  if (!ctx.user) {
    return ctx.answerCallbackQuery({
      text: 'Нужно привязать аккаунт',
    })
  }

  const eventId = data[2]

  await unregisterFromEvent({ eventId, telegramUserId: ctx.user.telegramId })

  await ctx.editMessageReplyMarkup({
    reply_markup: eventNavigationKeyboard(
      eventId,
      0, // page если нужно
      1, // total
      false,
      '', // game
    ),
  })
  await ctx.answerCallbackQuery({
    text: '❌ Вы отписались',
  })
}
